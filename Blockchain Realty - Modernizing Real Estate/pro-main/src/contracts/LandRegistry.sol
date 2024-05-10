pragma solidity ^0.5.0;

contract LandRegistry {
    struct Task {
        uint256 id;
        string content;
        bool completed;
    }
    struct user {
        address userid;
        string uname;
        uint256 ucontact;
        string uemail;
        uint256 upostalCode;
        string city;
        bool exist;
    }
    struct landDetails {
        address payable id;
        string ipfsHash;
        string laddress;
        uint256 lamount;
        uint256 key;
        string isGovtApproved;
        string isAvailable;
        address requester;
        string rejectionReason;
       
        reqStatus requestStatus;
    }

    address[] userarr;
    uint256[] assets;
    address owner;
    enum reqStatus {Default, Pending, Rejected, Approved}

    constructor() public {
        owner = msg.sender;
    }

    struct profiles {
        uint256[] assetList;
    }

    mapping(address => profiles) profile;

    mapping(address => user) public users;
    mapping(uint256 => landDetails) public land;

    function addUser(
        address uid,
        string memory _uname,
        uint256 _ucontact,
        string memory _uemail,
        uint256 _ucode,
        string memory _ucity
    ) public returns (bool) {
        users[uid] = user(
            uid,
            _uname,
            _ucontact,
            _uemail,
            _ucode,
            _ucity,
            true
        );
        userarr.push(uid);
        return true;
    }

    function getUser(address uid)
        public
        view
        returns (
            address,
            string memory,
            uint256,
            string memory,
            uint256,
            string memory,
            bool
        )
    {
        if (users[uid].exist)
            return (
                users[uid].userid,
                users[uid].uname,
                users[uid].ucontact,
                users[uid].uemail,
                users[uid].upostalCode,
                users[uid].city,
                users[uid].exist
            );
    }

    function Registration(
        address payable _id,
        string memory _ipfsHash,
        string memory _laddress,
        uint256 _lamount,
        uint256 _key,
        string memory status,
        string memory _isAvailable
    ) public returns (bool) {
        land[_key] = landDetails(
            _id,
            _ipfsHash,
            _laddress,
            _lamount,
            _key,
            status,
            _isAvailable,
            0x0000000000000000000000000000000000000000,
            reqStatus.Default
        );
        profile[_id].assetList.push(_key);
        assets.push(_key);
        return true;
    }

    function computeId(string memory _laddress, string memory _lamount)
        public
        view
        returns (uint256)
    {
        return
            uint256(keccak256(abi.encodePacked(_laddress, _lamount))) %
            10000000000000;
    }

    function viewAssets() public view returns (uint256[] memory) {
        return (profile[msg.sender].assetList);
    }

    function Assets() public view returns (uint256[] memory) {
        return assets;
    }

    function landInfoOwner(uint256 id)
        public
        view
        returns (
            address payable,
            string memory,
            uint256,
            string memory,
            string memory,
            address,
            reqStatus
        )
    {
        return (
            land[id].id,
            land[id].ipfsHash,
            land[id].lamount,
            land[id].isGovtApproved,
            land[id].isAvailable,
            land[id].requester,
            land[id].requestStatus
        );
    }

    function govtStatus(
        uint256 _id,
        string memory status,
        string memory _isAvailable
    ) public returns (bool) {
        land[_id].isGovtApproved = status;
        land[_id].isAvailable = _isAvailable;
        return true;
    }

    function makeAvailable(uint256 property) public {
        require(land[property].id == msg.sender);
        land[property].isAvailable = "Available";
    }

    function requstToLandOwner(uint256 id) public {
        land[id].requester = msg.sender;
        land[id].isAvailable = "Pending";
        land[id].requestStatus = reqStatus.Pending;
    }

    function processRequest(uint256 property, reqStatus status) public {
        require(land[property].id == msg.sender);
        land[property].requestStatus = status;
        land[property].isAvailable = "Approved";
        if (status == reqStatus.Rejected) {
            land[property].requester = address(0);
            land[property].requestStatus = reqStatus.Default;
            land[property].isAvailable = "Available";
            land[property].rejectionReason = rejectionReason;
        }
    }

    
    function buyProperty(uint256 property) public payable {
        require(land[property].requestStatus == reqStatus.Approved);
        require(msg.value == (land[property].lamount * 10000000000000));
        land[property].id.transfer(
            land[property].lamount * 10000000000000
        );
// function buyProperty(uint256 property) public payable {
//     require(land[property].requestStatus == reqStatus.Approved, "Property purchase not approved");

//     // Calculate total price of the property
//     uint256 totalPrice = land[property].lamount * 10000000000000;

//     // Calculate stamp duty (8% of the total price)
//     uint256 stampDuty = totalPrice * 8 / 100;
    

//    // Ensure that the buyer sends enough funds to cover the total amount
//     require(msg.value == totalPrice + stampDuty, "Insufficient funds");

//    // Transfer payment to the seller
//     address payable seller = land[property].id;
//     seller.transfer(totalPrice);

//     //Transfer stamp duty to the government account
//     address payable governmentAccount = address(uint160(0x3f2D35d9c80d589EE25631c997373e858010831D));
//    governmentAccount.transfer(stampDuty);

    //Update ownership and status
    removeOwnership(land[property].id, property);
    land[property].id = msg.sender;
    land[property].isGovtApproved = "NULL";
    land[property].isAvailable = "Not yet approved by the govt.";
    land[property].requester = address(0);
    land[property].requestStatus = reqStatus.Default;
    profile[msg.sender].assetList.push(property);
}


    function removeOwnership(address previousOwner, uint256 id) private {
        uint256 index = findId(id, previousOwner);
        profile[previousOwner].assetList[index] = profile[previousOwner]
            .assetList[profile[previousOwner].assetList.length - 1];
        delete profile[previousOwner].assetList[profile[previousOwner]
            .assetList
            .length - 1];
        profile[previousOwner].assetList.length--;
    }

    function findId(uint256 id, address user) public view returns (uint256) {
        uint256 i;
        for (i = 0; i < profile[user].assetList.length; i++) {
            if (profile[user].assetList[i] == id) return i;
        }
        return i;
    }

    function updateIPFSHash(uint256 id, string memory newIPFSHash) public {
// removeOwnership(land[id].id, id);
// land[id].id = msg.sender;
// land[id].isGovtApproved = "NULL";
// land[id].isAvailable = "Not yet approved by the govt.";
// land[id].requester = address(0);
// land[id].requestStatus = reqStatus.Default;
// profile[msg.sender].assetList.push(id);
require(msg.sender == land[id].id, "Only the owner can update IPFS hash");
land[id].ipfsHash = newIPFSHash;

    }
    event PropertyRemoved(uint256 id);
    function removeProperty(uint256 id) public {
    // Check if the property with the given ID exists
    require(land[id].id != address(0), "Property does not exist");

    // Ensure that only the owner of the property can remove it
    require(land[id].id == msg.sender, "Only the owner can remove the property");

    // Remove the property by deleting it from the mapping and the owner's asset list
    delete land[id];
    removeOwnership(msg.sender, id);

    // Emit an event to indicate that the property has been removed
    emit PropertyRemoved(id);
}
function retrieveRejectionReason(uint256 id) public view returns (string memory) {
    // Check if the property with the given ID exists
    require(land[id].id != address(0), "Property does not exist");

    // Ensure that the property has been rejected
    require(land[id].requestStatus == reqStatus.Rejected, "Property not rejected");

    // Return the rejection reason
    return land[id].rejectionReason;
}


}
