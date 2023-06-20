//! RemoveGroup instruction handler

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
pub struct RemoveGroup<'info> {
    #[account()]
    pub authority: Signer<'info>,

    #[account(
        mut,
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
        mut,
        has_one = custody @ AutoEmissionsError::InvalidCustodyAddress,
        close = authority
    )]
    pub group: Box<Account<'info, Group>>,

    #[account(mut)]
    pub custody: Box<Account<'info, TokenAccount>>,

    token_program: Program<'info, Token>,
}

#[derive(AnchorSerialize, AnchorDeserialize)]
pub struct RemoveGroupParams {}

pub fn remove_group(ctx: Context<RemoveGroup>, _params: &RemoveGroupParams) -> Result<()> {
    require!(
        ctx.accounts.group.participants == 0 && ctx.accounts.custody.amount == 0,
        AutoEmissionsError::InvalidGroupState
    );

    utils::close_token_account(
        ctx.accounts.authority.to_account_info(),
        ctx.accounts.custody.to_account_info(),
        ctx.accounts.token_program.to_account_info(),
        ctx.accounts.transfer_authority.to_account_info(),
        ctx.accounts.protocol.transfer_authority_bump,
    )?;

    Ok(())
}
