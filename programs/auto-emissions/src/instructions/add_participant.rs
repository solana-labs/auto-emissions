//! AddParticipant instruction handler

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
#[instruction(params: AddParticipantParams)]
pub struct AddParticipant<'info> {
    #[account(mut)]
    pub authority: Signer<'info>,

    #[account()]
    pub protocol: Box<Account<'info, Protocol>>,

    #[account(mut)]
    pub group: Box<Account<'info, Group>>,

    #[account(
        init,
        payer = authority,
        space = Participant::LEN,
        seeds = [b"participant",
                 group.key().as_ref(),
                 params.owner.as_ref()],
        bump
    )]
    pub participant: Box<Account<'info, Participant>>,

    system_program: Program<'info, System>,
}

#[derive(AnchorSerialize, AnchorDeserialize)]
pub struct AddParticipantParams {
    pub owner: Pubkey,
    pub allocation_percent: u64, // with implied BPS_DECIMALS
}

pub fn add_participant(ctx: Context<AddParticipant>, params: &AddParticipantParams) -> Result<()> {
    let group = ctx.accounts.group.as_mut();

    require!(
        ctx.accounts.protocol.authority == ctx.accounts.authority.key()
            || (ctx.accounts.protocol.allow_group_authorities
                && group.group_authority == ctx.accounts.authority.key()),
        AutoEmissionsError::InvalidAuthority
    );

    let participant = ctx.accounts.participant.as_mut();
    participant.group = group.key();
    participant.owner = params.owner;
    participant.allocation_percent = params.allocation_percent;
    participant.claimed_amount = 0;

    if !participant.validate() {
        return err!(AutoEmissionsError::InvalidParticipantConfig);
    }

    group.participants = math::checked_add(group.participants, 1)?;
    group.allocation_percent =
        math::checked_add(group.allocation_percent, participant.allocation_percent)?;

    if group.allocation_percent > BPS_POWER {
        return err!(AutoEmissionsError::InvalidGroupState);
    }

    Ok(())
}
