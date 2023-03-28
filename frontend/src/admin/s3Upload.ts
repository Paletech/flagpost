import {getS3} from "../utils";
const { v4 } = require('uuid');

export const uploadToS3 = async (file: File, filename: string, bucket: string) =>{
    const s3 = await getS3();
    const params = {
      Bucket: bucket,
      Key: filename,
      Body: file,
    };

   await s3.putObject(params).promise()
}
export const setFileName = (userId: string | null, file: File) => {
    const now = new Date();
    const folderFromNow = `/${now.getFullYear()}/${now.getMonth() + 1}/${now.getDate()}/`;
    return `${userId}${folderFromNow}${v4()}${file.name}`;
  }