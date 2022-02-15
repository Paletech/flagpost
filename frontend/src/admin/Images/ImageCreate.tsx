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

    <ImageInput source="pictures" label="Related pictures" accept="image/*" placeholder={<p>Drop your file here</p>}>
        <ImageField source="pictures" title="title" />
    </ImageInput>

    </SimpleForm>
  </Create>
);
