//! Protocol's global state.

use anchor_lang::prelude::*;

#[account]
#[derive(Default, Debug, PartialEq)]
pub struct Protocol {
    pub authority: Pubkey,
    pub allow_claims: bool,
    pub allow_early_withdrawals: bool,
    pub allow_group_authorities: bool,

    pub transfer_authority_bump: u8,
}

impl Protocol {
    pub const LEN: usize = 8 + std::mem::size_of::<Protocol>();

    pub fn validate(&self) -> bool {
        self.authority != Pubkey::default()
    }
}
