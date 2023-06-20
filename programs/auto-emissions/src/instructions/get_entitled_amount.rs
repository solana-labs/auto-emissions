//! GetEntitledAmount instruction handler

use {
    crate::{
        error::AutoEmissionsError,
        state::{group::Group, participant::Participant},
    },
    anchor_lang::prelude::*,
    anchor_spl::token::TokenAccount,
};

#[derive(Accounts)]
pub struct GetEntitledAmount<'info> {
    #[account(
        has_one = custody @ AutoEmissionsError::InvalidCustodyAddress
    )]
    pub group: Box<Account<'info, Group>>,

    #[account()]
    pub custody: Box<Account<'info, TokenAccount>>,

    #[account(
        has_one = group @ AutoEmissionsError::InvalidGroupAddress,
    )]
    pub participant: Box<Account<'info, Participant>>,
}

#[derive(AnchorSerialize, AnchorDeserialize)]
pub struct GetEntitledAmountParams {
    time: u64,
}

pub fn get_entitled_amount(
    ctx: Context<GetEntitledAmount>,
    params: &GetEntitledAmountParams,
) -> Result<u64> {
    ctx.accounts
        .participant
        .get_entitled_amount(ctx.accounts.group.get_unlocked_amount(
            ctx.accounts.custody.amount,
            if params.time > 0 {
                params.time
            } else {
                ctx.accounts.group.get_time()?
            },
        )?)
}
