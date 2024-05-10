// const axios = require("axios");
// const FormData = require("form-data");
// const fs = require("fs");

// const JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiI5NDgwOTY3MS0wMzVjLTRiNjktYjRmNS0zMTkyODI3ZDM5NDEiLCJlbWFpbCI6ImthbWlsaGFkMTIzQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaW5fcG9saWN5Ijp7InJlZ2lvbnMiOlt7ImlkIjoiRlJBMSIsImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxfSx7ImlkIjoiTllDMSIsImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxfV0sInZlcnNpb24iOjF9LCJtZmFfZW5hYmxlZCI6ZmFsc2UsInN0YXR1cyI6IkFDVElWRSJ9LCJhdXRoZW50aWNhdGlvblR5cGUiOiJzY29wZWRLZXkiLCJzY29wZWRLZXlLZXkiOiJjZWQ0MmYyMGNmZGY2OTllOTU1YSIsInNjb3BlZEtleVNlY3JldCI6Ijc0MjdjNDk2MmZlNDhlNTE1MmJhMjBmODJhYTllMDZiNzU4NmYxMWRkMWQ4ZGEwMTFlNGU3Y2ZkMGQ0MTdiYzQiLCJpYXQiOjE3MTIyMDk0NzN9.BMLZp5YoE3KUQQ-PDfdrW2_ESEMsesqExRdld5T1K0c";

// function UploadForm() {
//   const [file, setFile] = useState(null);

//   const handleFileChange = (event) => {
//     if (event.target.files && event.target.files.length > 0) {
//       setFile(event.target.files[0]);
//     }
//   };

//   const handleUpload = async () => {
//     if (!file) {
//       console.log("No file selected");
//       return;
//     }

//     try {
//       const formData = new FormData();
//       formData.append("file", file);

//       const pinataMetadata = JSON.stringify({
//         name: file.name,
//       });
//       formData.append("pinataMetadata", pinataMetadata);

//       const pinataOptions = JSON.stringify({
//         cidVersion: 1,
//       });
//       formData.append("pinataOptions", pinataOptions);

//       const res = await axios.post(
//         "https://api.pinata.cloud/pinning/pinFileToIPFS",
//         formData,
//         {
//           headers: {
//             Authorization: `Bearer ${JWT}`,
//             ...formData.getHeaders(), // Include form-data headers
//           },
//         }
//       );
//       console.log(res.data);
//     } catch (error) {
//       console.log("Error:", error);
//     }
//   };

//   return (
//     <div>
//       <input type="file" onChange={handleFileChange} />
//       <button onClick={handleUpload}>Upload</button>
//     </div>
//   );
// }

// export default UploadForm;

// Import React if JSX is used
import React, { useState } from 'react';
import axios from 'axios';

const JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiI5NDgwOTY3MS0wMzVjLTRiNjktYjRmNS0zMTkyODI3ZDM5NDEiLCJlbWFpbCI6ImthbWlsaGFkMTIzQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaW5fcG9saWN5Ijp7InJlZ2lvbnMiOlt7ImlkIjoiRlJBMSIsImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxfSx7ImlkIjoiTllDMSIsImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxfV0sInZlcnNpb24iOjF9LCJtZmFfZW5hYmxlZCI6ZmFsc2UsInN0YXR1cyI6IkFDVElWRSJ9LCJhdXRoZW50aWNhdGlvblR5cGUiOiJzY29wZWRLZXkiLCJzY29wZWRLZXlLZXkiOiJjZWQ0MmYyMGNmZGY2OTllOTU1YSIsInNjb3BlZEtleVNlY3JldCI6Ijc0MjdjNDk2MmZlNDhlNTE1MmJhMjBmODJhYTllMDZiNzU4NmYxMWRkMWQ4ZGEwMTFlNGU3Y2ZkMGQ0MTdiYzQiLCJpYXQiOjE3MTIyMDk0NzN9.BMLZp5YoE3KUQQ-PDfdrW2_ESEMsesqExRdld5T1K0c";

function UploadForm() {
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    if (event.target.files && event.target.files.length > 0) {
      setFile(event.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      console.log("No file selected");
      return;
    }
  
    try {
      const formData = new FormData();
      formData.append("file", file);
  
      const pinataMetadata = JSON.stringify({
        name: file.name,
      });
      formData.append("pinataMetadata", pinataMetadata);
  
      const pinataOptions = JSON.stringify({
        cidVersion: 1,
      });
      formData.append("pinataOptions", pinataOptions);
  
      const res = await axios.post(
        "https://api.pinata.cloud/pinning/pinFileToIPFS",
        formData,
        {
          headers: {
            Authorization: `Bearer ${JWT}`,
            "Content-Type": "multipart/form-data", // Specify content type for form data
          },
        }
      );
      console.log(res.data);
    } catch (error) {
      console.log("Error:", error);
    }
  };
  
  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
    </div>
  );
}

export default UploadForm;

