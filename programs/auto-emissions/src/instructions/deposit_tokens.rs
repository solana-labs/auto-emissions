//! DepositTokens instruction handler

use {
    crate::{error::AutoEmissionsError, state::group::Group, utils},
    anchor_lang::prelude::*,
    anchor_spl::token::{Token, TokenAccount},
};

#[derive(Accounts)]
pub struct DepositTokens<'info> {
    #[account()]
    pub owner: Signer<'info>,

    #[account(
        mut,
        constraint = funding_account.mint == group.mint,
        has_one = owner @ AutoEmissionsError::InvalidAuthority
    )]
    pub funding_account: Box<Account<'info, TokenAccount>>,

    #[account(
        has_one = custody @ AutoEmissionsError::InvalidCustodyAddress
    )]
    pub group: Box<Account<'info, Group>>,

    #[account(mut)]
    pub custody: Box<Account<'info, TokenAccount>>,

    token_program: Program<'info, Token>,
}

#[derive(AnchorSerialize, AnchorDeserialize)]
pub struct DepositTokensParams {
    pub amount: u64,
}

pub fn deposit_tokens(ctx: Context<DepositTokens>, params: &DepositTokensParams) -> Result<()> {
    utils::transfer_tokens_from_user(
        ctx.accounts.funding_account.to_account_info(),
        ctx.accounts.custody.to_account_info(),
        ctx.accounts.owner.to_account_info(),
        ctx.accounts.token_program.to_account_info(),
        params.amount,
    )?;

    Ok(())
}
