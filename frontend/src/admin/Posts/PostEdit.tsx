import React, { FC } from 'react';
import {
  Edit,
  SimpleForm,
  TextInput,
  ReferenceArrayInput,
  SelectArrayInput
  
} from 'react-admin';

export const PostEdit: FC = (props) => (
  <Edit {...props}>
    <SimpleForm>
      <TextInput disabled source="id" />
      <TextInput source="type" />
      <TextInput source="text" />

{/*       <ReferenceArrayInput source="categories_id" reference="categories"> */}
{/*             <SelectArrayInput optionText="name" /> */}
{/*       </ReferenceArrayInput> */}

{/*       <ReferenceArrayInput label="files" source="file" reference="files" > */}
{/*             <SelectArrayInput optionText="id" /> */}
{/*       </ReferenceArrayInput> */}

{/*        <ReferenceInput label="Image" source="image_id" reference="images"> */}
{/*             <SelectInput optionText="path" /> */}
{/*       </ReferenceInput> */}


{/*       <ReferenceArrayInput source="categories" reference="categories"> */}
{/*             <SelectArrayInput optionText="id" /> */}
{/*       </ReferenceArrayInput> */}

      <ReferenceArrayInput source="files" reference="files">
            <SelectArrayInput optionText="id" />
      </ReferenceArrayInput>

    </SimpleForm>
  </Edit>
);
