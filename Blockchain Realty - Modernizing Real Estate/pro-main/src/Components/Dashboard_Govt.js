import React, { Component } from 'react'
import { withRouter, Redirect } from 'react-router-dom'
import { Button, Container, CircularProgress } from '@material-ui/core'
import Land from '../abis/LandRegistry.json'
import ipfs from '../ipfs'
import Table from '../Containers/Govt_Table'
import { withStyles } from '@material-ui/core/styles'
import Web3 from 'web3'
import jwtDecode from 'jwt-decode'
import axios from 'axios';

const styles = (theme) => ({
  container: {
    // paddingLedt: '0px',
    // paddingRight: '0px',
    '& .MuiContainer-maxWidthLg': {
      maxWidth: '100%',
    },
  },
})

class Dashboard extends Component {
  constructor(props) {
    super(props)
    this.state = {
      assetList: [],
      isLoading: true,
      username: '',
      Governmentpublickey: '',
      address: '',
      contact: '',
      city: '',
      imgurl: '',
    }
  }

  componentWillMount = async () => {
    // console.log('token= ' + window.localStorage.getItem('token'))
    const user = jwtDecode(window.localStorage.getItem('token'))
    this.setState({ ...user.user })
    // this.setState({ ...user.user })
    const web3 = window.web3
    // Use web3 to get the user's accounts.
    const accounts = await web3.eth.getAccounts()
    window.localStorage.setItem('web3account', accounts[0])
    this.setState({ isLoading: false })
    const networkId = await web3.eth.net.getId()
    const LandData = Land.networks[networkId]
    if (LandData) {
      const landList = new web3.eth.Contract(Land.abi, LandData.address)
      this.setState({ landList })
    } else {
      window.alert('Token contract not deployed to detected network.')
    }
    this.getDetails()
  }
  // async fetchDataFromPinata(ipfsHash) {
  //   const JWT = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiI3ZWViNzgyYS1kNmU1LTQ2ZWYtYTlmZS1kNmIzZTRkY2NmOWQiLCJlbWFpbCI6InUyMDAzMTAxQHJhamFnaXJpLmVkdS5pbiIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaW5fcG9saWN5Ijp7InJlZ2lvbnMiOlt7ImlkIjoiRlJBMSIsImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxfSx7ImlkIjoiTllDMSIsImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxfV0sInZlcnNpb24iOjF9LCJtZmFfZW5hYmxlZCI6ZmFsc2UsInN0YXR1cyI6IkFDVElWRSJ9LCJhdXRoZW50aWNhdGlvblR5cGUiOiJzY29wZWRLZXkiLCJzY29wZWRLZXlLZXkiOiJjYzJlNDU2YzZhZTBiN2Q5YTM5NyIsInNjb3BlZEtleVNlY3JldCI6IjRiZDIyMzJhZDQzNmNlMzdlMDBhYWJhMTlmNjQ3YWY3NTQxOTNiNzAxMjI4MjIxMDI2MWFmNTg0MTFlZWE4ZTgiLCJpYXQiOjE3MTIyNDA4MjV9.QpMJbIE-xDc77LshaRFcOW0jw2wjxic1_1L4Frh2OUA'; // Replace with your Pinata API key

  //   const pinataOptions = {
  //     headers: {
  //       Authorization: `Bearer ${JWT}`,
  //       Accept: "text/plain",
  //     },
  //   };

  //   try {
  //     const response = await axios.get(
  //       `https://cors-anywhere.herokuapp.com/https://gateway.pinata.cloud/ipfs/${ipfsHash}`,
  //       pinataOptions
  //     );
       // Handle the fetched data
  //      console.log('Fetched data:', response.data);
  //      return response.data; // Return fetched data
  //    } catch (error) {
  //      console.error('Error fetching data from Pinata:', error);
  //      throw error; // Throw error for handling
  //    }
  //  }

  async fetchDataFromProxy(ipfsHash) {
    try {
      const response = await fetch(`http://localhost:3001/proxy?ipfsHash=${ipfsHash}`);
      const data = await response.text();
      //console.log(data)
      //window.alert(data);
      return data;
    } catch (error) {
      console.error('Error fetching data from proxy:', error);
      throw error;
    }
  }


 
  async propertyDetails(property) {
    let details = await this.state.landList.methods.landInfoOwner(property).call();
    const ipfsHash = details[1];
  
    try {
      const dataFromPinata1 = await this.fetchDataFromProxy(ipfsHash);
     // console.log('Data from Pinata:', dataFromPinata1);

      const dataFromPinata = JSON.parse(dataFromPinata1);
  
      // Create a new asset object
      const newAsset = {
        property: property,
        uniqueID: details[1],
        name: dataFromPinata.name,
        key: details[0],
        email: dataFromPinata.email,
        contact: dataFromPinata.contact,
        pan: dataFromPinata.pan,
        occupation: dataFromPinata.occupation,
        oaddress: dataFromPinata.address,
        ostate: dataFromPinata.state,
        ocity: dataFromPinata.city,
        opostalCode: dataFromPinata.postalCode,
        laddress: dataFromPinata.laddress,
        lstate: dataFromPinata.lstate,
        lcity: dataFromPinata.lcity,
        lpostalCode: dataFromPinata.lpostalCode,
        larea: dataFromPinata.larea,
        lamount: details[2],
        isGovtApproved: details[3],
        isAvailable: details[4],
        requester: details[5],
        requestStatus: details[6],
        document: dataFromPinata.document,
        images: dataFromPinata.images,
      };
  
    //  console.log('New Asset:', newAsset);
  
      // Update state immutably
      this.setState(prevState => ({
        assetList: [...prevState.assetList, newAsset]
      }), () => {
        console.log('Updated Asset List:', this.state.assetList);
      });
    } catch (error) {
      console.error('Error fetching data from Pinata:', error);
     // window.alert('Error');
      // Handle error appropriately
    }
  }
  
      
  async getDetails() {
    const properties = await this.state.landList.methods.Assets().call();
  
    for (let item of properties) {
      console.log('item:' + item);
      const details = await this.state.landList.methods.landInfoOwner(item).call();
      if (details[3] !== 'NULL') { // Check if isGovtApproved is not NULL
        this.propertyDetails(item);
      }
    }
  }
  
  render() {
    const { classes } = this.props
    return this.state.isLoading ? (
      <div style={{ position: 'absolute', top: '50%', left: '50%' }}>
        <CircularProgress />
      </div>
    ) : (
      <div className="profile-bg">
        <div className={classes.container}>
          <Container style={{ marginTop: '40px' }}>
            {/* <Button
            style={{ marginTop: '30px' }}
            variant="contained"
            color="primary"
            onClick={() => this.props.history.push('/registration_form')}
          >
            Register Land
          </Button> */}
            <div style={{ marginTop: '100px' }}>
              <Table assetList={this.state.assetList} />
            </div>
          </Container>
        </div>
      </div>
    )
  }
}
export default withStyles(styles)(Dashboard)
