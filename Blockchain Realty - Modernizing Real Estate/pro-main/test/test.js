const LandRegistry = artifacts.require("./src/contracts/LandRegistry.sol");


contract("LandRegistry", async (accounts) => {
    let landRegistryInstance;

    before(async () => {
        landRegistryInstance = await LandRegistry.deployed();
    });

    it("should deploy the LandRegistry contract", async () => {
        assert(landRegistryInstance.address !== '', "contract address should be present");
    });

    it("should add a user", async () => {
       
        const result = await landRegistryInstance.addUser(
            
            accounts[0],          
            "Jacob Mathew",           
            1234567890,           
            "jacob@example.com",   
            12345,                
            "Kochi"            
        );
      
        assert.exists(result.receipt, "User addition failed");

        const user = await landRegistryInstance.getUser(accounts[0]);
        assert.equal(user[1], "Jacob Mathew", "User name does not match");
        assert.equal(user[2], 1234567890, "User contact does not match");
        assert.equal(user[3], "jacob@example.com", "User email does not match");
        assert.equal(user[4], 12345, "User postal code does not match");
        assert.equal(user[5], "Kochi", "User city does not match");
        assert.isTrue(user[6], "User existence flag is not true");
    });

    it("should register land", async () => {
        const result = await landRegistryInstance.Registration(
            accounts[0],         
            "ipfs_hash",          
            "123 Main Road",        
            10000,                
            1,                    
            "Approved",           
            "Available"           
        );
      
        assert.exists(result.receipt, "Land Registration failed");
        const land = await landRegistryInstance.landInfoOwner(1);
        assert.equal(land[0], accounts[0], "Land owner address does not match");
        assert.equal(land[1], "ipfs_hash", "Land IPFS hash does not match");
        assert.equal(land[2], 10000, "Land amount does not match");
        assert.equal(land[3], "Approved", "Govt approval status does not match");
        assert.equal(land[4], "Available", "Land availability status does not match");
        assert.equal(land[5], 0, "Land requester address should be zero");
        assert.equal(land[6], 0, "Land request status should be Default");
    });

    it("should update land IPFS hash", async () => {
        await landRegistryInstance.updateIPFSHash(1, "new_ipfs_hash", { from: accounts[0] });
        const updatedLand = await landRegistryInstance.landInfoOwner(1);
        assert.equal(updatedLand[1], "new_ipfs_hash", "Land IPFS hash update failed");
    });

    it("should process land request", async () => {
        await landRegistryInstance.requstToLandOwner(1, { from: accounts[1] });

        const land = await landRegistryInstance.landInfoOwner(1);
        assert.equal(land[5], accounts[1], "Land requester address does not match");
        assert.equal(land[4], "Pending", "Land availability status should be Pending");

        await landRegistryInstance.processRequest(1, 2, { from: accounts[0] });

        const updatedLand = await landRegistryInstance.landInfoOwner(1);
     
        assert.equal(updatedLand[5], 0, "Land requester address should be reset");
        assert.equal(updatedLand[3], "Approved", "Land request status should be Approved");
        assert.equal(updatedLand[3], "Approved", "Land availability status should be Approved");
    });

    it("should make land available for purchase", async () => {
        await landRegistryInstance.makeAvailable(1, { from: accounts[0] });
        const updatedLand = await landRegistryInstance.landInfoOwner(1);
        assert.equal(updatedLand[4], "Available", "Land availability status should be Available");
    });

    it("should buy a property", async () => {
      const buyerBalanceBefore = await web3.eth.getBalance(accounts[1]);
        const amount = 10000 * 10000000000000; 
        const samount = amount.toString();
        await landRegistryInstance.buyProperty(1, { from: accounts[1], value: samount })
        const buyerBalanceAfter = await web3.eth.getBalance(accounts[1]);
        const updatedLandDetails = await landRegistryInstance.landInfoOwner(1);
       const difference = Number(buyerBalanceBefore) - Number(buyerBalanceAfter);
        assert.isAtLeast(difference, amount, "Buyer balance should decrease by at least the purchase amount");
         assert.equal(updatedLandDetails[0], accounts[1], "Land owner address does not match after purchase");
        assert.equal(updatedLandDetails[4], "Not yet approved by the govt.", "Land availability status should be Not yet approved by the govt.");
    });
    

    it("should update government status", async () => {
        await landRegistryInstance.govtStatus(1, "Rejected", "Not Available");
        const updatedLand = await landRegistryInstance.landInfoOwner(1);
        assert.equal(updatedLand[3], "Rejected", "Govt approval status update failed");
        assert.equal(updatedLand[4], "Not Available", "Land availability status update failed");
    });
});
