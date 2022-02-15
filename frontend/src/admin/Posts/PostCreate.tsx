import React, { FC } from 'react';
import {
  Create,
  SimpleForm,
  TextInput,
  ReferenceInput,
  SelectInput,
  ReferenceArrayInput,
  SelectArrayInput

} from 'react-admin';

export const PostCreate: FC = (props) => (
  <Create {...props}>
    <SimpleForm>
      <TextInput source="type" />
      <TextInput source="text" />

      <ReferenceInput source="user_id" reference="users">
            <SelectInput optionText="first_name" />
      </ReferenceInput>
       <ReferenceInput source="category_id" reference="categories">
            <SelectInput optionText="name" />
      </ReferenceInput>

      <ReferenceArrayInput source="file_id" reference="files">
            <SelectArrayInput optionText="id" />
      </ReferenceArrayInput>


    </SimpleForm>
  </Create>
);
