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

export const CategoryList: FC = (props) => (
  <List {...props}>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="name" />
      <TextField source="color" />
      <BooleanField source="selected" />


      <ReferenceField source="image_id" reference="images">
            <TextField source="path" />
      </ReferenceField>

      <ReferenceField source="user_id" reference="users">
            <TextField source="first_name" />
      </ReferenceField>
      <EditButton />
    </Datagrid>
  </List>
);
