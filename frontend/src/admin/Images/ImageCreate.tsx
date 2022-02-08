import React, { FC } from 'react';
import {
  Create,
  SimpleForm,
  ImageInput,
  ImageField,
} from 'react-admin';

export const ImageCreate: FC = (props) => (
  <Create {...props}>
    <SimpleForm>

    <ImageInput source="file" label="Related pictures" accept="image/*" placeholder={<p>Drop your file here</p>}>
        <ImageField source="src" title="title" />
    </ImageInput>


    </SimpleForm>
  </Create>
);
