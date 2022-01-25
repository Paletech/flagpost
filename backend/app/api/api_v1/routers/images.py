import typing as t

from fastapi import APIRouter, Depends, Response

from app.db.session import get_db
from app.image.crud import get_all_images
from app.image.schemas import ImageOut

images_router = r = APIRouter()


@r.get(
    "/images",
    response_model=t.List[ImageOut],
)
async def post_list(
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
