import React, { FC } from 'react';
import {
  Edit,
  SimpleForm,
  TextInput,
  ReferenceInput,
  SelectInput,
  ReferenceArrayInput,
  SelectArrayInput
} from 'react-admin';

// import { ReferenceManyToManyInput, useReferenceManyToManyUpdate } from '@react-admin/ra-many-to-many';
export const PostEdit: FC = (props) => (
  <Edit {...props}>
    <SimpleForm>
      <TextInput disabled source="id" />
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
  </Edit>
);
