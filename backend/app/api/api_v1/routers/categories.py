from uuid import UUID

from fastapi import APIRouter, Request, Depends, Response, encoders
import typing as t

from app.category.schemas import CategoryBase, CategoryOut, CategoryCreate, CategoryEdit
from app.category.crud import get_all_categories, get_my_category, create_category, delete_category, edit_category, \
    get_category

from app.db.session import get_db

from app.core.auth import get_current_active_user, get_current_active_superuser, get_current_user

categories_router = r = APIRouter()


@r.get(
    "/categories",
    response_model=t.List[CategoryOut],
    # response_model=CategoryOut,
)
async def categories_list(
        response: Response,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
        skip: int = 0,
        limit: int = 10
):
    """
    Get all categories
    """
    category = get_all_categories(db, skip, limit)
    response.headers["Content-Range"] = f"0-9/{len(category)}"
    return category


@r.get(
    "/categories/{category_id}",
    response_model=CategoryOut,
)
async def category_details(
        request: Request,
        category_id: UUID,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Get category details
    """
    return get_category(db, category_id)


@r.get(
    "/categories/my/",
    response_model=t.List[CategoryOut],
)
async def categories_details(
        request: Request,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
        skip: int = 0,
        limit: int = 10
):
    """
    Get my category
    """

    category = get_my_category(db, skip, limit, user_id=current_user)
    return category


# @r.post(
#     "/categories",
#     response_model=CategoryOut,
# )
# async def category_choose(
#         request: Request,
#         category_id: int,
#         db=Depends(get_db),
#         current_user=Depends(get_current_active_superuser),
# ):
#     """
#     Choose category
#     """
#     return choose_category(db, category_id)


@r.post(
    "/categories",
    response_model=CategoryOut,
)
async def category_create(
        request: Request,
        category: CategoryCreate,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Create category
    """
    return create_category(db, current_user.id, category)


@r.delete(
    "/categories/{category_id}",  response_model=CategoryOut, response_model_exclude_none=True
)
async def categories_delete(
        request: Request,
        category_id: UUID,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Delete category
    """

    return delete_category(db, category_id)


@r.put(
    "/categories/{category_id}",
    response_model=CategoryOut
)
async def categories_update(
        request: Request,
        category: CategoryEdit,
        category_id: UUID,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Update category
    """

    return edit_category(db, category_id, category)

