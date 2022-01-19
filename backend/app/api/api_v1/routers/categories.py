from fastapi import APIRouter, Request, Depends, Response, encoders
import typing as t

from app.category.schemas import CategoryBase, CategoryOut, CategoryCreate, CategoryEdit
from app.category.crud import get_all_categories, get_my_category, create_category, delete_category, edit_category

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
):
    """
    Get all categories
    """
    category = get_all_categories(db)
    response.headers["Content-Range"] = f"0-9/{len(category)}"
    return category


@r.get(
    "/categories/{category_id}",
    response_model=CategoryOut,
)
async def categories_details(
        request: Request,
        category_id: int,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Get my category
    """

    category = get_my_category(db, category_id, current_user)
    return category


# @r.post(
#     "/categories",
#     response_model=CategoryOut,
# )
# async def category_choose(
#         request: Request,
#         category_id: int,
#         db=Depends(get_db),
#         # current_user=Depends(get_current_active_superuser),
# ):
#     """
#     Choose category
#     """
#     return choose_category(db, category_id)


@r.post(
    "/categories/create",
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
    "/categories/{category_id}",
)
async def categories_delete(
        request: Request,
        category_id: int,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Delete category
    """
    delete_category(db, current_user, category_id)
    return {"status": True}


@r.put(
    "/categories/{category_id}",
    response_model=CategoryOut
)
async def categories_update(
        request: Request,
        category: CategoryEdit,
        category_id: int,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Update category
    """

    return edit_category(db, current_user, category_id, category)
