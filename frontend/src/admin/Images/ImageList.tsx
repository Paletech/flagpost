// in src/users.js
import React, {FC} from 'react';
import {Datagrid, EditButton, ImageField, List, TextField} from 'react-admin';
import {Button} from "@material-ui/core";
const url = require('url');
const AWS = require('../../utils/auth')
export const ImageList: FC = (props) =>{
    const getImageFromS3 = async () => {
        const objectUrl = `https://s3.us-east-1.amazonaws.com/flagpost-images/eb39f01b84fb4df39de671340fffca5d/2023/3/24/23115d506eff445a87b717004f36f12f.jpg`
        const { host, pathname } = url.parse(objectUrl);
        const bucketName = host.split('.')[0];
        const objectKey = pathname.substring(1);

        // Use the S3 client to get the object
        const s3 = new AWS.S3();
        let a =  s3.getObject({ Bucket: bucketName, Key: objectKey });
        console.log(a)

    }

 return (
  <List {...props}>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <ImageField
          source='path' 
      />
        <Button onClick={getImageFromS3}></Button>
      <EditButton />
    </Datagrid>
  </List>
);
}

