import typing as t
from uuid import UUID

from fastapi import APIRouter, Depends, File, Request, Response, UploadFile

from app.core.auth import get_current_user
from app.core.s3.upload.files import FileS3Manager
from app.db.session import get_db
from app.files.crud import create_file, delete_file, get_all_files, get_file
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
    files = await get_all_files(db)
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = f"0-9/{len(files)}"
    return files


@r.get(
    "/files/{file_id}",
    response_model=FileOut,
)
async def files_details(
        request: Request,
        file_id: UUID,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Get files by id
    """
    file = await get_file(db, file_id)
    return file


@r.post(
    "/posts/{post_id}/files",
)
async def post_upload_file(
        # request: Request,
        post_id: UUID,
        file: UploadFile = File(...),
        db=Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Upload file
    """
    path = "as"# await FileS3Manager(user=current_user).upload(file=file)
    file = await create_file(db, post_id, path)
    return file


@r.delete(
    "/files/{file_id}",
)
async def file_delete(
        request: Request,
        file_id: UUID,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Delete file
    """
    await delete_file(db, file_id)
    # await FileS3Manager(user=current_user).delete(file)
    return {"status": True}
