// in src/users.js
import React, { FC } from 'react';
import {
  List,
  Datagrid,
  TextField,
  BooleanField,
  EmailField,
  EditButton,
  ReferenceField
} from 'react-admin';

export const PostList: FC = (props) => (
  <List {...props}>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="type" />
      <TextField source="text" />

      <ReferenceField source="user_id" reference="users">
            <TextField source="first_name" />
      </ReferenceField>

      <EditButton />
    </Datagrid>
  </List>
);
