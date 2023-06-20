//! GetUnlockedAmount instruction handler

use {
    crate::{error::AutoEmissionsError, state::group::Group},
    anchor_lang::prelude::*,
    anchor_spl::token::TokenAccount,
};

#[derive(Accounts)]
pub struct GetUnlockedAmount<'info> {
    #[account(
        has_one = custody @ AutoEmissionsError::InvalidCustodyAddress
    )]
    pub group: Box<Account<'info, Group>>,

    #[account()]
    pub custody: Box<Account<'info, TokenAccount>>,
}

#[derive(AnchorSerialize, AnchorDeserialize)]
pub struct GetUnlockedAmountParams {
    time: u64,
}

pub fn get_unlocked_amount(
    ctx: Context<GetUnlockedAmount>,
    params: &GetUnlockedAmountParams,
) -> Result<u64> {
    ctx.accounts.group.get_unlocked_amount(
        ctx.accounts.custody.amount,
        if params.time > 0 {
            params.time
        } else {
            ctx.accounts.group.get_time()?
        },
    )
}
