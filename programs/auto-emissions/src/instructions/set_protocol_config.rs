//! SetProtocolConfig instruction handler

use {
    crate::{error::AutoEmissionsError, state::protocol::Protocol},
    anchor_lang::prelude::*,
};

#[derive(Accounts)]
pub struct SetProtocolConfig<'info> {
    #[account()]
    pub authority: Signer<'info>,

    #[account(
        mut,
        has_one = authority @ AutoEmissionsError::InvalidAuthority
    )]
    pub protocol: Box<Account<'info, Protocol>>,
}

#[derive(AnchorSerialize, AnchorDeserialize)]
pub struct SetProtocolConfigParams {
    pub allow_claims: bool,
    pub allow_early_withdrawals: bool,
    pub allow_group_authorities: bool,
}

pub fn set_protocol_config(
    ctx: Context<SetProtocolConfig>,
    params: &SetProtocolConfigParams,
) -> Result<()> {
    let protocol = ctx.accounts.protocol.as_mut();

    protocol.allow_claims = params.allow_claims;
    protocol.allow_early_withdrawals = params.allow_early_withdrawals;
    protocol.allow_group_authorities = params.allow_group_authorities;

    if !protocol.validate() {
        return err!(AutoEmissionsError::InvalidProtocolConfig);
    }

    Ok(())
}
