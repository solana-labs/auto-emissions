//! SetAuthority instruction handler

use {
    crate::{error::AutoEmissionsError, program::AutoEmissions, state::protocol::Protocol, utils},
    anchor_lang::prelude::*,
};

#[derive(Accounts)]
pub struct SetAuthority<'info> {
    #[account()]
    pub authority: Signer<'info>,

    #[account(mut)]
    pub protocol: Box<Account<'info, Protocol>>,

    /// CHECK: ProgramData account, doesn't work in tests
    #[account()]
    pub autoemissions_program_data: AccountInfo<'info /*, ProgramData*/>,

    autoemissions_program: Program<'info, AutoEmissions>,
}

#[derive(AnchorSerialize, AnchorDeserialize)]
pub struct SetAuthorityParams {
    pub new_authority: Pubkey,
}

pub fn set_authority(ctx: Context<SetAuthority>, params: &SetAuthorityParams) -> Result<()> {
    let protocol = ctx.accounts.protocol.as_mut();

    // allow to set new authority by protocol authority or program's upgrade authority
    // the latter is needed in case protocol authority was mistakenly set to a wrong address
    if ctx.accounts.authority.key() != protocol.authority {
        utils::validate_upgrade_authority::<AutoEmissions>(
            ctx.accounts.authority.key(),
            &ctx.accounts.autoemissions_program_data.to_account_info(),
            &ctx.accounts.autoemissions_program.to_account_info(),
        )?;
    }

    protocol.authority = params.new_authority;
    if !protocol.validate() {
        return err!(AutoEmissionsError::InvalidProtocolConfig);
    }

    Ok(())
}
