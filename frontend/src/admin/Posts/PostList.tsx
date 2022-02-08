// in src/users.js
import React, { FC } from 'react';
import {
  List,
  Datagrid,
  TextField,
  BooleanField,
  EmailField,
  EditButton,
  ReferenceField,
  SingleFieldList,
  ChipField,
  ReferenceManyField,

} from 'react-admin';

export const PostList: FC = (props) => (
  <List {...props}>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="type" />
      <TextField source="text" />

    <ReferenceManyField label="File" reference="files" target="post_id">
        <SingleFieldList>
            <ChipField source="id" />
        </SingleFieldList>
    </ReferenceManyField>

      <EditButton />
    </Datagrid>
  </List>
);
