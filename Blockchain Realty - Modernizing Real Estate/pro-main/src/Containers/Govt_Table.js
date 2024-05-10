// import React, { Component } from 'react'
// import { makeStyles } from '@material-ui/core/styles'
// import Paper from '@material-ui/core/Paper'
// import Table from '@material-ui/core/Table'
// import TableBody from '@material-ui/core/TableBody'
// import TableCell from '@material-ui/core/TableCell'
// import TableContainer from '@material-ui/core/TableContainer'
// import TableHead from '@material-ui/core/TableHead'
// import TextField from '@material-ui/core/TextField';
// import TablePagination from '@material-ui/core/TablePagination'
// import TableRow from '@material-ui/core/TableRow'
// import { withStyles } from '@material-ui/core/styles'
// import Button from '@material-ui/core/Button'
// import Grid from '@material-ui/core/Grid'
// import Land from '../abis/LandRegistry.json'
// import axios from 'axios'
// import Dialog from '@material-ui/core/Dialog'
// import DialogActions from '@material-ui/core/DialogActions'
// import DialogContent from '@material-ui/core/DialogContent'
// import DialogContentText from '@material-ui/core/DialogContentText'
// import DialogTitle from '@material-ui/core/DialogTitle'
// import Slide from '@material-ui/core/Slide'



// const Transition = React.forwardRef(function Transition(props, ref) {
//   return <Slide direction="up" ref={ref} {...props} />
// })
// const columns = [
//   { id: 'property', label: 'Property ID', minWidth: 100 },
//   { id: 'name', label: 'Full Name', minWidth: 100 },

//   {
//     id: 'laddress',
//     label: 'Land Details',
//     minWidth: 170,
//   },

//   {
//     id: 'lstate',
//     label: 'State',
//     minWidth: 100,
//   },
//   {
//     id: 'lcity',
//     label: 'City',
//     minWidth: 100,
//   },

//   {
//     id: 'lamount',
//     label: 'Total Amount (in Rs)',
//     minWidth: 100,
//   },
//   {
//     id: 'document',
//     label: 'Documents',
//     minWidth: 100,
//   },
//   {
//     id: 'images',
//     label: 'Land Images',
//     minWidth: 100,
//   },
//   {
//     id: 'isGovtApproved',
//     label: 'Status of Land Approval (by the Govt.)',
//     minWidth: 100,
//   },
//   {
//     id: 'isAvailable',
//     label: 'Land Availability Status',
//     minWidth: 100,
//   },
// ]

// const styles = (theme) => ({
//   root: {
//     width: '100%',
//   },
//   buttonGroup: {
//     display: 'flex',
//     gap: '8px', // Add gap between buttons
//     marginBottom: '8px', // Add vertical spacing
//   },
//   rejectReasonTextField: {
//     marginBottom: '8px', // Add vertical spacing
//   },
// });

// class table extends Component {
//   constructor(props) {
//     super(props)
//     this.state = {
//       assetList: [],
//       isLoading: true,
//       images: [],
//       open1: false,
//       rejectReason: '',
//       isRejecting: false, 
//       selectedRejectId: null,
//       rejectionReasons: {},
//     }
//   }
//   componentDidMount = async () => {
//     const web3 = window.web3
//     const accounts = await web3.eth.getAccounts()
//     await window.localStorage.setItem('web3account', accounts[0])
//     this.setState({ account: accounts[0] })
//     const networkId = await web3.eth.net.getId()
//     const LandData = Land.networks[networkId]
//     if (LandData) {
//       const landList = new web3.eth.Contract(Land.abi, LandData.address)
//       this.setState({ landList })
//     } else {
//       window.alert('Token contract not deployed to detected network.')
//     }
//   }

//   handleAccept = async (id, status, status1, email, number, rejectReason) => {
//     // if (status === 'Rejected') {
//     //   this.setState({ isRejecting: true }); // Set state variable to true when reject button is clicked
//     //   return; // Exit function to show text field for reject reason
//     // }

//     const flag = await this.state.landList.methods
//       .govtStatus(id, status, status1)
//       .send({
//         from: this.state.account,
//         gas: 1000000,
//       })
//     let data = {
//       lemail: email,
//       subject:
//         status == 'Approved'
//           ? 'Government has accepted your request.'
//           : 'Government has rejected your request.',
//       message:
//         status == 'Approved'
//           ? 'Government has accepted your request. Please check your account for more details.'
//           : 'Government has rejected your request. Please check your account for more details.',
//       number,
//       rejectReason: status == 'Rejected' ? rejectReason : '',
//     }
//     console.log(data)
//     await axios
//       .post('http://localhost:3001/send_mail', data)
//       .then((response) => {
//         if (response.status == 200) {
//           alert('Message Sent.')
//         } else {
//           alert('Message failed to send.')
//         }
//       })
//     this.setState({ flag })
//     if (flag) window.location.reload()
//   }
//   handleViewImages = async (images) => {
//     this.setState({ open1: true })

//     if (images) {
//       this.setState({
//         images: images,
//       })
//     }
//   }
//   handleClose1 = () => {
//     this.setState({ open1: false })
//   }

//   handleReject = (id, status, status1, email, number, rejectionReason) => {
//     const { rejectionReasons } = this.state;
//     const { selectedRejectId, isRejecting, rejectReason } = this.state;

//     // If the Reject button is clicked again for the same row, toggle isRejecting state
//     if (selectedRejectId === id && isRejecting) {
//         const updatedReasons = { ...rejectionReasons, [id]: rejectReason };
//         this.setState({ rejectionReasons: updatedReasons });
//         this.setState({ isRejecting: false, selectedRejectId: null, rejectReason: '' });
//         // Call handleAccept function when Reject button is clicked again
//         this.handleAccept(id, status, status1, email, number, rejectReason);
//     } else {
//         // If it's the first time Reject button is clicked or for a different row, set isRejecting state and selectedRejectId
//         if (!rejectionReason) {
//             const enteredReason = prompt("Enter rejection reason:");
//             if (enteredReason === null || enteredReason === '') return; // If cancel is pressed or no reason is entered, do nothing
//             rejectionReason = enteredReason;
//         }
//         // Call the smart contract function with the rejection reason
//         this.state.landList.methods.processRequest(id, status, status1, email, number, rejectionReason)
//             .send({
//                 from: this.state.account,
//                 gas: 1000000
//             })
//             .then(() => {
//                 // Reload the page after processing the request
//                 window.location.reload();
//             });

//         this.setState({ isRejecting: true, selectedRejectId: id });
//     }
// };


//   handleRejectReasonChange = (event) => {
//     // Update reject reason state when text field value changes
//     this.setState({ rejectReason: event.target.value });
//   };

// //   render() {
// //     const { classes, assetList } = this.props;
// //     const { isRejecting, rejectReason, selectedRejectId } = this.state;

// //     return (
// //       <Paper className={classes.root}>
// //         <TableContainer className={classes.container}>
// //           <Table stickyHeader aria-label="sticky table">
// //             <TableHead>
// //               <TableRow>
// //                 {columns.map((column) => (
// //                   <TableCell
// //                     key={column.id}
// //                     align={column.align}
// //                     style={{ minWidth: column.minWidth }}
// //                   >
// //                     <b>{column.label}</b>
// //                   </TableCell>
// //                 ))}
// //               </TableRow>
// //             </TableHead>
// //             <TableBody>
// //               {assetList.map((row, index) => {
// //                 return (
// //                   <TableRow hover role="checkbox" key={row.code}>
// //                     {columns.map((column) => {
// //                       const value = row[column.id];
// //                       return (
// //                         <TableCell key={column.id} align={column.align}>
// //                           {column.id === 'isGovtApproved' && value === 'Not Approved' ? (
// //                             <div>
// //                               <Button
// //                                 variant="contained"
// //                                 color="primary"
// //                                 onClick={() =>
// //                                   this.handleAccept(
// //                                     row['property'],
// //                                     'Approved',
// //                                     'GovtApproved',
// //                                     row['email'],
// //                                     row['contact']
// //                                   )
// //                                 }
// //                               >
// //                                 Accept
// //                               </Button>
// //                               <Button
// //                                 variant="contained"
// //                                 color="secondary"
// //                                 onClick={() =>
// //                                   this.handleReject(
// //                                     row['property'],
// //                                     'Rejected',
// //                                     'GovtRejected',
// //                                     row['email'],
// //                                     row['contact']
// //                                   )
// //                                 }
// //                               >
// //                                 Reject
// //                               </Button>
// //                               {isRejecting && selectedRejectId === row['property'] && ( // Render text field only for the selected row
// //                                 <TextField
// //                                   label="Reason for rejection"
// //                                   multiline
// //                                   rows={4}
// //                                   value={rejectReason}
// //                                   onChange={this.handleRejectReasonChange}
// //                                 />
// //                               )}
// //                             </div>
// //                           ) : column.id === 'document' ? (
// //                             <a href={row['document']} download>
// //                               Download Document
// //                             </a>
// //                           ) : column.id === 'images' ? (
// //                             <Button
// //                               variant="contained"
// //                               color="primary"
// //                               onClick={() => this.handleViewImages(row['images'])}
// //                             >
// //                               View Images
// //                             </Button>
// //                           ) : (
// //                             value
// //                           )}
// //                           <Dialog
// //                             open={this.state.open1}
// //                             TransitionComponent={Transition}
// //                             keepMounted
// //                             onClose={this.handleClose1}
// //                             aria-labelledby="alert-dialog-slide-title"
// //                             aria-describedby="alert-dialog-slide-description"
// //                           >
// //                             <DialogTitle
// //                               id="alert-dialog-slide-title"
// //                               style={{ textAlign: 'center' }}
// //                             >
// //                               {'View Images'}
// //                             </DialogTitle>
// //                             <DialogContent>
// //                               <DialogContentText id="alert-dialog-slide-description">
// //                                 {this.state.images.map((image) => (
// //                                   <img
// //                                     src={image}
// //                                     style={{
// //                                       height: '300px',
// //                                       width: '400px',
// //                                       margin: '10px',
// //                                     }}
// //                                   />
// //                                 ))}
// //                               </DialogContentText>
// //                             </DialogContent>
// //                             <DialogActions>
// //                               <Button onClick={this.handleClose1} color="primary">
// //                                 Close
// //                               </Button>
// //                             </DialogActions>
// //                           </Dialog>
// //                         </TableCell>
// //                       );
// //                     })}
// //                   </TableRow>
// //                 );
// //               })}
// //             </TableBody>
// //           </Table>
// //         </TableContainer>
// //       </Paper>
// //     );
// //   }
// // }

// render() {
//   const { classes, assetList } = this.props;
//   const { isRejecting, rejectReason, selectedRejectId } = this.state;

//   return (
//     <Paper className={classes.root}>
//       <TableContainer className={classes.container}>
//         <Table stickyHeader aria-label="sticky table">
//           <TableHead>
//             <TableRow>
//               {columns.map((column) => (
//                 <TableCell
//                   key={column.id}
//                   align={column.align}
//                   style={{ minWidth: column.minWidth }}
//                 >
//                   <b>{column.label}</b>
//                 </TableCell>
//               ))}
//             </TableRow>
//           </TableHead>
//           <TableBody>
//             {assetList.map((row, index) => {
//               return (
//                 <TableRow hover role="checkbox" key={row.code}>
//                   {columns.map((column) => {
//                     const value = row[column.id];
//                     return (
//                       <TableCell key={column.id} align={column.align}>
//                         {column.id === 'isGovtApproved' && value === 'Not Approved' ? (
//                           <div>
//                             <div className={classes.buttonGroup}>
//                               <Button
//                                 variant="contained"
//                                 color="primary"
//                                 onClick={() =>
//                                   this.handleAccept(
//                                     row['property'],
//                                     'Approved',
//                                     'GovtApproved',
//                                     row['email'],
//                                     row['contact']
//                                   )
//                                 }
//                               >
//                                 Accept
//                               </Button>
//                               <Button
//                                 variant="contained"
//                                 color="secondary"
//                                 onClick={() =>
//                                                                      this.handleReject(
//                                                                       row['property'],
//                                                                     'Rejected',
//                                                                       'GovtRejected',
//                                                                        row['email'],
//                                                                        row['contact']
//                                                                      )
//                                                                    }
//                               >
//                                 Reject
//                               </Button>
//                             </div>
//                             {isRejecting && selectedRejectId === row['property'] && ( // Render text field only for the selected row
//                               <TextField
//                                 className={classes.rejectReasonTextField}
//                                 label="Reason for rejection"
//                                 multiline
//                                 rows={4}
//                                 value={rejectReason}
//                                 onChange={this.handleRejectReasonChange}
//                               />
//                             )}
//                           </div>
//                         ) : column.id === 'document' ? (
//                           <a href={row['document']} download>
//                             Download Document
//                           </a>
//                         ) : column.id === 'images' ? (
//                           <Button
//                             variant="contained"
//                             color="primary"
//                             onClick={() => this.handleViewImages(row['images'])}
//                           >
//                             View Images
//                           </Button>
//                         ) : (
//                           value
//                         )}
//                         <Dialog
//                           open={this.state.open1}
//                           TransitionComponent={Transition}
//                           keepMounted
//                           onClose={this.handleClose1}
//                           aria-labelledby="alert-dialog-slide-title"
//                           aria-describedby="alert-dialog-slide-description"
//                         >
//                           <DialogTitle
//                             id="alert-dialog-slide-title"
//                             style={{ textAlign: 'center' }}
//                           >
//                             {'View Images'}
//                           </DialogTitle>
//                           <DialogContent>
//                             <DialogContentText id="alert-dialog-slide-description">
//                               {this.state.images.map((image) => (
//                                 <img
//                                   src={image}
//                                   style={{
//                                     height: '300px',
//                                     width: '400px',
//                                     margin: '10px',
//                                   }}
//                                 />
//                               ))}
//                             </DialogContentText>
//                           </DialogContent>
//                           <DialogActions>
//                             <Button onClick={this.handleClose1} color="primary">
//                               Close
//                             </Button>
//                           </DialogActions>
//                         </Dialog>
//                       </TableCell>
//                     );
//                   })}
//                 </TableRow>
//               );
//             })}
//           </TableBody>
//         </Table>
//       </TableContainer>
//     </Paper>
//   );
// }
// }


// export default withStyles(styles)(table)


import React, { Component } from 'react'
import { makeStyles } from '@material-ui/core/styles'
import Paper from '@material-ui/core/Paper'
import Table from '@material-ui/core/Table'
import TableBody from '@material-ui/core/TableBody'
import TableCell from '@material-ui/core/TableCell'
import TableContainer from '@material-ui/core/TableContainer'
import TableHead from '@material-ui/core/TableHead'
import TablePagination from '@material-ui/core/TablePagination'
import TableRow from '@material-ui/core/TableRow'
import { withStyles } from '@material-ui/core/styles'
import Button from '@material-ui/core/Button'
import Grid from '@material-ui/core/Grid'
import Land from '../abis/LandRegistry.json'
import axios from 'axios'
import Dialog from '@material-ui/core/Dialog'
import DialogActions from '@material-ui/core/DialogActions'
import DialogContent from '@material-ui/core/DialogContent'
import DialogContentText from '@material-ui/core/DialogContentText'
import DialogTitle from '@material-ui/core/DialogTitle'
import Slide from '@material-ui/core/Slide'

const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />
})
const columns = [
  { id: 'property', label: 'Property ID', minWidth: 100 },
  { id: 'name', label: 'Full Name', minWidth: 100 },

  {
    id: 'laddress',
    label: 'Land Details',
    minWidth: 170,
  },

  {
    id: 'lstate',
    label: 'State',
    minWidth: 100,
  },
  {
    id: 'lcity',
    label: 'City',
    minWidth: 100,
  },

  {
    id: 'lamount',
    label: 'Total Amount (in Rs)',
    minWidth: 100,
  },
  {
    id: 'document',
    label: 'Documents',
    minWidth: 100,
  },
  {
    id: 'images',
    label: 'Land Images',
    minWidth: 100,
  },
  {
    id: 'isGovtApproved',
    label: 'Status of Land Approval (by the Govt.)',
    minWidth: 100,
  },
  {
    id: 'isAvailable',
    label: 'Land Availability Status',
    minWidth: 100,
  },
]

const styles = (theme) => ({
  root: {
    width: '100%',
  },
})

class table extends Component {
  constructor(props) {
    super(props)
    this.state = {
      assetList: [],
      isLoading: true,
      images: [],
      open1: false,
    }
  }
  componentDidMount = async () => {
    const web3 = window.web3
    const accounts = await web3.eth.getAccounts()
    await window.localStorage.setItem('web3account', accounts[0])
    this.setState({ account: accounts[0] })
    const networkId = await web3.eth.net.getId()
    const LandData = Land.networks[networkId]
    if (LandData) {
      const landList = new web3.eth.Contract(Land.abi, LandData.address)
      this.setState({ landList })
    } else {
      window.alert('Token contract not deployed to detected network.')
    }
  }

  handleAccept = async (id, status, status1, email, number) => {
    const flag = await this.state.landList.methods
      .govtStatus(id, status, status1)
      .send({
        from: this.state.account,
        gas: 1000000,
      })
    let data = {
      lemail: email,
      subject:
        status == 'Approved'
          ? 'Government has accepted your request.'
          : 'Government has rejected your request.',
      message:
        status == 'Approved'
          ? 'Government has accepted your request. Please check your account for more details.'
          : 'Government has rejected your request. Please check your account for more details.',
      number,
    }
    console.log(data)
    await axios
      .post('http://localhost:3001/send_mail', data)
      .then((response) => {
        if (response.status == 200) {
          alert('Message Sent.')
        } else {
          alert('Message failed to send.')
        }
      })
    this.setState({ flag })
    if (flag) window.location.reload()
  }
  handleViewImages = async (images) => {
    this.setState({ open1: true })

    if (images) {
      this.setState({
        images: images,
      })
    }
  }
  handleClose1 = () => {
    this.setState({ open1: false })
  }

  render() {
    const { classes, assetList } = this.props
    return (
      <Paper className={classes.root}>
        {console.log(assetList)}
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
                return (
                  <TableRow hover role="checkbox" key={row.code}>
                    {columns.map((column) => {
                      const value = row[column.id]
                      return (
                        <TableCell key={column.id} align={column.align}>
                          {column.id == 'isGovtApproved' &&
                          value == 'Not Approved' ? (
                            <Grid container spacing={2}>
                              <Grid item>
                                <Button
                                  variant="contained"
                                  color="primary"
                                  onClick={() =>
                                    this.handleAccept(
                                      row['property'],
                                      'Approved',
                                      'GovtApproved',
                                      row['email'],
                                      row['contact'],
                                    )
                                  }
                                >
                                  Accept
                                </Button>
                              </Grid>
                              <Grid item>
                                <Button
                                  variant="contained"
                                  color="secondary"
                                  onClick={() =>
                                    this.handleAccept(
                                      row['property'],
                                      'Rejected',
                                      'GovtRejected',
                                      row['email'],
                                      row['contact'],
                                    )
                                  }
                                >
                                  Reject
                                </Button>
                              </Grid>
                            </Grid>
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
              })}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    )
  }
}
export default withStyles(styles)(table)
