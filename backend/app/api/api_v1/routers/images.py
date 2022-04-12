import base64
import typing as t
from uuid import UUID

from fastapi import APIRouter, Depends, Response

from app.core.auth import get_current_user
from app.core.upload_data import upload_image_to_s3, delete_file_from_s3
from app.db.session import get_db
from app.image.crud import get_all_images, get_image, delete_image, create_image
from app.image.schemas import ImageOut, ImageUpload

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
    response.headers["Content-Range"] = f"0-9/{len(images)}"
    return images


@r.get(
    "/images/{image_id}",
    response_model=ImageOut,
)
async def images_details(
        image_id: UUID,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Get image by id
    """
    image = get_image(db, image_id=image_id)
    return image


@r.post(
    "/images",
)
async def image_upload(
        # file: UploadFile = File(...),
        pictures: ImageUpload,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Upload image
    """

    img_data = pictures.pictures[0].get('src').split('base64,')[-1]
    filename = pictures.pictures[0].get('title')
    file = base64.b64decode(img_data)

    url = await upload_image_to_s3(file=file, filename=filename)
    create_image(db, url)
    return url


@r.delete(
    "/images/{image_id}",
)
async def image_delete(
        image_id: UUID,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Delete image
    """

    image = get_image(db, image_id)
    await delete_file_from_s3(image.path)
    delete_image(db, image=image)
    return {"status": True}
