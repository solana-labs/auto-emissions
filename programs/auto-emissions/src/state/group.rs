//! Group state.

use {
    crate::{constants::BPS_POWER, math},
    anchor_lang::prelude::*,
};

#[account]
#[derive(Default, Debug, PartialEq)]
pub struct Group {
    pub project_name: String,
    pub group_name: String,
    pub group_authority: Pubkey,

    pub allow_claims: bool,
    pub allow_early_withdrawals: bool,

    pub initial_unlock_time: u64,
    pub initial_unlock_percent: u64, // with implied BPS_DECIMALS
    pub unlock_frequency: u64,
    pub unlock_count: u64,
    pub claim_end_time: u64,

    pub custody: Pubkey,
    pub mint: Pubkey,
    pub mint_decimals: u8,

    pub claimed_amount: u64,

    pub participants: u64,
    pub allocation_percent: u64, // with implied BPS_DECIMALS

    // time of inception, also used as current wall clock time for testing
    pub inception_time: u64,
}

impl Group {
    pub const LEN: usize = 8 + std::mem::size_of::<Group>();

    pub fn validate(&self, curtime: u64) -> bool {
        if self.project_name.is_empty()
            || self.project_name.len() > 64
            || self.group_name.is_empty()
            || self.group_name.len() > 64
            || self.group_authority == Pubkey::default()
            || self.initial_unlock_time == 0
            || self.initial_unlock_percent > BPS_POWER
            || self.claim_end_time <= curtime
            || self.claim_end_time <= self.initial_unlock_time
        {
            return false;
        }

        if self.initial_unlock_percent == BPS_POWER {
            if self.unlock_frequency != 0 || self.unlock_count != 0 {
                return false;
            }
        } else {
            if self.unlock_frequency == 0 || self.unlock_count == 0 {
                return false;
            }
            if let Ok(unlock_duration) = math::checked_mul(self.unlock_frequency, self.unlock_count)
            {
                if let Ok(unlock_end_time) =
                    math::checked_add(self.initial_unlock_time, unlock_duration)
                {
                    if self.claim_end_time > unlock_end_time {
                        return true;
                    }
                }
            }
            return false;
        }

        true
    }

    #[cfg(feature = "test")]
    pub fn get_time(&self) -> Result<u64> {
        Ok(self.inception_time)
    }

    #[cfg(not(feature = "test"))]
    pub fn get_time(&self) -> Result<u64> {
        let time = solana_program::sysvar::clock::Clock::get()?.unix_timestamp;
        if time > 0 {
            math::checked_as_u64(time)
        } else {
            Err(ProgramError::InvalidAccountData.into())
        }
    }

    pub fn is_expired(&self, curtime: u64) -> bool {
        curtime > self.claim_end_time
    }

    pub fn get_unlocked_amount(&self, token_balance: u64, curtime: u64) -> Result<u64> {
        if curtime < self.initial_unlock_time {
            return Ok(0);
        }

        let total_supply = math::checked_add(token_balance, self.claimed_amount)?;

        if self.initial_unlock_percent >= BPS_POWER {
            return Ok(total_supply);
        }

        let initial_unlocked = math::checked_as_u64(math::checked_div(
            math::checked_mul(total_supply as u128, self.initial_unlock_percent as u128)?,
            BPS_POWER as u128,
        )?)?;

        if self.unlock_count == 0 || self.unlock_frequency == 0 {
            // should never happen if the group was validated
            return Ok(initial_unlocked);
        }

        let intervals_count = math::checked_div(
            math::checked_sub(curtime, self.initial_unlock_time)?,
            self.unlock_frequency,
        )?;
        let intervals_count = std::cmp::min(intervals_count, self.unlock_count);

        if intervals_count == self.unlock_count {
            return Ok(total_supply);
        }

        // extra_unlocked = unlocked_per_interval * intervals_count
        // where unlocked_per_interval = (total_supply - initial_unlocked) / unlock_count
        let extra_unlocked = math::checked_as_u64(math::checked_div(
            math::checked_mul(
                math::checked_sub(total_supply, initial_unlocked)? as u128,
                intervals_count as u128,
            )?,
            self.unlock_count as u128,
        )?)?;

        math::checked_add(initial_unlocked, extra_unlocked)
    }

    pub fn claim_amount(&mut self, amount: u64) -> Result<()> {
        self.claimed_amount = math::checked_add(self.claimed_amount, amount)?;
        Ok(())
    }
}
