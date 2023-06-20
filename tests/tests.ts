import * as anchor from "@coral-xyz/anchor";
import { TestClient } from "./test_client";
import { PublicKey } from "@solana/web3.js";
import { expect, assert } from "chai";
import BN from "bn.js";

describe("auto_emissions", () => {
  let tc = new TestClient();
  tc.printErrors = true;

  let protocolExpected;
  let groupExpected;
  let participantExpected;

  it("init", async () => {
    await tc.initFixture();
    await tc.init();

    let err = await tc.ensureFails(tc.init());
    assert(err.logs[3].includes("already in use"));

    protocolExpected = {
      authority: tc.authority.publicKey,
      allowClaims: true,
      allowEarlyWithdrawals: true,
      allowGroupAuthorities: true,
      transferAuthorityBump: tc.transferAuthority.bump,
    };

    let protocol = await tc.program.account.protocol.fetch(
      tc.protocol.publicKey
    );
    expect(JSON.stringify(protocol)).to.equal(JSON.stringify(protocolExpected));
  });

  it("setAuthority", async () => {
    await tc.setAuthority(tc.provider.wallet.publicKey);

    protocolExpected = {
      authority: tc.provider.wallet.publicKey,
      allowClaims: true,
      allowEarlyWithdrawals: true,
      allowGroupAuthorities: true,
      transferAuthorityBump: tc.transferAuthority.bump,
    };

    let protocol = await tc.program.account.protocol.fetch(
      tc.protocol.publicKey
    );
    expect(JSON.stringify(protocol)).to.equal(JSON.stringify(protocolExpected));

    // reset back to tc.authority
    await tc.setAuthority(tc.authority.publicKey);

    protocolExpected.authority = tc.authority.publicKey;
    protocol = await tc.program.account.protocol.fetch(tc.protocol.publicKey);
    expect(JSON.stringify(protocol)).to.equal(JSON.stringify(protocolExpected));
  });

  it("addGroup", async () => {
    let params = {
      projectName: "test project",
      groupName: "test group",
      groupAuthority: tc.group.authority.publicKey,
      allowClaims: true,
      allowEarlyWithdrawals: true,
      initialUnlockTime: new BN(100),
      initialUnlockPercent: new BN(1000),
      unlockFrequency: new BN(10),
      unlockCount: new BN(3),
      claimEndTime: new BN(300),
    };

    await tc.addGroup(params);

    groupExpected = {
      projectName: "test project",
      groupName: "test group",
      groupAuthority: tc.group.authority.publicKey,
      allowClaims: true,
      allowEarlyWithdrawals: true,
      initialUnlockTime: "100",
      initialUnlockPercent: "1000",
      unlockFrequency: "10",
      unlockCount: "3",
      claimEndTime: "300",
      custody: tc.group.custodyAccount,
      mint: tc.group.mint.publicKey,
      mintDecimals: 0,
      claimedAmount: "0",
      participants: "0",
      allocationPercent: "0",
      inceptionTime: "0",
    };

    let group = await tc.program.account.group.fetch(tc.group.groupAccount);
    expect(JSON.stringify(group)).to.equal(JSON.stringify(groupExpected));
  });

  it("setTestTime", async () => {
    await tc.setTestTime(new BN(50));

    groupExpected.inceptionTime = "50";
    let group = await tc.program.account.group.fetch(tc.group.groupAccount);
    expect(JSON.stringify(group)).to.equal(JSON.stringify(groupExpected));
  });

  it("addParticipant", async () => {
    let params = {
      owner: tc.users[0].wallet.publicKey,
      allocationPercent: new BN(5000),
    };

    await tc.addParticipant(params, tc.users[0]);

    participantExpected = {
      group: tc.group.groupAccount,
      owner: tc.users[0].wallet.publicKey,
      allocationPercent: "5000",
      claimedAmount: "0",
    };

    let participant = await tc.program.account.participant.fetch(
      tc.users[0].participantAccount
    );
    expect(JSON.stringify(participant)).to.equal(
      JSON.stringify(participantExpected)
    );
  });

  it("claimTokens", async () => {
    await tc.claimTokens(new BN(100000), tc.users[0]);

    participantExpected.claimedAmount = new BN(0);

    let participant = await tc.program.account.participant.fetch(
      tc.users[0].participantAccount
    );
    expect(JSON.stringify(participant)).to.equal(
      JSON.stringify(participantExpected)
    );
  });
});
