//! AddGroup instruction handler

use {
    crate::{
        error::AutoEmissionsError,
        state::{group::Group, protocol::Protocol},
    },
    anchor_lang::prelude::*,
    anchor_spl::token::{Mint, Token, TokenAccount},
};

#[derive(Accounts)]
#[instruction(params: AddGroupParams)]
pub struct AddGroup<'info> {
    #[account(mut)]
    pub authority: Signer<'info>,

    #[account(
        has_one = authority @ AutoEmissionsError::InvalidAuthority
    )]
    pub protocol: Box<Account<'info, Protocol>>,

    /// CHECK: empty PDA, authority for token accounts
    #[account(
        seeds = [b"transfer_authority"],
        bump = protocol.transfer_authority_bump
    )]
    pub transfer_authority: AccountInfo<'info>,

    #[account(
        init,
        payer = authority,
        space = Group::LEN,
        seeds = [b"group",
                 params.project_name.as_bytes(),
                 params.group_name.as_bytes()],
        bump
    )]
    pub group: Box<Account<'info, Group>>,

    #[account(
        init,
        payer = authority,
        token::mint = mint,
        token::authority = transfer_authority,
        seeds = [b"custody",
                 group.key().as_ref()],
        bump
    )]
    pub custody: Box<Account<'info, TokenAccount>>,

    #[account()]
    pub mint: Box<Account<'info, Mint>>,

    system_program: Program<'info, System>,
    token_program: Program<'info, Token>,
}

#[derive(AnchorSerialize, AnchorDeserialize)]
pub struct AddGroupParams {
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
}

pub fn add_group(ctx: Context<AddGroup>, params: &AddGroupParams) -> Result<()> {
    let group = ctx.accounts.group.as_mut();

    group.project_name = params.project_name.clone();
    group.group_name = params.group_name.clone();
    group.group_authority = params.group_authority;

    group.allow_claims = params.allow_claims;
    group.allow_early_withdrawals = params.allow_early_withdrawals;

    group.initial_unlock_time = params.initial_unlock_time;
    group.initial_unlock_percent = params.initial_unlock_percent;
    group.unlock_frequency = params.unlock_frequency;
    group.unlock_count = params.unlock_count;
    group.claim_end_time = params.claim_end_time;

    group.custody = ctx.accounts.custody.key();
    group.mint = ctx.accounts.mint.key();
    group.mint_decimals = ctx.accounts.mint.decimals;

    group.claimed_amount = 0;

    group.participants = 0;
    group.allocation_percent = 0;

    group.inception_time = group.get_time()?;

    if !group.validate(group.get_time()?) {
        return err!(AutoEmissionsError::InvalidGroupConfig);
    }

    Ok(())
}
