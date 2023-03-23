import React, {FC, useState} from 'react';
import {
  Create,
  SimpleForm,
  ImageInput,
    InputImage,
  ImageField,
} from 'react-admin';
import {BASE_URL} from "../../config";
import {Button} from "@material-ui/core";

export const ImageCreate: FC = (props) => {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (selectedFile) {
      const formData = new FormData();
      formData.append('file', selectedFile);
      const token = localStorage.getItem("token")
      const response = await fetch(BASE_URL + 'api/v1/images', {
        method: 'POST',
        headers: {
          "Authorization": `Bearer ${token}`
        },
        body: formData
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }
    }
  };

    return (
        <div>
        <input type="file" onChange={handleFileChange} />
        <Button onClick={handleUpload}>Upload</Button>
      </div>)
}