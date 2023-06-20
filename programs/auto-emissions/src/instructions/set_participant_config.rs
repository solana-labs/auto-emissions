//! SetParticipantConfig instruction handler

use {
    crate::{
        constants::BPS_POWER,
        error::AutoEmissionsError,
        math,
        state::{group::Group, participant::Participant, protocol::Protocol},
    },
    anchor_lang::prelude::*,
};

#[derive(Accounts)]
pub struct SetParticipantConfig<'info> {
    #[account()]
    pub authority: Signer<'info>,

    #[account()]
    pub protocol: Box<Account<'info, Protocol>>,

    #[account(mut)]
    pub group: Box<Account<'info, Group>>,

    #[account(
        mut,
        has_one = group @ AutoEmissionsError::InvalidGroupAddress,
    )]
    pub participant: Box<Account<'info, Participant>>,
}

#[derive(AnchorSerialize, AnchorDeserialize)]
pub struct SetParticipantConfigParams {
    pub owner: Pubkey,
    pub allocation_percent: u64, // with implied BPS_DECIMALS
}

pub fn set_participant_config(
    ctx: Context<SetParticipantConfig>,
    params: &SetParticipantConfigParams,
) -> Result<()> {
    let group = ctx.accounts.group.as_mut();

    require!(
        ctx.accounts.protocol.authority == ctx.accounts.authority.key()
            || (ctx.accounts.protocol.allow_group_authorities
                && group.group_authority == ctx.accounts.authority.key()),
        AutoEmissionsError::InvalidAuthority
    );

    let participant = ctx.accounts.participant.as_mut();
    group.allocation_percent =
        math::checked_sub(group.allocation_percent, participant.allocation_percent)?;
    group.allocation_percent =
        math::checked_add(group.allocation_percent, params.allocation_percent)?;

    if group.allocation_percent > math::checked_mul(100, BPS_POWER)? {
        return err!(AutoEmissionsError::InvalidGroupState);
    }

    participant.owner = params.owner;
    participant.allocation_percent = params.allocation_percent;

    if !participant.validate() {
        return err!(AutoEmissionsError::InvalidParticipantConfig);
    }

    Ok(())
}
