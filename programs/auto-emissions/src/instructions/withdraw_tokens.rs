//! WithdrawTokens instruction handler

use {
    crate::{
        error::AutoEmissionsError,
        state::{group::Group, protocol::Protocol},
        utils,
    },
    anchor_lang::prelude::*,
    anchor_spl::token::{Token, TokenAccount},
};

#[derive(Accounts)]
pub struct WithdrawTokens<'info> {
    #[account()]
    pub authority: Signer<'info>,

    #[account(
        mut,
        constraint = receiving_account.mint == group.mint,
        constraint = receiving_account.owner == authority.key()
    )]
    pub receiving_account: Box<Account<'info, TokenAccount>>,

    /// CHECK: empty PDA, authority for token accounts
    #[account(
        seeds = [b"transfer_authority"],
        bump = protocol.transfer_authority_bump
    )]
    pub transfer_authority: AccountInfo<'info>,

    #[account()]
    pub protocol: Box<Account<'info, Protocol>>,

    #[account(
        has_one = custody @ AutoEmissionsError::InvalidCustodyAddress
    )]
    pub group: Box<Account<'info, Group>>,

    #[account(mut)]
    pub custody: Box<Account<'info, TokenAccount>>,

    token_program: Program<'info, Token>,
}

#[derive(AnchorSerialize, AnchorDeserialize)]
pub struct WithdrawTokensParams {
    pub amount: u64,
}

pub fn withdraw_tokens(ctx: Context<WithdrawTokens>, params: &WithdrawTokensParams) -> Result<()> {
    let group = ctx.accounts.group.as_mut();

    require!(
        ctx.accounts.protocol.authority == ctx.accounts.authority.key()
            || (ctx.accounts.protocol.allow_group_authorities
                && group.group_authority == ctx.accounts.authority.key()),
        AutoEmissionsError::InvalidAuthority
    );

    require!(
        group.is_expired(group.get_time()?)
            || (ctx.accounts.protocol.allow_early_withdrawals && group.allow_early_withdrawals),
        AutoEmissionsError::InstructionNotAllowed
    );

    utils::transfer_tokens(
        ctx.accounts.custody.to_account_info(),
        ctx.accounts.receiving_account.to_account_info(),
        ctx.accounts.transfer_authority.to_account_info(),
        ctx.accounts.token_program.to_account_info(),
        ctx.accounts.protocol.transfer_authority_bump,
        params.amount,
    )?;

    Ok(())
}
