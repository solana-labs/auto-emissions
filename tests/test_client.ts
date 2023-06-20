import * as anchor from "@coral-xyz/anchor";
import { AutoEmissions } from "../target/types/auto_emissions";
import {
  PublicKey,
  Keypair,
  SystemProgram,
  AccountMeta,
  SYSVAR_RENT_PUBKEY,
} from "@solana/web3.js";
import * as spl from "@solana/spl-token";
import BN from "bn.js";

export class TestClient {
  authority: Keypair;
  provider: anchor.AnchorProvider;
  program: anchor.Program<AutoEmissions>;
  printErrors: boolean;

  transferAuthority: { publicKey: PublicKey; bump: number };
  protocol: { publicKey: PublicKey; bump: number };
  group: {
    authority: Keypair;
    groupAccount: PublicKey;
    custodyAccount: PublicKey;
    mint: Keypair;
    decimals: number;
  };
  fundingAccount: PublicKey;

  users: {
    wallet: Keypair;
    tokenAccount: PublicKey;
    participantAccount: PublicKey;
  }[];

  constructor() {
    this.provider = anchor.AnchorProvider.env();
    anchor.setProvider(this.provider);
    this.program = anchor.workspace
      .AutoEmissions as anchor.Program<AutoEmissions>;
    this.printErrors = true;

    anchor.BN.prototype.toJSON = function () {
      return this.toString(10);
    };
  }

  initFixture = async () => {
    this.authority = Keypair.generate();
    this.group = this.generateGroup();
    await this.requestAirdrop(this.group.authority.publicKey);
    await this.confirmTx(await this.requestAirdrop(this.authority.publicKey));

    // pdas
    this.transferAuthority = this.findProgramAddress("transfer_authority");
    this.protocol = this.findProgramAddress("protocol");

    // create mint
    await spl.createMint(
      this.provider.connection,
      this.group.authority,
      this.group.authority.publicKey,
      null,
      this.group.decimals,
      this.group.mint
    );

    this.fundingAccount = await spl.createAssociatedTokenAccount(
      this.provider.connection,
      this.group.authority,
      this.group.mint.publicKey,
      this.group.authority.publicKey
    );

    await this.mintTokens(
      1000,
      this.group.decimals,
      this.group.mint.publicKey,
      this.fundingAccount
    );

    // users
    this.users = [];
    for (let i = 0; i < 2; ++i) {
      let wallet = Keypair.generate();
      await this.requestAirdrop(wallet.publicKey);

      let tokenAccount = await spl.createAssociatedTokenAccount(
        this.provider.connection,
        this.authority,
        this.group.mint.publicKey,
        wallet.publicKey
      );

      let participantAccount = this.findProgramAddress("participant", [
        this.group.groupAccount,
        wallet.publicKey,
      ]).publicKey;

      this.users.push({
        wallet,
        tokenAccount,
        participantAccount,
      });
    }
  };

  requestAirdrop = async (pubkey: PublicKey) => {
    if ((await this.getSolBalance(pubkey)) < 1e9 / 2) {
      return this.provider.connection.requestAirdrop(pubkey, 1e9);
    }
  };

  mintTokens = async (
    uiAmount: number,
    decimals: number,
    mint: PublicKey,
    destiantionWallet: PublicKey
  ) => {
    await spl.mintToChecked(
      this.provider.connection,
      this.group.authority,
      mint,
      destiantionWallet,
      this.group.authority,
      this.toTokenAmount(uiAmount, decimals).toNumber(),
      decimals
    );
  };

  generateGroup = (decimals: number) => {
    let authority = Keypair.generate();
    let mint = Keypair.generate();
    let groupAccount = this.findProgramAddress("group", [
      "test project",
      "test group",
    ]).publicKey;
    let custodyAccount = this.findProgramAddress("custody", [
      groupAccount,
    ]).publicKey;

    return {
      authority,
      groupAccount,
      custodyAccount,
      mint,
      decimals,
    };
  };

  findProgramAddress = (label: string, extraSeeds = null) => {
    let seeds = [Buffer.from(anchor.utils.bytes.utf8.encode(label))];
    if (extraSeeds) {
      for (let extraSeed of extraSeeds) {
        if (typeof extraSeed === "string") {
          seeds.push(Buffer.from(anchor.utils.bytes.utf8.encode(extraSeed)));
        } else if (Array.isArray(extraSeed)) {
          seeds.push(Buffer.from(extraSeed));
        } else {
          seeds.push(extraSeed.toBuffer());
        }
      }
    }
    let res = PublicKey.findProgramAddressSync(seeds, this.program.programId);
    return { publicKey: res[0], bump: res[1] };
  };

  confirmTx = async (txSignature: anchor.web3.TransactionSignature) => {
    const latestBlockHash = await this.provider.connection.getLatestBlockhash();

    await this.provider.connection.confirmTransaction(
      {
        blockhash: latestBlockHash.blockhash,
        lastValidBlockHeight: latestBlockHash.lastValidBlockHeight,
        signature: txSignature,
      },
      { commitment: "processed" }
    );
  };

  confirmAndLogTx = async (txSignature: anchor.web3.TransactionSignature) => {
    await this.confirmTx(txSignature);
    let tx = await this.provider.connection.getTransaction(txSignature, {
      commitment: "confirmed",
    });
    console.log(tx);
  };

  getBalance = async (pubkey: PublicKey) => {
    return spl
      .getAccount(this.provider.connection, pubkey)
      .then((account) => Number(account.amount))
      .catch(() => 0);
  };

  getSolBalance = async (pubkey: PublicKey) => {
    return this.provider.connection
      .getBalance(pubkey)
      .then((balance) => balance)
      .catch(() => 0);
  };

  getExtraSolBalance = async (pubkey: PublicKey) => {
    let balance = await this.provider.connection
      .getBalance(pubkey)
      .then((balance) => balance)
      .catch(() => 0);
    let accountInfo = await this.provider.connection.getAccountInfo(pubkey);
    let dataSize = accountInfo ? accountInfo.data.length : 0;
    let minBalance =
      await this.provider.connection.getMinimumBalanceForRentExemption(
        dataSize
      );
    return balance > minBalance ? balance - minBalance : 0;
  };

  getTokenAccount = async (pubkey: PublicKey) => {
    return spl.getAccount(this.provider.connection, pubkey);
  };

  getTime() {
    const now = new Date();
    const utcMilllisecondsSinceEpoch =
      now.getTime() + now.getTimezoneOffset() * 60 * 1000;
    return utcMilllisecondsSinceEpoch / 1000;
  }

  toTokenAmount(uiAmount: number, decimals: number) {
    return new BN(uiAmount * 10 ** decimals);
  }

  toUiAmount(token_amount: number, decimals: number) {
    return token_amount / 10 ** decimals;
  }

  ensureFails = async (promise, message = null) => {
    let printErrors = this.printErrors;
    this.printErrors = false;
    let res = null;
    try {
      await promise;
    } catch (err) {
      res = err;
    }
    this.printErrors = printErrors;
    if (!res) {
      throw new Error(message ? message : "Call should've failed");
    }
    return res;
  };

  ///////
  // instructions

  init = async () => {
    try {
      let programData = PublicKey.findProgramAddressSync(
        [this.program.programId.toBuffer()],
        new PublicKey("BPFLoaderUpgradeab1e11111111111111111111111")
      )[0];

      await this.program.methods
        .init({
          authority: this.authority.publicKey,
          allowClaims: true,
          allowEarlyWithdrawals: true,
          allowGroupAuthorities: true,
        })
        .accounts({
          upgradeAuthority: this.provider.wallet.publicKey,
          protocol: this.protocol.publicKey,
          transferAuthority: this.transferAuthority.publicKey,
          autoemissionsProgramData: programData,
          autoemissionsProgram: this.program.programId,
          systemProgram: SystemProgram.programId,
        })
        .rpc();
    } catch (err) {
      if (this.printErrors) {
        console.log(err);
      }
      throw err;
    }
  };

  setAuthority = async (newAuthority: PublicKey) => {
    try {
      let programData = PublicKey.findProgramAddressSync(
        [this.program.programId.toBuffer()],
        new PublicKey("BPFLoaderUpgradeab1e11111111111111111111111")
      )[0];

      await this.program.methods
        .setAuthority({
          newAuthority,
        })
        .accounts({
          authority: this.authority.publicKey,
          protocol: this.protocol.publicKey,
          autoemissionsProgramData: programData,
          autoemissionsProgram: this.program.programId,
        })
        .signers([this.authority])
        .rpc();
    } catch (err) {
      if (this.printErrors) {
        console.log(err);
      }
      throw err;
    }
  };

  setTestTime = async (time: BN) => {
    try {
      await this.program.methods
        .setTestTime({ time })
        .accounts({
          authority: this.authority.publicKey,
          protocol: this.protocol.publicKey,
          group: this.group.groupAccount,
        })
        .signers([this.authority])
        .rpc();
    } catch (err) {
      if (this.printErrors) {
        console.log(err);
      }
      throw err;
    }
  };

  addGroup = async (params) => {
    try {
      await this.program.methods
        .addGroup(params)
        .accounts({
          authority: this.authority.publicKey,
          protocol: this.protocol.publicKey,
          transferAuthority: this.transferAuthority.publicKey,
          group: this.group.groupAccount,
          custody: this.group.custodyAccount,
          mint: this.group.mint.publicKey,
          systemProgram: SystemProgram.programId,
          tokenProgram: spl.TOKEN_PROGRAM_ID,
        })
        .signers([this.authority])
        .rpc();
    } catch (err) {
      if (this.printErrors) {
        console.log(err);
      }
      throw err;
    }
  };

  addParticipant = async (params, user) => {
    try {
      await this.program.methods
        .addParticipant(params)
        .accounts({
          authority: this.group.authority.publicKey,
          protocol: this.protocol.publicKey,
          group: this.group.groupAccount,
          participant: user.participantAccount,
          systemProgram: SystemProgram.programId,
        })
        .signers([this.group.authority])
        .rpc();
    } catch (err) {
      if (this.printErrors) {
        console.log(err);
      }
      throw err;
    }
  };

  depositTokens = async (amount: BN, fundingAccount: PublicKey) => {
    try {
      await this.program.methods
        .depositTokens({ amount })
        .accounts({
          owner: this.group.authority.publicKey,
          fundingAccount,
          group: this.group.groupAccount,
          custody: this.group.custodyAccount,
          tokenProgram: spl.TOKEN_PROGRAM_ID,
        })
        .signers([this.group.authority])
        .rpc();
    } catch (err) {
      if (this.printErrors) {
        console.log(err);
      }
      throw err;
    }
  };

  claimTokens = async (maxAmount: BN, user) => {
    try {
      await this.program.methods
        .claimTokens({ maxAmount })
        .accounts({
          owner: user.wallet.publicKey,
          receivingAccount: user.tokenAccount,
          protocol: this.protocol.publicKey,
          transferAuthority: this.transferAuthority.publicKey,
          group: this.group.groupAccount,
          custody: this.group.custodyAccount,
          participant: user.participantAccount,
          tokenProgram: spl.TOKEN_PROGRAM_ID,
        })
        .signers([user.wallet])
        .rpc();
    } catch (err) {
      if (this.printErrors) {
        console.log(err);
      }
      throw err;
    }
  };
}
