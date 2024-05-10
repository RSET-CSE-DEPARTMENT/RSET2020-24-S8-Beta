// import React, { Component } from 'react'
// import { withRouter, Redirect } from 'react-router-dom'
// import { Button, Container, CircularProgress } from '@material-ui/core'
// import Land from '../abis/LandRegistry.json'
// import ipfs from '../ipfs'
// import Table from '../Containers/Owner_Table'
// import AvailableTable from '../Containers/Buyer_Table'
// import { withStyles } from '@material-ui/core/styles'
// import AppBar from '@material-ui/core/AppBar'
// import Tabs from '@material-ui/core/Tabs'
// import Tab from '@material-ui/core/Tab'
// import Typography from '@material-ui/core/Typography'
// import Box from '@material-ui/core/Box'
// import PropTypes from 'prop-types'
// // import SwipeableViews from 'react-swipeable-views'
// //import RegistrationForm from '../Containers/RegistrationForm'
// import Registration2 from '../Containers/Registration2'
// import axios from 'axios';

// function TabPanel(props) {
//   const { children, value, index, ...other } = props

//   return (
//     <div
//       role="tabpanel"
//       hidden={value !== index}
//       id={`full-width-tabpanel-${index}`}
//       aria-labelledby={`full-width-tab-${index}`}
//       {...other}
//     >
//       {value === index && (
//         <Box p={3}>
//           <Typography>{children}</Typography>
//         </Box>
//       )}
//     </div>
//   )
// }

// TabPanel.propTypes = {
//   children: PropTypes.node,
//   index: PropTypes.any.isRequired,
//   value: PropTypes.any.isRequired,
// }

// function a11yProps(index) {
//   return {
//     id: `full-width-tab-${index}`,
//     'aria-controls': `full-width-tabpanel-${index}`,
//   }
// }

// const styles = (theme) => ({
//   container: {
//     '& .MuiContainer-maxWidthLg': {
//       maxWidth: '100%',
//     },
//   },
//   root: {
//     backgroundColor: '#fff',
//     // width: 500,
//     borderRadius: '5px',
//     minHeight: '80vh',
//   },
// })

// class Dashboard extends Component {
//   constructor(props) {
//     super(props)
//     this.state = {
//       assetList: [],
//       assetList1: [],
//       isLoading: true,
//       value: 0,
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

//     if (
//       !window.localStorage.getItem('authenticated') ||
//       window.localStorage.getItem('authenticated') === 'false'
//     )
//       this.props.history.push('/login')
//     // const category=window.localStorage.getItem('category');
//     this.setState({ isLoading: false })
//     this.getDetails()
//     this.getDetails1()
//   }

//   async fetchDataFromPinata(ipfsHash) {
//     const JWT = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiI3ZWViNzgyYS1kNmU1LTQ2ZWYtYTlmZS1kNmIzZTRkY2NmOWQiLCJlbWFpbCI6InUyMDAzMTAxQHJhamFnaXJpLmVkdS5pbiIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaW5fcG9saWN5Ijp7InJlZ2lvbnMiOlt7ImlkIjoiRlJBMSIsImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxfSx7ImlkIjoiTllDMSIsImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxfV0sInZlcnNpb24iOjF9LCJtZmFfZW5hYmxlZCI6ZmFsc2UsInN0YXR1cyI6IkFDVElWRSJ9LCJhdXRoZW50aWNhdGlvblR5cGUiOiJzY29wZWRLZXkiLCJzY29wZWRLZXlLZXkiOiJjYzJlNDU2YzZhZTBiN2Q5YTM5NyIsInNjb3BlZEtleVNlY3JldCI6IjRiZDIyMzJhZDQzNmNlMzdlMDBhYWJhMTlmNjQ3YWY3NTQxOTNiNzAxMjI4MjIxMDI2MWFmNTg0MTFlZWE4ZTgiLCJpYXQiOjE3MTIyNDA4MjV9.QpMJbIE-xDc77LshaRFcOW0jw2wjxic1_1L4Frh2OUA'; // Replace with your Pinata API key

//     const pinataOptions = {
//       headers: {
//         Authorization: `Bearer ${JWT}`,
//         Accept: "text/plain",
//       },
//     };

//     try {
//       const response = await fetch(
//         `https://silver-adorable-ocelot-850.mypinata.cloud/ipfs/${ipfsHash}`,
//         pinataOptions
//       );

//       if (!response.ok) {
//         throw new Error(`Failed to fetch data from Pinata: ${response.statusText}`);
//       }

//       const responseData = await response.text();
//       // Handle the fetched data
//       console.log('Fetched data:', responseData);
//       return responseData; // Return fetched data
//     } catch (error) {
//       console.error('Error fetching data from Pinata:', error);
//       throw error; // Throw error for handling
//     }
//   }

//   // async propertyDetails(property) {
//   //   let details = await this.state.landList.methods
//   //     .landInfoOwner(property)
//   //     .call()
//   //   ipfs.cat(details[1], (err, res) => {
//   //     if (err) {
//   //       console.error(err)
//   //       return
//   //     }
//   //     const temp = JSON.parse(res.toString())
//   //     this.state.assetList.push({
//   //       property: property,
//   //       uniqueID: details[1],
//   //       name: temp.name,
//   //       key: details[0],
//   //       email: temp.email,
//   //       contact: temp.contact,
//   //       pan: temp.pan,
//   //       occupation: temp.occupation,
//   //       oaddress: temp.address,
//   //       ostate: temp.state,
//   //       ocity: temp.city,
//   //       opostalCode: temp.postalCode,
//   //       laddress: temp.laddress,
//   //       lstate: temp.lstate,
//   //       lcity: temp.lcity,
//   //       lpostalCode: temp.lpostalCode,
//   //       larea: temp.larea,
//   //       lamount: details[2],
//   //       isGovtApproved: details[3],
//   //       isAvailable: details[4],
//   //       requester: details[5],
//   //       requestStatus: details[6],
//   //       document: temp.document,
//   //       images: temp.images,
//   //     })
//   //     this.setState({ assetList: [...this.state.assetList] })
//   //   })
//   // }

//   async propertyDetails(property) {
//     let details = await this.state.landList.methods.landInfoOwner(property).call();

//     const ipfsHash = details[1];
//     // window.alert(ipfsHash);

//     try {
//       const dataFromPinata = await this.fetchDataFromPinata(ipfsHash);

//       this.state.assetList.push({
//         property: property,
//         uniqueID: details[1],
//         name: dataFromPinata.name,
//         key: details[0],
//         email: dataFromPinata.email,
//         contact: dataFromPinata.contact,
//         pan: dataFromPinata.pan,
//         occupation: dataFromPinata.occupation,
//         oaddress: dataFromPinata.address,
//         ostate: dataFromPinata.state,
//         ocity: dataFromPinata.city,
//         opostalCode: dataFromPinata.postalCode,
//         laddress: dataFromPinata.laddress,
//         lstate: dataFromPinata.lstate,
//         lcity: dataFromPinata.lcity,
//         lpostalCode: dataFromPinata.lpostalCode,
//         larea: dataFromPinata.larea,
//         lamount: details[2],
//         isGovtApproved: details[3],
//         isAvailable: details[4],
//         requester: details[5],
//         requestStatus: details[6],
//         document: dataFromPinata.document,
//         images: dataFromPinata.images,
//       });

//       this.setState({ assetList: [...this.state.assetList] });
//     } catch (error) {
//       console.error('Error fetching data from Pinata:', error);
//       window.alert('Error');
//       // Handle error appropriately
//     }
//   }

//   // async propertyDetails1(property) {
//   //   let details = await this.state.landList.methods
//   //     .landInfoOwner(property)
//   //     .call()
//   //   ipfs.cat(details[1], (err, res) => {
//   //     if (err) {
//   //       console.error(err)
//   //       return
//   //     }
//   //     const temp = JSON.parse(res.toString())
//   //     console.log('temp', temp)

//   //     if (
//   //       details[0] != this.state.account &&
//   //       (details[5] == this.state.account ||
//   //         details[5] == '0x0000000000000000000000000000000000000000')
//   //     ) {
//   //       this.state.assetList1.push({
//   //         property: property,
//   //         uniqueID: details[1],
//   //         name: temp.name,
//   //         key: details[0],
//   //         email: temp.email,
//   //         contact: temp.contact,
//   //         pan: temp.pan,
//   //         occupation: temp.occupation,
//   //         oaddress: temp.address,
//   //         ostate: temp.state,
//   //         ocity: temp.city,
//   //         opostalCode: temp.postalCode,
//   //         laddress: temp.laddress,
//   //         lstate: temp.lstate,
//   //         lcity: temp.lcity,
//   //         lpostalCode: temp.lpostalCode,
//   //         larea: temp.larea,
//   //         lamount: details[2],
//   //         isGovtApproved: details[3],
//   //         isAvailable: details[4],
//   //         requester: details[5],
//   //         requestStatus: details[6],
//   //         document: temp.document,
//   //         images: temp.images,
//   //       })
//   //       this.setState({ assetList1: [...this.state.assetList1] })
//   //     }
//   //   })
//   // }


//   async propertyDetails1(property) {
//     try {
//       let details = await this.state.landList.methods.landInfoOwner(property).call();
//       const ipfsHash = details[1];
//       const dataFromPinata = await this.fetchDataFromPinata(ipfsHash);

//       if (
//         details[0] !== this.state.account &&
//         (details[5] === this.state.account || details[5] === '0x0000000000000000000000000000000000000000')
//       ) {
//         this.state.assetList1.push({
//           property: property,
//           uniqueID: details[1],
//           name: dataFromPinata.name,
//           key: details[0],
//           email: dataFromPinata.email,
//           contact: dataFromPinata.contact,
//           pan: dataFromPinata.pan,
//           occupation: dataFromPinata.occupation,
//           oaddress: dataFromPinata.address,
//           ostate: dataFromPinata.state,
//           ocity: dataFromPinata.city,
//           opostalCode: dataFromPinata.postalCode,
//           laddress: dataFromPinata.laddress,
//           lstate: dataFromPinata.lstate,
//           lcity: dataFromPinata.lcity,
//           lpostalCode: dataFromPinata.lpostalCode,
//           larea: dataFromPinata.larea,
//           lamount: details[2],
//           isGovtApproved: details[3],
//           isAvailable: details[4],
//           requester: details[5],
//           requestStatus: details[6],
//           document: dataFromPinata.document,
//           images: dataFromPinata.images,
//         });
//         this.setState({ assetList1: [...this.state.assetList1] });
//       }
//     } catch (error) {
//       console.error('Error fetching property details:', error);
//       // Handle error appropriately
//     }
//   }


//   async getDetails() {
//     const properties = await this.state.landList.methods
//       .viewAssets()
//       .call({ from: this.state.account })
//     for (let item of properties) {
//       this.propertyDetails(item)
//     }
//   }
//   async getDetails1() {
//     const properties = await this.state.landList.methods.Assets().call()
//     // console.log(properties)

//     for (let item of properties) {
//       this.propertyDetails1(item)
//     }
//   }
//   handleChange = (event, newValue) => {
//     this.setState({ value: newValue })
//   }
//   handleChangeIndex = (index) => {
//     this.setState({ index })
//   }
//   render() {
//     const { classes } = this.props
//     return this.state.isLoading ? (
//       <div style={{ position: 'absolute', top: '50%', left: '50%' }}>
//         <CircularProgress />
//       </div>
//     ) : (
//       <div className="profile-bg ">
//         <div className={classes.container}>
//           <Container style={{ marginTop: '40px' }}>
//             <div className={classes.root}>
//               <AppBar position="static" color="default" className="dashboard">
//                 <Tabs
//                   value={this.state.value}
//                   onChange={this.handleChange}
//                   indicatorColor="primary"
//                   textColor="primary"
//                   variant="fullWidth"
//                   aria-label="full width tabs example"
//                 >
//                   <Tab label="My Properties" {...a11yProps(0)} />
//                   <Tab label="Available Properties" {...a11yProps(1)} />
//                   <Tab label="Regsiter Land" {...a11yProps(2)} />
//                 </Tabs>
//               </AppBar>
//               {/* <SwipeableViews
//         axis={theme.direction === 'rtl' ? 'x-reverse' : 'x'}
//         index={value}
//         onChangeIndex={handleChangeIndex}
//       > */}
//               <TabPanel value={this.state.value} index={0}>
//                 <div style={{ marginTop: '60px' }}>
//                   {/* <h2 style={{ textAlign: 'center' }}>My Properties</h2> */}
//                   <Table assetList={this.state.assetList} />
//                 </div>
//               </TabPanel>
//               <TabPanel value={this.state.value} index={1}>
//                 <div style={{ marginTop: '60px' }}>
//                   {/* <h2 style={{ textAlign: 'center' }}>Available Properties</h2> */}
//                   <AvailableTable assetList={this.state.assetList1} />
//                 </div>
//               </TabPanel>
//               <TabPanel value={this.state.value} index={2}>
//                 <Registration2 />
//               </TabPanel>

//               {/* </SwipeableViews> */}
//               {/* <Button
//               style={{ marginTop: '30px' }}
//               variant="contained"
//               color="primary"
//               onClick={() => this.props.history.push('/registration_form')}
//             >
//               Register Land
//             </Button> */}
//             </div>
//           </Container>
//         </div>
//       </div>
//     )
//   }
// }
// export default withStyles(styles)(Dashboard)

import React, { Component } from 'react'
import { withRouter } from 'react-router-dom'
import { Button, Container, CircularProgress } from '@material-ui/core'
import Land from '../abis/LandRegistry.json'
import Table from '../Containers/Owner_Table'
import AvailableTable from '../Containers/Buyer_Table'
import { withStyles } from '@material-ui/core/styles'
import AppBar from '@material-ui/core/AppBar'
import Tabs from '@material-ui/core/Tabs'
import Tab from '@material-ui/core/Tab'
import Typography from '@material-ui/core/Typography'
import Box from '@material-ui/core/Box'
import PropTypes from 'prop-types'
import Registration2 from '../Containers/Registration2'
import axios from 'axios';

function TabPanel(props) {
  const { children, value, index, ...other } = props

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`full-width-tabpanel-${index}`}
      aria-labelledby={`full-width-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box p={3}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  )
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.any.isRequired,
  value: PropTypes.any.isRequired,
}

function a11yProps(index) {
  return {
    id: `full-width-tab-${index}`,
    'aria-controls': `full-width-tabpanel-${index}`,
  }
}

const styles = (theme) => ({
  container: {
    '& .MuiContainer-maxWidthLg': {
      maxWidth: '100%',
    },
  },
  root: {
    backgroundColor: '#fff',
    borderRadius: '5px',
    minHeight: '80vh',
  },
})

class Dashboard extends Component {
  constructor(props) {
    super(props)
    this.state = {
      assetList: [],
      assetList1: [],
      isLoading: true,
      value: 0,
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

    if (
      !window.localStorage.getItem('authenticated') ||
      window.localStorage.getItem('authenticated') === 'false'
    )
      this.props.history.push('/login')
    this.setState({ isLoading: false })
    this.getDetails()
    this.getDetails1()
  }

  async fetchDataFromProxy(ipfsHash) {
    try {
      const response = await fetch(`http://localhost:3001/proxy?ipfsHash=${ipfsHash}`);
      const data = await response.text();
      return data;
    } catch (error) {
      console.error('Error fetching data from proxy:', error);
      throw error;
    }
  }


  async propertyDetails(property) {
    let details = await this.state.landList.methods.landInfoOwner(property).call();

    const ipfsHash = details[1];
    let dataFromProxy = await this.fetchDataFromProxy(ipfsHash);
    //console.log('data', dataFromProxy);

    try {
      if (typeof dataFromProxy === 'string') {
        // Parse the string data as JSON
        dataFromProxy = JSON.parse(dataFromProxy);
      }
      this.state.assetList.push({
        property: property,
        uniqueID: details[1],
        name: dataFromProxy.name,
        key: details[0],
        email: dataFromProxy.email,
        contact: dataFromProxy.contact,
        pan: dataFromProxy.pan,
        occupation: dataFromProxy.occupation,
        oaddress: dataFromProxy.address,
        ostate: dataFromProxy.state,
        ocity: dataFromProxy.city,
        opostalCode: dataFromProxy.postalCode,
        laddress: dataFromProxy.laddress,
        lstate: dataFromProxy.lstate,
        lcity: dataFromProxy.lcity,
        lpostalCode: dataFromProxy.lpostalCode,
        larea: dataFromProxy.larea,
        lamount: details[2],
        isGovtApproved: details[3],
        isAvailable: details[4],
        requester: details[5],
        requestStatus: details[6],
        document: dataFromProxy.document,
        images: dataFromProxy.images,
      });

      this.setState({ assetList: [...this.state.assetList] });
    } catch (error) {
      console.error('Error fetching data from proxy:', error);
    }
  }

  async propertyDetails1(property) {
    try {
      let details = await this.state.landList.methods.landInfoOwner(property).call();
      const ipfsHash = details[1];
      const dataFromProxy1 = await this.fetchDataFromProxy(ipfsHash);
      const dataFromProxy = JSON.parse(dataFromProxy1);
      // if (typeof dataFromProxy === 'string') {
      //   // Parse the string data as JSON
      //   dataFromProxy = JSON.parse(dataFromProxy);
      // }

      if (
        details[0] !== this.state.account &&
        (details[5] === this.state.account || details[5] === '0x0000000000000000000000000000000000000000')
      ) {
        this.state.assetList1.push({
          property: property,
          uniqueID: details[1],
          name: dataFromProxy.name,
          key: details[0],
          email: dataFromProxy.email,
          contact: dataFromProxy.contact,
          pan: dataFromProxy.pan,
          occupation: dataFromProxy.occupation,
          oaddress: dataFromProxy.address,
          ostate: dataFromProxy.state,
          ocity: dataFromProxy.city,
          opostalCode: dataFromProxy.postalCode,
          laddress: dataFromProxy.laddress,
          lstate: dataFromProxy.lstate,
          lcity: dataFromProxy.lcity,
          lpostalCode: dataFromProxy.lpostalCode,
          larea: dataFromProxy.larea,
          lamount: details[2],
          isGovtApproved: details[3],
          isAvailable: details[4],
          requester: details[5],
          requestStatus: details[6],
          document: dataFromProxy.document,
          images: dataFromProxy.images,
        });
        this.setState({ assetList1: [...this.state.assetList1] });
        console.log(this.state.assetList1)
      }
    } catch (error) {
      console.error('Error fetching property details:', error);
    }
  }

  async getDetails() {
    const properties = await this.state.landList.methods.viewAssets().call({ from: this.state.account })
    for (let item of properties) {
      this.propertyDetails(item)
    }
  }

  async getDetails1() {
    const properties = await this.state.landList.methods.Assets().call()
    for (let item of properties) {
      this.propertyDetails1(item)
    }
  }

  handleChange = (event, newValue) => {
    this.setState({ value: newValue })
  }

  render() {
    const { classes } = this.props
    return this.state.isLoading ? (
      <div style={{ position: 'absolute', top: '50%', left: '50%' }}>
        <CircularProgress />
      </div>
    ) : (
      <div className="profile-bg ">
        <div className={classes.container}>
          <Container style={{ marginTop: '40px' }}>
            <div className={classes.root}>
              <AppBar position="static" color="default" className="dashboard">
                <Tabs
                  value={this.state.value}
                  onChange={this.handleChange}
                  indicatorColor="primary"
                  textColor="primary"
                  variant="fullWidth"
                  aria-label="full width tabs example"
                >
                  <Tab label="My Properties" {...a11yProps(0)} />
                  <Tab label="Available Properties" {...a11yProps(1)} />
                  <Tab label="Regsiter Land" {...a11yProps(2)} />
                </Tabs>
              </AppBar>
              <TabPanel value={this.state.value} index={0}>
                <div style={{ marginTop: '60px' }}>
                  <Table assetList={this.state.assetList} />
                </div>
              </TabPanel>
              <TabPanel value={this.state.value} index={1}>
                <div style={{ marginTop: '60px' }}>
                  <AvailableTable assetList={this.state.assetList1} />
                </div>
              </TabPanel>
              <TabPanel value={this.state.value} index={2}>
                <Registration2 />
              </TabPanel>
            </div>
          </Container>
        </div>
      </div>
    )
  }
}

export default withStyles(styles)(withRouter(Dashboard))

