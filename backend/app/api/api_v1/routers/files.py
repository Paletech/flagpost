import typing as t
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File, Response

from app.core.auth import get_current_user
from app.core.upload_data import upload_to_s3
from app.db.session import get_db
from app.files.crud import get_all_files, get_file, create_file, delete_file
from app.files.schemas import FileOut

files_router = r = APIRouter()


@r.get(
    "/files",
    response_model=t.List[FileOut],
)
async def files_list(
        response: Response,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Get all files
    """
    files = get_all_files(db)
    response.headers["Content-Range"] = f"0-9/{len(files)}"
    return files


@r.get(
    "/files/{file_id}",
    response_model=FileOut,
)
async def files_details(
        file_id: UUID,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Get files by id
    """
    file = get_file(db, file_id=file_id)
    return file


@r.post(
    "/upload_file/{post_id}",
)
async def post_upload_file(
        post_id: UUID,
        file: UploadFile = File(...),
        db=Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Upload file
    """
    response = await upload_to_s3(file=file, user=current_user, post_id=post_id)
    path = response.pop('data_for_base')
    create_file(db, post_id=post_id, path=path)
    return response['response']['fields']


@r.delete(
    "/files/{file_id}",
)
async def file_delete(
        file_id: UUID,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Delete file
    """
    delete_file(db, file=file_id, user_id=current_user)
    return {"status": True}
