import typing as t
from uuid import UUID

from fastapi import APIRouter, Depends, Response, Request, UploadFile, File

from app.core.auth import get_current_user
from app.db.session import get_db
from app.image.crud import get_all_images, get_image, delete_image
from app.image.schemas import ImageOut

images_router = r = APIRouter()


@r.get(
    "/images",
    response_model=t.List[ImageOut],
)
async def image_list(
        response: Response,
        db=Depends(get_db),
        # current_user=Depends(get_current_user),
):
    """
    Get all images
    """
    images = get_all_images(db)
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = f"0-9/{len(images)}"
    return images


@r.get(
    "/images/{image_id}",
    response_model=ImageOut,
)
async def images_details(
        request: Request,
        image_id: UUID,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Get image by id
    """
    image = get_image(db, image_id)
    return image


@r.post(
    "/images",
)
async def image_upload(
        # request: Request,
        file: UploadFile = File(...),
        # file: str,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Upload image
    """
    # response = upload_to_s3(file, current_user, post_id)
    # path = response.pop('data_for_base')
    # create_file(db, post_id, path)

    file_location = f"files/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    # return image


@r.delete(
    "/images/{image_id}",
)
async def image_delete(
        request: Request,
        image_id: UUID,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Delete image
    """
    delete_image(db, image_id)
    return {"status": True}
