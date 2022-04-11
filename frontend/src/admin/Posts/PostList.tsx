// in src/users.js
import React, { FC } from 'react';
import {
  List,
  Datagrid,
  TextField,
  EditButton,
  ReferenceField,
  ArrayField


} from 'react-admin';

export const PostList: FC = (props) => (
  <List {...props}>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="type" />
      <TextField source="text" />

      <ReferenceField source="user_id" reference="users" label="User Name">
            <TextField source="first_name" />
      </ReferenceField>

    <ArrayField source="categories">
        <Datagrid>
            <TextField source="id" />
            <TextField source="name" />
         </Datagrid>
    </ArrayField>


    <ArrayField source="files">
        <Datagrid>
            <TextField source="id" />
        </Datagrid>
    </ArrayField>

{/*      <EditButton /> */}
    </Datagrid>
  </List>
);
