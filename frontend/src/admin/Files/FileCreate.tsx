import React, { FC } from 'react';
import {
  Create,
  SimpleForm,
  TextInput,
} from 'react-admin';

export const FileCreate: FC = (props) => (
  <Create {...props}>
    <SimpleForm>
      <TextInput source="width" />
      <TextInput source="height" />
      <TextInput source="path" />
      <TextInput source="public_path" />

    </SimpleForm>
  </Create>
);
