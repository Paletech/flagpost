// in src/users.js
import React, { FC } from 'react';
import {
  List,
  Datagrid,
  TextField,
  BooleanField,
  EditButton,
} from 'react-admin';

export const FileList: FC = (props) => (
  <List {...props}>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="width" />
      <TextField source="height" />
      <TextField source="path" />
      <BooleanField source="public_path" />
      <EditButton />
    </Datagrid>
  </List>
);
