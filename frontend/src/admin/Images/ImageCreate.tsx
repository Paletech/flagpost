import React, {FC, useState} from 'react';
import {BASE_URL} from "../../config";
import {Button} from "@material-ui/core";
import {setFileName, uploadToS3} from "../s3Upload";

export const ImageCreate: FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const sendImageDataToAPI = async (filename: string) => {
    const token = localStorage.getItem("token")
    const response = await fetch(BASE_URL + 'api/v1/images', {
      method: 'POST',
      headers: {
        "Authorization": `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        path: filename
      })
      });
  }

  const handleUpload = async () => {
    const userId = localStorage.getItem('userId')
    if (selectedFile) {
      const filename = setFileName(userId, selectedFile)
      await uploadToS3(selectedFile, filename, 'flagpost-images')
      await sendImageDataToAPI(filename)
  }
  }

    return (
        <div>
        <input type="file" onChange={handleFileChange} />
        <Button onClick={handleUpload}>Upload</Button>
      </div>)
};