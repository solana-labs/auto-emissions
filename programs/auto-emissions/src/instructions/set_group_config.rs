//! SetGroupConfig instruction handler

use {
    crate::{
        error::AutoEmissionsError,
        state::{group::Group, protocol::Protocol},
    },
    anchor_lang::prelude::*,
};

#[derive(Accounts)]
pub struct SetGroupConfig<'info> {
    #[account()]
    pub authority: Signer<'info>,

    #[account(
        has_one = authority @ AutoEmissionsError::InvalidAuthority
    )]
    pub protocol: Box<Account<'info, Protocol>>,

    #[account(mut)]
    pub group: Box<Account<'info, Group>>,
}

#[derive(AnchorSerialize, AnchorDeserialize)]
pub struct SetGroupConfigParams {
    pub group_authority: Pubkey,
    pub allow_claims: bool,
    pub allow_early_withdrawals: bool,
    pub initial_unlock_time: u64,
    pub initial_unlock_percent: u64, // with implied BPS_DECIMALS
    pub unlock_frequency: u64,
    pub unlock_count: u64,
    pub claim_end_time: u64,
}

pub fn set_group_config(ctx: Context<SetGroupConfig>, params: &SetGroupConfigParams) -> Result<()> {
    let group = ctx.accounts.group.as_mut();

    require_eq!(
        group.claimed_amount,
        0,
        AutoEmissionsError::InvalidGroupState
    );

    group.group_authority = params.group_authority;
    group.allow_claims = params.allow_claims;
    group.allow_early_withdrawals = params.allow_early_withdrawals;
    group.initial_unlock_time = params.initial_unlock_time;
    group.initial_unlock_percent = params.initial_unlock_percent;
    group.unlock_frequency = params.unlock_frequency;
    group.unlock_count = params.unlock_count;
    group.claim_end_time = params.claim_end_time;

    if !group.validate(group.get_time()?) {
        return err!(AutoEmissionsError::InvalidGroupConfig);
    }

    Ok(())
}
