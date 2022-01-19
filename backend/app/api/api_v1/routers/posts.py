from fastapi import APIRouter, Request, Depends, Response, encoders
import typing as t

from app import category
from app.category.schemas import CategoryBase, CategoryOut, CategoryCreate
from app.category.crud import get_all_categories, get_my_category, create_category, delete_category, edit_category

from app.db.session import get_db

from app.core.auth import get_current_active_user, get_current_active_superuser
from app.post.crud import get_all_posts, get_post, create_post, delete_post
from app.post.schemas import PostOut, PostCreate

posts_router = r = APIRouter()


@r.get(
    "/posts",
    response_model=t.List[PostOut],
)
async def post_list(
        response: Response,
        db=Depends(get_db),
        # current_user=Depends(get_current_active_superuser),
):
    """
    Get all posts
    """
    posts = get_all_posts(db)
    response.headers["Content-Range"] = f"0-9/{len(posts)}"
    return posts


@r.get(
    "/posts/{post_id}",
    response_model=PostOut,
)
async def post_details(
        request: Request,
        post_id: int,
        db=Depends(get_db),
        # current_user=Depends(get_current_active_superuser),
):
    """
    Get category by id
    """
    post = get_post(db, post_id)
    return post


@r.post(
    "/posts/create",
    response_model=PostOut,
)
async def post_create(
        request: Request,
        post: PostCreate,
        db=Depends(get_db),
        current_user=Depends(get_current_active_user),
):
    """
    Create post
    """
    return create_post(db, current_user.id, post)


@r.delete(
    "/posts/{post_id}",
)
async def post_delete(
        request: Request,
        post_id: int,
        db=Depends(get_db),
        # current_user=Depends(get_current_active_superuser),
):
    """
    Delete post
    """
    delete_post(db, post_id)
    return {"status": True}


@r.put(
    "/posts/{post_id}",
    response_model=PostOut
)
async def post_update(
        request: Request,
        post: PostCreate,
        post_id: int,
        db=Depends(get_db),
        # current_user=Depends(get_current_active_superuser),
):
    """
    Update post
    """

    return edit_category(db, post_id, post)
