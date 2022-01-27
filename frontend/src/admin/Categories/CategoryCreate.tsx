import React, { FC } from 'react';
import {
  Create,
  SimpleForm,
  TextInput,
  BooleanInput,
  ReferenceInput,
  SelectInput,

  ReferenceField,
  TextField

} from 'react-admin';

export const CategoryCreate: FC = (props) => (
  <Create {...props}>
    <SimpleForm>
      <TextInput source="name" />
      <TextInput source="color" />
      <BooleanInput source="selected" />

      <ReferenceInput source="user_id" reference="users">
            <SelectInput optionText="first_name" />
      </ReferenceInput>

      <ReferenceInput label="Image" source="image_id" reference="categories">
            <SelectInput optionText="image.path" />
      </ReferenceInput>


    </SimpleForm>
  </Create>
);
