//! RemoveParticipant instruction handler

use {
    crate::{
        error::AutoEmissionsError,
        math,
        state::{group::Group, participant::Participant, protocol::Protocol},
    },
    anchor_lang::prelude::*,
};

#[derive(Accounts)]
pub struct RemoveParticipant<'info> {
    #[account()]
    pub authority: Signer<'info>,

    #[account()]
    pub protocol: Box<Account<'info, Protocol>>,

    #[account(mut)]
    pub group: Box<Account<'info, Group>>,

    #[account(
        mut,
        has_one = group @ AutoEmissionsError::InvalidGroupAddress,
        close = authority
    )]
    pub participant: Box<Account<'info, Participant>>,
}

#[derive(AnchorSerialize, AnchorDeserialize)]
pub struct RemoveParticipantParams {}

pub fn remove_participant(
    ctx: Context<RemoveParticipant>,
    _params: &RemoveParticipantParams,
) -> Result<()> {
    let group = ctx.accounts.group.as_mut();

    require!(
        ctx.accounts.protocol.authority == ctx.accounts.authority.key()
            || (ctx.accounts.protocol.allow_group_authorities
                && group.group_authority == ctx.accounts.authority.key()),
        AutoEmissionsError::InvalidAuthority
    );

    require_eq!(
        group.claimed_amount,
        0,
        AutoEmissionsError::InvalidGroupState
    );

    group.participants = math::checked_sub(group.participants, 1)?;
    group.allocation_percent = math::checked_sub(
        group.allocation_percent,
        ctx.accounts.participant.allocation_percent,
    )?;

    Ok(())
}
