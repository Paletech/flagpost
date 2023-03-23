// in src/users.js
import React, { FC } from 'react';
import {
  List,
  Datagrid,
  TextField,
  BooleanField,
  EmailField,
  EditButton,
    ImageField
} from 'react-admin';

export const ImageList: FC = (props) =>{

 return (
  <List {...props}>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <ImageField
          source="path"
      />
      <EditButton />
    </Datagrid>
  </List>
);
}

