import React, { FC } from 'react';
import {
  Create,
  SimpleForm,
  TextInput,
  ReferenceArrayInput,
  SelectArrayInput

} from 'react-admin';

export const PostCreate: FC = (props) => (
  <Create {...props}>
    <SimpleForm>
      <TextInput source="type" />
      <TextInput source="text" />

      <ReferenceArrayInput source="categories" reference="categories">
            <SelectArrayInput optionText="name" />
      </ReferenceArrayInput>

      <ReferenceArrayInput source="files" reference="files">
            <SelectArrayInput optionText="id" />
      </ReferenceArrayInput>

    </SimpleForm>
  </Create>
);
