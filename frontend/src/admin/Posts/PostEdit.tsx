import React, { FC } from 'react';
import {
  Edit,
  SimpleForm,
  TextInput,
  PasswordInput,
  BooleanInput,
  ReferenceInput,
  SelectInput,
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

{/*       <ReferenceManyToManyInput */}
{/*                 source="category_id" */}
{/*                 reference="categories" */}
{/*                 through="association_table" */}
{/*                 using="category_id,post_id" */}
{/*                 fullWidth */}
{/*                 label="Categories" */}
{/*             > */}
{/*                 <SelectArrayInput optionText="name" /> */}
{/*             </ReferenceManyToManyInput> */}

       <ReferenceInput source="file_id" reference="files">
            <SelectInput optionText="path" />
      </ReferenceInput>

    </SimpleForm>
  </Edit>
);
