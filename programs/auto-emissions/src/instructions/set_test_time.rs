//! SetTestTime instruction handler

use {
    crate::{
        error::AutoEmissionsError,
        state::{group::Group, protocol::Protocol},
    },
    anchor_lang::prelude::*,
};

#[derive(Accounts)]
pub struct SetTestTime<'info> {
    #[account(mut)]
    pub authority: Signer<'info>,

    #[account(
        has_one = authority @ AutoEmissionsError::InvalidAuthority
    )]
    pub protocol: Box<Account<'info, Protocol>>,

    #[account(mut)]
    pub group: Box<Account<'info, Group>>,
}

#[derive(AnchorSerialize, AnchorDeserialize)]
pub struct SetTestTimeParams {
    pub time: u64,
}

pub fn set_test_time(ctx: Context<SetTestTime>, params: &SetTestTimeParams) -> Result<()> {
    if !cfg!(feature = "test") {
        return err!(AutoEmissionsError::InvalidEnvironment);
    }

    ctx.accounts.group.inception_time = params.time;

    Ok(())
}
