//! Common utility functions.

#[cfg(not(feature = "test"))]
use crate::{error::AutoEmissionsError, program::AutoEmissions};
//
use {anchor_lang::prelude::*, anchor_spl::token::Transfer};

#[cfg(not(feature = "test"))]
pub fn validate_upgrade_authority(
    upgrade_authority: Pubkey,
    autoemissions_program_data: &AccountInfo,
    autoemissions_program: &AccountInfo,
) -> Result<()> {
    let program: Program<AutoEmissions> = Program::try_from(autoemissions_program)?;
    let program_data: Account<ProgramData> = Account::try_from(autoemissions_program_data)?;

    // should be also checked in Program::try_from()
    if autoemissions_program.owner != &crate::ID {
        return Err(Error::from(ErrorCode::AccountOwnedByWrongProgram)
            .with_pubkeys((*autoemissions_program.owner, crate::ID)));
    }

    require!(
        program.programdata_address()? == Some(program_data.key())
            && program_data.upgrade_authority_address == Some(upgrade_authority),
        AutoEmissionsError::InvalidAuthority
    );

    Ok(())
}

#[cfg(feature = "test")]
pub fn validate_upgrade_authority(
    _authority: Pubkey,
    _autoemissions_program_data: &AccountInfo,
    _autoemissions_program: &AccountInfo,
) -> Result<()> {
    Ok(())
}

pub fn transfer_tokens<'info>(
    from: AccountInfo<'info>,
    to: AccountInfo<'info>,
    authority: AccountInfo<'info>,
    token_program: AccountInfo<'info>,
    transfer_authority_bump: u8,
    amount: u64,
) -> Result<()> {
    let authority_seeds: &[&[&[u8]]] = &[&[b"transfer_authority", &[transfer_authority_bump]]];

    let context = CpiContext::new(
        token_program,
        Transfer {
            from,
            to,
            authority,
        },
    )
    .with_signer(authority_seeds);

    anchor_spl::token::transfer(context, amount)
}

pub fn transfer_tokens_from_user<'info>(
    from: AccountInfo<'info>,
    to: AccountInfo<'info>,
    authority: AccountInfo<'info>,
    token_program: AccountInfo<'info>,
    amount: u64,
) -> Result<()> {
    let context = CpiContext::new(
        token_program,
        Transfer {
            from,
            to,
            authority,
        },
    );
    anchor_spl::token::transfer(context, amount)
}

pub fn close_token_account<'info>(
    receiver: AccountInfo<'info>,
    token_account: AccountInfo<'info>,
    token_program: AccountInfo<'info>,
    authority: AccountInfo<'info>,
    transfer_authority_bump: u8,
) -> Result<()> {
    let authority_seeds: &[&[&[u8]]] = &[&[b"transfer_authority", &[transfer_authority_bump]]];

    let cpi_accounts = anchor_spl::token::CloseAccount {
        account: token_account,
        destination: receiver,
        authority,
    };
    let cpi_context = anchor_lang::context::CpiContext::new(token_program, cpi_accounts);

    anchor_spl::token::close_account(cpi_context.with_signer(authority_seeds))
}
