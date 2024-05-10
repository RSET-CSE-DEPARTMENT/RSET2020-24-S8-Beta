// import React, { Component } from 'react';
// import { withStyles } from '@material-ui/core/styles';
// import Paper from '@material-ui/core/Paper';
// import Table from '@material-ui/core/Table';
// import TableBody from '@material-ui/core/TableBody';
// import TableCell from '@material-ui/core/TableCell';
// import TableContainer from '@material-ui/core/TableContainer';
// import TableHead from '@material-ui/core/TableHead';
// import TableRow from '@material-ui/core/TableRow';
// import Button from '@material-ui/core/Button';
// import Dialog from '@material-ui/core/Dialog';
// import DialogActions from '@material-ui/core/DialogActions';
// import DialogContent from '@material-ui/core/DialogContent';
// import DialogContentText from '@material-ui/core/DialogContentText';
// import DialogTitle from '@material-ui/core/DialogTitle';
// import Slide from '@material-ui/core/Slide';
// import axios from 'axios';
// import Land from '../abis/LandRegistry.json';
// import Web3 from 'web3';

// const Transition = React.forwardRef(function Transition(props, ref) {
//   return <Slide direction="up" ref={ref} {...props} />;
// });

// const columns = [
//   { id: 'property', label: 'Property ID', minWidth: 100 },
//   { id: 'name', label: 'Full Name', minWidth: 100 },
//   { id: 'laddress', label: 'Land Details', minWidth: 170 },
//   { id: 'lstate', label: 'State', minWidth: 100 },
//   { id: 'lcity', label: 'City', minWidth: 100 },
//   { id: 'lamount', label: 'Total Amount (in Rs)', minWidth: 100 },
//   { id: 'document', label: 'Documents', minWidth: 100 },
//   { id: 'images', label: 'Land Images', minWidth: 100 },
//   { id: 'isGovtApproved', label: 'Status of Land Approval (by the Govt.)', minWidth: 100 },
//   { id: 'isAvailable', label: 'Land Availability Status', minWidth: 100 },
// ];

// const styles = (theme) => ({
//   root: {
//     width: '100%',
//   },
// });

// class TableComponent extends Component {
//   constructor(props) {
//     super(props);
//     this.state = {
//       assetList: [],
//       isLoading: true,
//       images: [],
//       open1: false,
//       account: '', // Added state for account
//       landList: null, // Added state for landList
//     };
//   }

//   componentDidMount = async () => {
//     const web3 = window.web3;
//     const accounts = await web3.eth.getAccounts();
//     await window.localStorage.setItem('web3account', accounts[0]);
//     this.setState({ account: accounts[0] });
//     const networkId = await web3.eth.net.getId();
//     const LandData = Land.networks[networkId];
//     if (LandData) {
//       const landList = new web3.eth.Contract(Land.abi, LandData.address);
//       this.setState({ landList });
//     } else {
//       window.alert('Token contract not deployed to detected network.');
//     }
//     const user = await this.state.landList.methods.getUser(accounts[0]).call();
//     this.setState({
//       uid: user[0],
//       uname: user[1],
//       ucontact: user[2],
//       uemail: user[3],
//       ucode: user[4],
//       ucity: user[5],
//       exist: user[6],
//     });
//   };

//   handleAccept = async (id, email) => {
//     await this.state.landList.methods.requstToLandOwner(id).send({
//       from: this.state.account,
//       gas: 1000000,
//     });
//     let data = {
//       lemail: email,
//       subject: `${this.state.uname} has requested to buy`,
//       message: `${this.state.uname} has requested to buy the property. Please check your account for more details.`,
//     };
//     console.log(data);
//     await axios
//       .post('http://localhost:3001/send_mail', data)
//       .then((response) => {
//         if (response.status === 200) {
//           alert('Message Sent.');
//         } else {
//           alert('Message failed to send.');
//         }
//       });
//     window.location.reload();
//   };

  // handleBuy = async (id, amount) => {
  //   amount = amount * 10000000000000;
  //   let mValue = parseInt(amount);
  //   let StringValue = mValue.toString();

  //   const web3 = window.web3;

  //   // Get the current Ethereum account
  //   const accounts = await web3.eth.getAccounts();
  //   const fromAccount = accounts[0];

  //   const stampDutyInWei = (amount * 8) / 100;

  //   // Convert the stamp duty amount to wei
  //   //const stampDutyInWei = web3.utils.toWei(stampDuty.toString(), 'ether');

  //   web3.eth.sendTransaction({
  //     from: fromAccount,
  //     to: '0x7c39e9dfF27336cd45F409e471Ba5d92f846482D', // Your Ganache account address
  //     value: stampDutyInWei,
  // }).then((stampDutyReceipt) => {
  //     // Stamp duty transfer successful
  //     console.log('Stamp duty transferred:', stampDutyReceipt)});

    

  //   // Call the buyProperty function on the contract
  //  // const gasEstimate = await contract.methods.buyProperty(propertyId).estimateGas({ from: sender, value: valueInWei });
  //   //window.alert(gasEstimate);
  //   await this.state.landList.methods.buyProperty(id).send({
  //     from: this.state.account,
  //     value: StringValue,
  //   });
  // // handleBuy = async (id) => {
  // //   try {
  // //       // Call the buyProperty function on the contract
  // //       const web3 = window.web3;
  // //       await this.state.landList.methods.buyProperty(id).send({
  // //           from: this.state.account,
  // //           value: web3.utils.toWei('0.1', 'ether'), // Sending a small amount as a placeholder
  // //           gas: 3000000,
  // //           gasPrice: web3.utils.toWei('10', 'gwei'),
  // //       });

  // //       // Reload the page or update state as needed
  // //       window.location.reload();
  // //       //console.log(receipt); // Log transaction receipt for debugging
  // //   } catch (error) {
  // //       // Handle error, e.g., display error message to the user
  // //       console.error("Error in buying property:", error);
  // //       //console.error("Transaction failed:", error.message); // Log error message

  // //   }


  //   // Retrieve the IPFS hash associated with the property from the contract
  //   const ipfsHash = await this.state.landList.methods.land(id).call().then(res => res.ipfsHash);

  //   // Fetch current details from Pinata
  //   const currentDetails = await this.fetchDetailsFromPinata(ipfsHash);

  //   // Modify details with new owner information
  //   const newOwnerDetails = {
  //     ...currentDetails,
  //     owner: this.state.account,
  //     name: this.state.uname, // Assuming you want to update the 'owner' field with the buyer's address
  //   };

  //   // Upload modified details to Pinata and get new IPFS hash
  //   const newIPFSHash = await this.uploadDetailsToPinata(newOwnerDetails);

  //   // Update the IPFS hash associated with the property in the contract
  //   await this.state.landList.methods.updateIPFSHash(id, newIPFSHash).send({
  //     from: this.state.account,
  //   });

  //   // Reload the page
  //   window.location.reload();
  // };

  // fetchDetailsFromPinata = async (ipfsHash) => {
  //   const response = await axios.get(`https://cors-anywhere.herokuapp.com/https://gateway.pinata.cloud/ipfs/${ipfsHash}`);
  //   return response.data;
  // };

  // uploadDetailsToPinata = async (updatedDetails) => {
  //   const response = await axios.post('https://api.pinata.cloud/pinning/pinJSONToIPFS', updatedDetails, {
  //     headers: {
  //       'Content-Type': 'application/json',
  //       'pinata_api_key': 'cc2e456c6ae0b7d9a397',
  //       'pinata_secret_api_key': '4bd2232ad436ce37e00aaba19f647af754193b7012282210261af58411eea8e8',
  //     },
  //   });
  //   return response.data.IpfsHash;
  // };

//   handleViewImages = async (images) => {
//     this.setState({ open1: true });

//     if (images) {
//       this.setState({
//         images: images,
//       });
//     }
//   };

//   handleClose1 = () => {
//     this.setState({ open1: false });
//   };

//   render() {
//     const { classes, assetList } = this.props;
//     return (
//       <Paper className={classes.root}>
//         {/* {console.log(assetList)} */}
//         {console.log(this.state)}
//         <TableContainer className={classes.container}>
//           <Table stickyHeader aria-label="sticky table">
//             <TableHead>
//               <TableRow>
//                 {columns.map((column) => (
//                   <TableCell
//                     key={column.id}
//                     align={column.align}
//                     style={{ minWidth: column.minWidth }}
//                   >
//                     <b>{column.label}</b>
//                   </TableCell>
//                 ))}
//               </TableRow>
//             </TableHead>
//             <TableBody>
//               {assetList.map((row, index) => {
//                 return (
//                   <TableRow hover role="checkbox" key={row.code}>
//                     {columns.map((column) => {
//                       const value = row[column.id]
//                       return (
//                         <TableCell key={column.id} align={column.align}>
//                           {column.id == 'isAvailable' &&
//                           value == 'Available' ? (
//                             <Button
//                               variant="contained"
//                               color="primary"
//                               onClick={() =>
//                                 this.handleAccept(row['property'], row['email'])
//                               }
//                             >
//                               Request to Buy
//                             </Button>
//                           ) : column.id == 'isAvailable' &&
//                             value == 'GovtApproved' ? (
//                             <div>Unavailable</div>
//                           ) : column.id == 'isAvailable' &&
//                             value == 'Approved' ? (
//                             <Button
//                               variant="contained"
//                               color="primary"
//                               onClick={() =>
//                                 this.handleBuy(row['property'], row['lamount'])
//                               }
//                             >
//                               Buy
//                             </Button>
//                           ) : column.id == 'document' ? (
//                             <a href={row['document']} download>
//                               Download Document
//                             </a>
//                           ) : column.id == 'images' ? (
//                             <Button
//                               variant="contained"
//                               color="primary"
//                               onClick={() =>
//                                 this.handleViewImages(row['images'])
//                               }
//                             >
//                               View Images
//                             </Button>
//                           ) : (
//                             value
//                           )}
//                           <Dialog
//                             open={this.state.open1}
//                             TransitionComponent={Transition}
//                             keepMounted
//                             onClose={this.handleClose1}
//                             aria-labelledby="alert-dialog-slide-title"
//                             aria-describedby="alert-dialog-slide-description"
//                           >
//                             <DialogTitle
//                               id="alert-dialog-slide-title"
//                               style={{ textAlign: 'center' }}
//                             >
//                               {'View Images'}
//                             </DialogTitle>
//                             <DialogContent>
//                               <DialogContentText id="alert-dialog-slide-description">
//                                 {this.state.images.map((image) => (
//                                   <img
//                                     src={image}
//                                     style={{
//                                       height: '300px',
//                                       width: '400px',
//                                       margin: '10px',
//                                     }}
//                                   />
//                                 ))}
//                               </DialogContentText>
//                             </DialogContent>
//                             <DialogActions>
//                               <Button
//                                 onClick={this.handleClose1}
//                                 color="primary"
//                               >
//                                 Close
//                               </Button>
//                             </DialogActions>
//                           </Dialog>
//                         </TableCell>
//                       )
//                     })}
//                   </TableRow>
//                 )
//               })}
//             </TableBody>
//           </Table>
//         </TableContainer>
//       </Paper>
//     );
//   }
// }

// export default withStyles(styles)(TableComponent);

import React, { Component } from 'react';
import { withStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import Slide from '@material-ui/core/Slide';
import axios from 'axios';
import Land from '../abis/LandRegistry.json';
import Web3 from 'web3';

const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});

const columns = [
  { id: 'property', label: 'Property ID', minWidth: 100 },
  { id: 'name', label: 'Full Name', minWidth: 100 },
  { id: 'laddress', label: 'Land Details', minWidth: 170 },
  { id: 'lstate', label: 'State', minWidth: 100 },
  { id: 'lcity', label: 'City', minWidth: 100 },
  { id: 'lamount', label: 'Total Amount (in Rs)', minWidth: 100 },
  { id: 'document', label: 'Documents', minWidth: 100 },
  { id: 'images', label: 'Land Images', minWidth: 100 },
  { id: 'isGovtApproved', label: 'Status of Land Approval (by the Govt.)', minWidth: 100 },
  { id: 'isAvailable', label: 'Land Availability Status', minWidth: 100 },
];

const styles = (theme) => ({
  root: {
    width: '100%',
  },
});

class TableComponent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      assetList: [],
      isLoading: true,
      images: [],
      open1: false,
      account: '', // Added state for account
      landList: null, // Added state for landList
      isStampDutyPaid: false, // State to track stamp duty payment status
    };
  }

  componentDidMount = async () => {
    const web3 = window.web3;
    const accounts = await web3.eth.getAccounts();
    await window.localStorage.setItem('web3account', accounts[0]);
    this.setState({ account: accounts[0] });
    const networkId = await web3.eth.net.getId();
    const LandData = Land.networks[networkId];
    if (LandData) {
      const landList = new web3.eth.Contract(Land.abi, LandData.address);
      this.setState({ landList });
    } else {
      window.alert('Token contract not deployed to detected network.');
    }
    const user = await this.state.landList.methods.getUser(accounts[0]).call();
    this.setState({
      uid: user[0],
      uname: user[1],
      ucontact: user[2],
      uemail: user[3],
      ucode: user[4],
      ucity: user[5],
      exist: user[6],
    });
  };

  handleAccept = async (id, email) => {
    await this.state.landList.methods.requstToLandOwner(id).send({
      from: this.state.account,
      gas: 1000000,
    });
    let data = {
      lemail: email,
      subject: `${this.state.uname} has requested to buy`,
      message: `${this.state.uname} has requested to buy the property. Please check your account for more details.`,
    };
    console.log(data);
    await axios
      .post('http://localhost:3001/send_mail', data)
      .then((response) => {
        if (response.status === 200) {
          alert('Message Sent.');
        } else {
          alert('Message failed to send.');
        }
      });
    window.location.reload();
  };

  payStampDutyAndBuy = async (id, amount) => {
    // Calculate stamp duty amount
    const stampDutyInWei = (amount * 10000000000000 * 8) / 100;

    // Transfer stamp duty to the specified account
    await this.payStampDuty(id, stampDutyInWei);
  };

  // Function to handle payment of stamp duty
  payStampDuty = async (id, stampDutyInWei) => {
    // Get the current Ethereum account
    const accounts = await window.web3.eth.getAccounts();
    const fromAccount = accounts[0];

    // Transfer the stamp duty to the specified account
    await window.web3.eth.sendTransaction({
      from: fromAccount,
      to: '0x3C1F7bEaFa7BA110E5041FF75F4Fa69D40bB24De', // Your Ganache account address
      value: stampDutyInWei,
    }).then((stampDutyReceipt) => {
      // Stamp duty transfer successful
      console.log('Stamp duty transferred:', stampDutyReceipt);

      // Update the UI to enable the "Buy" button
      this.setState({ isStampDutyPaid: true });
    }).catch((error) => {
      // Handle error
      console.error('Error transferring stamp duty:', error);
    });
  };

  handleBuyProperty = async (id,amount) => {
    // Implement logic for buying the property after stamp duty payment
    amount = amount * 10000000000000;
    let mValue = parseInt(amount);
    let StringValue = mValue.toString();
    await this.state.landList.methods.buyProperty(id).send({
            from: this.state.account,
            value: StringValue,
          });
          const ipfsHash = await this.state.landList.methods.land(id).call().then(res => res.ipfsHash);

    // Fetch current details from Pinata
    const currentDetails = await this.fetchDataFromProxy(ipfsHash);
    const currentDetails1 = JSON.parse(currentDetails);
    await this.state.landList.methods.govtStatus(id, "NULL", "Not Available").send({
      from: this.state.account,
      gas: 1000000,
    });
    
    // Modify details with new owner information
    const newOwnerDetails = {
      ...currentDetails1,
      owner: this.state.account,
      name: this.state.uname, // Assuming you want to update the 'owner' field with the buyer's address
    };

    // Upload modified details to Pinata and get new IPFS hash
    const newIPFSHash = await this.uploadDetailsToPinata(newOwnerDetails);

    // Update the IPFS hash associated with the property in the contract
    await this.state.landList.methods.updateIPFSHash(id, newIPFSHash).send({
      from: this.state.account,
    });

    // Reload the page
    window.location.reload();
  };
  // fetchDetailsFromPinata = async (ipfsHash) => {
  //     const response = await axios.get(`https://cors-anywhere.herokuapp.com/https://gateway.pinata.cloud/ipfs/${ipfsHash}`);
  //     return response.data;
  //   };

     fetchDataFromProxy= async (ipfsHash) => {
      try {
        const response = await fetch(`http://localhost:3001/proxy?ipfsHash=${ipfsHash}`);
        const data = await response.text();
        return data;
      } catch (error) {
        console.error('Error fetching data from proxy:', error);
       // throw error;
      }
    }
  
    uploadDetailsToPinata = async (updatedDetails) => {
      const response = await axios.post('https://api.pinata.cloud/pinning/pinJSONToIPFS', updatedDetails, {
        headers: {
          'Content-Type': 'application/json',
          'pinata_api_key': 'cc2e456c6ae0b7d9a397',
          'pinata_secret_api_key': '4bd2232ad436ce37e00aaba19f647af754193b7012282210261af58411eea8e8',
        },
      });
      return response.data.IpfsHash;
    };

  handleViewImages = async (images) => {
    this.setState({ open1: true });

    if (images) {
      this.setState({
        images: images,
      });
    }
  };

  handleClose1 = () => {
    this.setState({ open1: false });
  };

  render() {
    const { classes, assetList } = this.props;
    return (
      <Paper className={classes.root}>
        {/* {console.log(assetList)} */}
        {console.log(this.state)}
        <TableContainer className={classes.container}>
          <Table stickyHeader aria-label="sticky table">
            <TableHead>
              <TableRow>
                {columns.map((column) => (
                  <TableCell
                    key={column.id}
                    align={column.align}
                    style={{ minWidth: column.minWidth }}
                  >
                    <b>{column.label}</b>
                  </TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>

              {assetList.map((row, index) => {
               if (row['isGovtApproved'] !== 'NULL') {
                return (
                  <TableRow hover role="checkbox" key={row.code}>
                    {columns.map((column) => {
                      const value = row[column.id]
                      return (
                        <TableCell key={column.id} align={column.align}>
                          {column.id == 'isAvailable' &&
                          value == 'Available' ? (
                            <Button
                              variant="contained"
                              color="primary"
                              onClick={() =>
                                this.handleAccept(row['property'], row['email'])
                              }
                            >
                              Request to Buy
                            </Button>
                          ) : column.id == 'isAvailable' &&
                            value == 'GovtApproved' ? (
                            <div>Unavailable</div>
                          ) : column.id == 'isAvailable' &&
                            value == 'Approved' && !this.state.isStampDutyPaid ? (
                            <Button
                              variant="contained"
                              color="primary"
                              onClick={() =>
                                this.payStampDutyAndBuy(row['property'], row['lamount'])
                              }
                            >
                              Pay Stamp Duty
                            </Button>
                          ) : column.id == 'isAvailable' &&
                            value == 'Approved' && this.state.isStampDutyPaid ? (
                            <Button
                              variant="contained"
                              color="primary"
                              onClick={() =>
                                this.handleBuyProperty(row['property'], row['lamount'])
                              }
                            >
                              Buy Property
                            </Button>
                          ) : column.id == 'document' ? (
                            <a href={row['document']} download>
                              Download Document
                            </a>
                          ) : column.id == 'images' ? (
                            <Button
                              variant="contained"
                              color="primary"
                              onClick={() =>
                                this.handleViewImages(row['images'])
                              }
                            >
                              View Images
                            </Button>
                          ) : (
                            value
                          )}
                          <Dialog
                            open={this.state.open1}
                            TransitionComponent={Transition}
                            keepMounted
                            onClose={this.handleClose1}
                            aria-labelledby="alert-dialog-slide-title"
                            aria-describedby="alert-dialog-slide-description"
                          >
                            <DialogTitle
                              id="alert-dialog-slide-title"
                              style={{ textAlign: 'center' }}
                            >
                              {'View Images'}
                            </DialogTitle>
                            <DialogContent>
                              <DialogContentText id="alert-dialog-slide-description">
                                {this.state.images.map((image) => (
                                  <img
                                    src={image}
                                    style={{
                                      height: '300px',
                                      width: '400px',
                                      margin: '10px',
                                    }}
                                  />
                                ))}
                              </DialogContentText>
                            </DialogContent>
                            <DialogActions>
                              <Button
                                onClick={this.handleClose1}
                                color="primary"
                              >
                                Close
                              </Button>
                            </DialogActions>
                          </Dialog>
                        </TableCell>
                      )
                    })}
                  </TableRow>
                )
              } else {
                // Skip rendering if the government approval status is "NULL"
                return null;
              }
              
              })}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    );
  }
}

export default withStyles(styles)(TableComponent);


























