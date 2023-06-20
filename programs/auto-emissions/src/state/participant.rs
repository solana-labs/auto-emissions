//! Participant state.

use {
    crate::{constants::BPS_POWER, math},
    anchor_lang::prelude::*,
};

#[account]
#[derive(Default, Debug, PartialEq)]
pub struct Participant {
    pub group: Pubkey,
    pub owner: Pubkey,
    pub allocation_percent: u64, // with implied BPS_DECIMALS
    pub claimed_amount: u64,
}

impl Participant {
    pub const LEN: usize = 8 + std::mem::size_of::<Participant>();

    pub fn validate(&self) -> bool {
        self.group != Pubkey::default()
            && self.owner != Pubkey::default()
            && self.allocation_percent > 0
    }

    pub fn get_entitled_amount(&self, unlocked_amount: u64) -> Result<u64> {
        let entitled_total = math::checked_as_u64(math::checked_div(
            math::checked_mul(unlocked_amount as u128, self.allocation_percent as u128)?,
            BPS_POWER as u128,
        )?)?;
        if entitled_total > self.claimed_amount {
            math::checked_sub(entitled_total, self.claimed_amount)
        } else {
            Ok(0)
        }
    }

    pub fn claim_amount(&mut self, amount: u64) -> Result<()> {
        self.claimed_amount = math::checked_add(self.claimed_amount, amount)?;
        Ok(())
    }
}
