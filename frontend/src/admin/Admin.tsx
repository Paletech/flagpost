import React, { FC } from 'react';
import { fetchUtils, Admin as ReactAdmin, Resource } from 'react-admin';
import simpleRestProvider from 'ra-data-simple-rest';
import authProvider from './authProvider';

import { CategoryList, CategoryEdit, CategoryCreate } from './Categories';
import { PostList, PostEdit, PostCreate } from './Posts';
import { UserList, UserEdit, UserCreate } from './Users';
import { FileList, FileCreate, FileEdit } from './Files';

const httpClient = (url: any, options: any) => {
  if (!options) {
    options = {};
  }
  if (!options.headers) {
    options.headers = new Headers({ Accept: 'application/json' });
  }
  const token = localStorage.getItem('token');
  options.headers.set('Authorization', `Bearer ${token}`);
  return fetchUtils.fetchJson(url, options);
};

const dataProvider = simpleRestProvider('api/v1', httpClient);

export const Admin: FC = () => {
  return (
    <ReactAdmin dataProvider={dataProvider} authProvider={authProvider}>
      {(permissions: 'admin' | 'user') => [
        permissions === 'admin' ? (
          <Resource
            name="users"
            list={UserList}
            edit={UserEdit}
            create={UserCreate}
        />
        ) : null,
        permissions === 'admin' ? (
          <Resource
            name="categories"
            list={CategoryList}
            edit={CategoryEdit}
            create={CategoryCreate}
        />
        ) : null,

          permissions === 'admin' ? (
          <Resource
            name="posts"
            list={PostList}
            edit={PostEdit}
            create={PostCreate}
        />
        ) : null,

          permissions === 'admin' ? (
          <Resource
            name="files"
            list={FileList}
            edit={FileEdit}
            create={FileCreate}
        />
        ) : null,

           permissions === 'admin' ? (
          <Resource
            name="images"
        />
        ) : null,


      ]}
    </ReactAdmin>
  );
};
