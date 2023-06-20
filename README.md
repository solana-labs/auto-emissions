# Solana Automatic Token Emissions

## Introduction

AutoEmissions is Carta for cryptocurrency projects. The product allows a user to manage their Token Emission Schedule and distribute token allocations to various individuals such as employees, advisors, and investors in an automated capacity.

## Quick start

### Setup Environment

1. Clone the repository from <https://github.com/solana-labs/auto-emissions.git>.
2. Install the latest Solana tools from <https://docs.solana.com/cli/install-solana-cli-tools>. If you already have Solana tools, run `solana-install update` to get the latest compatible version.
3. Install the latest Rust stable from <https://rustup.rs/>. If you already have Rust, run `rustup update` to get the latest version.
4. Install the latest Anchor framework from <https://www.anchor-lang.com/docs/installation>. If you already have Anchor, run `avm update` to get the latest version.

Rustfmt is used to format the code. It requires `nightly` features to be activated:

5. Install `nightly` rust toolchain. <https://rust-lang.github.io/rustup/installation/index.html#installing-nightly>
6. Execute `git config core.hooksPath .githooks` to activate pre-commit hooks.

#### [Optional] Vscode setup

1. Install `rust-analyzer` extension
2. If formatting doesn't work, make sure that `rust-analyzer.rustfmt.extraArgs` is set to `+nightly`

### Build

First, generate a new key for the program address with `solana-keygen new -o <PROG_ID_JSON>`. Then replace the existing program ID with the newly generated address in `Anchor.toml` and `programs/auto-emissions/src/lib.rs`.

Also, ensure the path to your wallet in `Anchor.toml` is correct. Alternatively, when running Anchor deploy or test commands, you can specify your wallet with `--provider.wallet` argument. The wallet's pubkey will be set as an upgrade authority upon initial deployment of the program. It is strongly recommended to make upgrade authority a multisig when deploying to the mainnet.

To build the program run `anchor build` command from the root `auto-emissions` directory:

```sh
cd auto-emissions
anchor build
```

### Test

Unit tests are executed with the `cargo test` command:

```sh
cargo test -- --nocapture
```

Integration tests can be started as follows:

```sh
npm install
anchor test -- --features test
```

By default, integration tests are executed on a local validator, so it won't cost you any SOL.

### Deploy

To deploy the program to the devnet and upload the IDL use the following commands:

```sh
anchor deploy --provider.cluster devnet --program-keypair <PROG_ID_JSON>
anchor idl init --provider.cluster devnet --filepath ./target/idl/auto_emissions.json <PROGRAM ID>
```

### Initialize

A small CLI Typescript client is included to help you initialize and manage the program. By default script uses devnet cluster. Add `-u https://api.mainnet-beta.solana.com` to all of the commands if you plan to execute them on mainnet.

To initialize deployed program, run the following commands:

```
npx ts-node app/cli.ts -k <ADMIN_WALLET> init <ADMIN_PUBKEY>
```

Where `<ADMIN_WALLET>` is the file path to the wallet that was set as the upgrade authority of the program upon deployment. `<ADMIN_PUBKEY>` will be set as protocol admin.

To change protocol admin, run:

```
npx ts-node app/cli.ts -k <ADMIN_WALLET> set-authority <ADMIN_PUBKEY>
```

To validate initialized program:

```
npx ts-node app/cli.ts -k <ADMIN_WALLET> get-protocol
```

For examples on how to create auto emission groups and add participants check integration tests under `test` directory.

To validate added groups and participants, run:

```
npx ts-node app/cli.ts -k <ADMIN_WALLET> get-groups <SCHEDULE_NAME>
npx ts-node app/cli.ts -k <ADMIN_WALLET> get-participants <GROUP_NAME>
```

You can list all of the available commands by running the following:

```
npx ts-node app/cli.ts --help
```

## Support

If you are experiencing technical difficulties while working with the AutoEmissions codebase, open an issue on [Github](https://github.com/solana-labs/auto-emissions/issues). For more general questions about programming on Solana blockchain use [StackExchange](https://solana.stackexchange.com).

If you find a bug in the code, you can raise an issue on [Github](https://github.com/solana-labs/auto-emissions/issues). But if this is a security issue, please don't disclose it on Github or in public channels. Send information to defi@solana.com instead.

## Contributing

Contributions are very welcome. Please refer to the [Contributing](https://github.com/solana-labs/solana/blob/master/CONTRIBUTING.md) guidelines for more information.

## License

Solana AutoEmissions codebase is released under [Apache License 2.0](LICENSE).

## Disclaimer

By accessing or using Solana AutoEmissions or any of its components, you accept and agree with the [Disclaimer](DISCLAIMER.md).
