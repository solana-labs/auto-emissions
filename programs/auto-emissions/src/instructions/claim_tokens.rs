//! ClaimTokens instruction handler

use {
    crate::{
        error::AutoEmissionsError,
        state::{group::Group, participant::Participant, protocol::Protocol},
        utils,
    },
    anchor_lang::prelude::*,
    anchor_spl::token::{Token, TokenAccount},
};

#[derive(Accounts)]
pub struct ClaimTokens<'info> {
    #[account()]
    pub owner: Signer<'info>,

    #[account(
        mut,
        constraint = receiving_account.mint == group.mint,
        has_one = owner @ AutoEmissionsError::InvalidAuthority
    )]
    pub receiving_account: Box<Account<'info, TokenAccount>>,

    #[account()]
    pub protocol: Box<Account<'info, Protocol>>,

    /// CHECK: empty PDA, authority for token accounts
    #[account(
        seeds = [b"transfer_authority"],
        bump = protocol.transfer_authority_bump
    )]
    pub transfer_authority: AccountInfo<'info>,

    #[account(
        mut,
        has_one = custody @ AutoEmissionsError::InvalidCustodyAddress
    )]
    pub group: Box<Account<'info, Group>>,

    #[account(mut)]
    pub custody: Box<Account<'info, TokenAccount>>,

    #[account(
        mut,
        has_one = group @ AutoEmissionsError::InvalidGroupAddress,
        has_one = owner @ AutoEmissionsError::InvalidAuthority
    )]
    pub participant: Box<Account<'info, Participant>>,

    token_program: Program<'info, Token>,
}

#[derive(AnchorSerialize, AnchorDeserialize)]
pub struct ClaimTokensParams {
    pub max_amount: u64,
}

pub fn claim_tokens(ctx: Context<ClaimTokens>, params: &ClaimTokensParams) -> Result<()> {
    let group = ctx.accounts.group.as_mut();

    require!(
        ctx.accounts.protocol.allow_claims && group.allow_claims,
        AutoEmissionsError::InstructionNotAllowed
    );

    let entitled_amount = ctx.accounts.participant.get_entitled_amount(
        group.get_unlocked_amount(ctx.accounts.custody.amount, group.get_time()?)?,
    )?;
    let transfer_amount = std::cmp::min(entitled_amount, params.max_amount);

    utils::transfer_tokens(
        ctx.accounts.custody.to_account_info(),
        ctx.accounts.receiving_account.to_account_info(),
        ctx.accounts.transfer_authority.to_account_info(),
        ctx.accounts.token_program.to_account_info(),
        ctx.accounts.protocol.transfer_authority_bump,
        transfer_amount,
    )?;

    ctx.accounts.participant.claim_amount(transfer_amount)?;
    group.claim_amount(transfer_amount)?;

    Ok(())
}
