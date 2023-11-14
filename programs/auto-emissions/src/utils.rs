//! Common utility functions.

use {anchor_lang::prelude::*, anchor_spl::token::Transfer};

pub fn validate_upgrade_authority<T: anchor_lang::Id>(
    expected_upgrade_authority: Pubkey,
    program_data: &AccountInfo,
    program: &AccountInfo,
) -> Result<()> {
    let program: Program<T> = Program::try_from(program)?;
    if let Some(programdata_address) = program.programdata_address()? {
        require_keys_eq!(
            programdata_address,
            program_data.key(),
            ErrorCode::InvalidProgramExecutable
        );
        let program_data: Account<ProgramData> = Account::try_from(program_data)?;
        if let Some(current_upgrade_authority) = program_data.upgrade_authority_address {
            if current_upgrade_authority != Pubkey::default() {
                require_keys_eq!(
                    current_upgrade_authority,
                    expected_upgrade_authority,
                    ErrorCode::ConstraintOwner
                );
            }
        }
    } // otherwise not upgradeable

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
