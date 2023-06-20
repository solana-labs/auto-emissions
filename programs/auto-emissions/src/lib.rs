//! AutoEmissions program entrypoint

#![allow(clippy::result_large_err)]

pub mod constants;
pub mod error;
pub mod instructions;
pub mod math;
pub mod state;
pub mod utils;

use {anchor_lang::prelude::*, instructions::*};

solana_security_txt::security_txt! {
    name: "AutoEmissions",
    project_url: "https://github.com/solana-labs/auto-emissions",
    contacts: "email:defi@solana.com",
    policy: "",
    preferred_languages: "en",
    auditors: ""
}

declare_id!("Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS");

#[program]
pub mod auto_emissions {
    use super::*;

    // protocol admin instructions
    pub fn init(ctx: Context<Init>, params: InitParams) -> Result<()> {
        instructions::init(ctx, &params)
    }

    pub fn add_group(ctx: Context<AddGroup>, params: AddGroupParams) -> Result<()> {
        instructions::add_group(ctx, &params)
    }

    pub fn remove_group(ctx: Context<RemoveGroup>, params: RemoveGroupParams) -> Result<()> {
        instructions::remove_group(ctx, &params)
    }

    pub fn set_authority(ctx: Context<SetAuthority>, params: SetAuthorityParams) -> Result<()> {
        instructions::set_authority(ctx, &params)
    }

    pub fn set_group_config(
        ctx: Context<SetGroupConfig>,
        params: SetGroupConfigParams,
    ) -> Result<()> {
        instructions::set_group_config(ctx, &params)
    }

    pub fn set_protocol_config(
        ctx: Context<SetProtocolConfig>,
        params: SetProtocolConfigParams,
    ) -> Result<()> {
        instructions::set_protocol_config(ctx, &params)
    }

    pub fn set_test_time(ctx: Context<SetTestTime>, params: SetTestTimeParams) -> Result<()> {
        instructions::set_test_time(ctx, &params)
    }

    // group admin instructions (can also be executed by the protocol admin)
    pub fn add_participant(
        ctx: Context<AddParticipant>,
        params: AddParticipantParams,
    ) -> Result<()> {
        instructions::add_participant(ctx, &params)
    }

    pub fn deposit_tokens(ctx: Context<DepositTokens>, params: DepositTokensParams) -> Result<()> {
        instructions::deposit_tokens(ctx, &params)
    }

    pub fn remove_participant(
        ctx: Context<RemoveParticipant>,
        params: RemoveParticipantParams,
    ) -> Result<()> {
        instructions::remove_participant(ctx, &params)
    }

    pub fn set_participant_config(
        ctx: Context<SetParticipantConfig>,
        params: SetParticipantConfigParams,
    ) -> Result<()> {
        instructions::set_participant_config(ctx, &params)
    }

    pub fn withdraw_tokens(
        ctx: Context<WithdrawTokens>,
        params: WithdrawTokensParams,
    ) -> Result<()> {
        instructions::withdraw_tokens(ctx, &params)
    }

    // permissionless instructions
    pub fn get_unlocked_amount(
        ctx: Context<GetUnlockedAmount>,
        params: GetUnlockedAmountParams,
    ) -> Result<u64> {
        instructions::get_unlocked_amount(ctx, &params)
    }

    pub fn get_entitled_amount(
        ctx: Context<GetEntitledAmount>,
        params: GetEntitledAmountParams,
    ) -> Result<u64> {
        instructions::get_entitled_amount(ctx, &params)
    }

    // participant instructions
    pub fn claim_tokens(ctx: Context<ClaimTokens>, params: ClaimTokensParams) -> Result<()> {
        instructions::claim_tokens(ctx, &params)
    }
}
