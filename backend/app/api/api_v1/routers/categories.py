from fastapi import APIRouter, Request, Depends, Response, encoders
import typing as t

from app.category.schemas import CategoryBase, CategoryOut
from app.category.crud import get_all_categories, get_my_category, create_category, delete_category

from app.db.session import get_db
from app.db.crud import (
    get_users,
    get_user,
    create_user,
    delete_user,
    edit_user,
)
from app.db.schemas import UserCreate, UserEdit, User, UserOut
from app.core.auth import get_current_active_user, get_current_active_superuser

categories_router = r = APIRouter()


@r.get(
    "/categories",
    response_model=t.List[CategoryOut],
)
async def categories_list(
        response: Response,
        db=Depends(get_db),
        # current_user=Depends(get_current_active_superuser),
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
        # current_user=Depends(get_current_active_superuser),
):
    """
    Get my category
    """
    category = get_my_category(db, category_id)
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
        category_id: int,
        db=Depends(get_db),
        # current_user=Depends(get_current_active_superuser),
):
    """
    Create category
    """
    return create_category(db, category_id)


@r.delete(
    "/categories/{category_id}",
)
async def categories_delete(
        request: Request,
        category_id: int,
        db=Depends(get_db),
        # current_user=Depends(get_current_active_superuser),
):
    """
    Delete category
    """
    delete_category(db, category_id)
    return {"status": True}




# @r.put(
#     "/users/{user_id}", response_model=User, response_model_exclude_none=True
# )
# async def user_edit(
#     request: Request,
#     user_id: int,
#     user: UserEdit,
#     db=Depends(get_db),
#     current_user=Depends(get_current_active_superuser),
# ):
#     """
#     Update existing user
#     """
#     return edit_user(db, user_id, user)
#
#
# @r.delete(
#     "/users/{user_id}", response_model=User, response_model_exclude_none=True
# )
# async def user_delete(
#     request: Request,
#     user_id: int,
#     db=Depends(get_db),
#     current_user=Depends(get_current_active_superuser),
# ):
#     """
#     Delete existing user
#     """
#     return delete_user(db, user_id)
