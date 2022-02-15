import React, { FC } from 'react';
import {
  Edit,
  SimpleForm,
  TextInput,
  BooleanInput,
  ReferenceInput,
  SelectInput
  
} from 'react-admin';

export const CategoryEdit: FC = (props) => (
  <Edit {...props}>
    <SimpleForm>
      <TextInput disabled source="id" />
      <TextInput source="name" />
      <TextInput source="color" />
      <BooleanInput source="selected" />

      <ReferenceInput source="user_id" reference="users">
            <SelectInput optionText="first_name" />
      </ReferenceInput>

      <ReferenceInput label="Image" source="image_id" reference="images">
            <SelectInput optionText="path" />
      </ReferenceInput>
    </SimpleForm>
  </Edit>
);
