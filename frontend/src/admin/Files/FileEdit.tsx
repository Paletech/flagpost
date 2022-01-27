import React, { FC } from 'react';
import {
  Edit,
  SimpleForm,
  TextInput,

} from 'react-admin';

export const FileEdit: FC = (props) => (
  <Edit {...props}>
    <SimpleForm>
      <TextInput disabled source="id" />
      <TextInput source="width" />
      <TextInput source="height" />
      <TextInput source="path" />
      <TextInput source="public_path" />

    </SimpleForm>
  </Edit>
);
