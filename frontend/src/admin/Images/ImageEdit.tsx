import React, { FC } from 'react';
import {
  Edit,
  SimpleForm,
  TextInput,

} from 'react-admin';

export const ImageEdit: FC = (props) => (
  <Edit {...props}>
    <SimpleForm>
      <TextInput source="path" />
      <TextInput source="public_path" />

    </SimpleForm>
  </Edit>
);
