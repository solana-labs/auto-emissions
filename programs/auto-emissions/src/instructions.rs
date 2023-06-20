// protocol admin instructions
pub mod add_group;
pub mod init;
pub mod remove_group;
pub mod set_authority;
pub mod set_group_config;
pub mod set_protocol_config;
pub mod set_test_time;

// group admin instructions (can also be executed by the protocol admin)
pub mod add_participant;
pub mod remove_participant;
pub mod set_participant_config;
pub mod withdraw_tokens;

// permissionless instructions
pub mod deposit_tokens;
pub mod get_entitled_amount;
pub mod get_unlocked_amount;

// participant instructions
pub mod claim_tokens;

// bring everything in scope
pub use {
    add_group::*, add_participant::*, claim_tokens::*, deposit_tokens::*, get_entitled_amount::*,
    get_unlocked_amount::*, init::*, remove_group::*, remove_participant::*, set_authority::*,
    set_group_config::*, set_participant_config::*, set_protocol_config::*, set_test_time::*,
    withdraw_tokens::*,
};
