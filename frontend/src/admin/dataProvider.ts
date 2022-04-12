import simpleRestProvider from 'ra-data-simple-rest';
import { fetchUtils, Admin as ReactAdmin, Resource } from 'react-admin';

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

const myDataProvider = {
    ...dataProvider,
    create: (resource, params) => {
        console.log('1')
        if (resource !== 'images' || !params.data.pictures) {
            // fallback to the default implementation
            return dataProvider.create(resource, params);
//             return dataProvider
        }
        console.log('2')

        let newDataFormat = [params.data.pictures]
        /**
         * For posts update only, convert uploaded image in base 64 and attach it to
         * the `picture` sent property, with `src` and `title` attributes.
         */
        // Freshly dropped pictures are File objects and must be converted to base64 strings
        const newPictures = newDataFormat.filter(
            p => p.rawFile instanceof File,
        );

        const formerPictures = newDataFormat.filter(
            p => !(p.rawFile instanceof File)
        );

        return Promise.all(newPictures.map(convertFileToBase64))
            .then(base64Pictures =>
                base64Pictures.map(picture64 => ({
                    src: picture64,
                    title: `${params.data.pictures.title}`,
                }))
            )
            .then(transformedNewPictures =>
                dataProvider.create(resource, {
                    ...params,
                    data: {
                        ...params.data,
                        pictures: [
                            ...transformedNewPictures,
                            ...formerPictures,
                        ],
                    },
                })
            );
    },
};

/**
 * Convert a `File` object returned by the upload input into a base 64 string.
 * That's not the most optimized way to store images in production, but it's
 * enough to illustrate the idea of data provider decoration.
 */
// const convertFileToBase64 = file =>
//     new Promise((resolve, reject) => {
//         const reader = new FileReader();
//         reader.onload = () => resolve(reader.result);
//         reader.onerror = reject;
//
//         reader.readAsDataURL(file.rawFile);
//     });


const convertFileToBase64 = file => new Promise((resolve, reject) => {
  const reader = new FileReader();
  reader.readAsDataURL(file.rawFile);

  reader.onload = () => resolve(reader.result);
  reader.onerror = reject;
});

const addUploadFeature = requestHandler => (type, resource, params) => {

  if (type === 'UPDATE' && resource === 'myResource') {

      if (params.data.myFile) {

          // NEW CODE HERE (to upload just one file):
          const myFile = params.data.myFile;
          if ( !(myFile.rawFile instanceof File) ){
              return Promise.reject('Error: Not a file...'); // Didn't test this...
          }

          return Promise.resolve( convertFileToBase64(myFile) )
              .then( (picture64) => ({
                  src: picture64,
                  title: `${myFile.title}`
              }))
              .then( transformedMyFile => requestHandler(type, resource, {
                  ...params,
                  data: {
                      ...params.data,
                      myFile: transformedMyFile
                  }
              }));
      }
  }
  return requestHandler(type, resource, params);
};


// export default addUploadFeature;

export default myDataProvider;
// export default dataProvider;