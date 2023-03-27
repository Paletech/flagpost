import React, {FC, useState} from 'react';
import {BASE_URL} from "../../config";
import {Button} from "@material-ui/core";
import {getS3} from "../../utils";
const { v4 } = require('uuid');


export const ImageCreate: FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setSelectedFile(event.target.files[0]);
    }
  };
  const setImageName = (user_id: string | null, file: File) => {
    const now = new Date();
    const folderFromNow = `/${now.getFullYear()}/${now.getMonth() + 1}/${now.getDate()}/`;
    return `${user_id}${folderFromNow}${v4()}${file.name}`;
  }
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
  const uploadToS3 = async (file: File, filename: string) =>{
    const s3 = await getS3();
    const params = {
      Bucket: 'flagpost-images',
      Key: filename,
      Body: file,
    };

   await s3.putObject(params).promise()
  }
  const handleUpload = async () => {
    const userId = localStorage.getItem('userId')
    if (selectedFile) {
      const filename = setImageName(userId, selectedFile)
      await uploadToS3(selectedFile, filename)
      await sendImageDataToAPI(filename)
  }
  }

    return (
        <div>
        <input type="file" onChange={handleFileChange} />
        <Button onClick={handleUpload}>Upload</Button>
      </div>)
};