import typing as t
from uuid import UUID

from fastapi import APIRouter, Request, Depends, Response, UploadFile, File

from app.core.auth import get_current_user
from app.core.s3_upload.files import FileS3Manager
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
        request: Request,
        file_id: UUID,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Get files by id
    """
    file = get_file(db, file_id)
    return file


# @r.post(
#     "/files/create",
#     response_model=FileOut,
# )
# async def file_create(
#         request: Request,
#         file: FileCreate,
#         db=Depends(get_db),
#         current_user=Depends(get_current_user),
# ):
#     """
#     Create file
#     """
#     return create_file(db, file)


@r.post(
    "/files",
)
async def post_upload_file(
        # request: Request,
        # post_id: t.Union[UUID, None],
        file: UploadFile = File(...),
        db=Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Upload file
    """
    manager = FileS3Manager(user=current_user)
    path = await manager.upload(file=file)
    # file = create_file(db, None, path)
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
    delete_file(db, file_id)
    return {"status": True}
