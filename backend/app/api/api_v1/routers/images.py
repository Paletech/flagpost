import typing as t
from uuid import UUID

from app.core.auth import get_current_user
from app.core.s3_upload.images import ImageS3Manager
from app.db.session import get_db
from app.image.crud import (create_image, delete_image, get_all_images,
                            get_image)
from app.image.schemas import ImageOut
from fastapi import APIRouter, Depends, File, Request, Response, UploadFile

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
    response_model=ImageOut
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
    manager = ImageS3Manager(user=current_user)
    path = await manager.upload(file=file)
    image = create_image(db=db, path=path)
    return image


@r.delete(
    "/images/{image_id}",
    status_code=200
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
    image = delete_image(db, image_id)
    await ImageS3Manager(user=current_user).delete(image)
    return {"status": True}
