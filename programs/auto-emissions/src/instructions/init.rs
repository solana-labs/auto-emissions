//! Init instruction handler

use {
    crate::{error::AutoEmissionsError, program::AutoEmissions, state::protocol::Protocol, utils},
    anchor_lang::prelude::*,
};

#[derive(Accounts)]
pub struct Init<'info> {
    #[account(mut)]
    pub upgrade_authority: Signer<'info>,

    #[account(
        init,
        payer = upgrade_authority,
        space = Protocol::LEN,
        seeds = [b"protocol"],
        bump
    )]
    pub protocol: Box<Account<'info, Protocol>>,

    /// CHECK: empty PDA, will be set as authority for token accounts
    #[account(
        init,
        payer = upgrade_authority,
        space = 0,
        seeds = [b"transfer_authority"],
        bump
    )]
    pub transfer_authority: AccountInfo<'info>,

    /// CHECK: ProgramData account, doesn't work in tests
    #[account()]
    pub autoemissions_program_data: AccountInfo<'info /*, ProgramData*/>,

    autoemissions_program: Program<'info, AutoEmissions>,

    system_program: Program<'info, System>,
}

#[derive(AnchorSerialize, AnchorDeserialize, Copy, Clone)]
pub struct InitParams {
    pub authority: Pubkey,
    pub allow_claims: bool,
    pub allow_early_withdrawals: bool,
    pub allow_group_authorities: bool,
}

pub fn init(ctx: Context<Init>, params: &InitParams) -> Result<()> {
    utils::validate_upgrade_authority(
        ctx.accounts.upgrade_authority.key(),
        &ctx.accounts.autoemissions_program_data.to_account_info(),
        &ctx.accounts.autoemissions_program.to_account_info(),
    )?;

    // record protocol state
    let protocol = ctx.accounts.protocol.as_mut();
    protocol.authority = params.authority;
    protocol.allow_claims = params.allow_claims;
    protocol.allow_early_withdrawals = params.allow_early_withdrawals;
    protocol.allow_group_authorities = params.allow_group_authorities;
    protocol.transfer_authority_bump = *ctx
        .bumps
        .get("transfer_authority")
        .ok_or(ProgramError::InvalidSeeds)?;

    if !protocol.validate() {
        return err!(AutoEmissionsError::InvalidProtocolConfig);
    }

    Ok(())
}
