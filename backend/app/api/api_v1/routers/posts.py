import typing as t
from uuid import UUID

from fastapi import APIRouter, Depends, Response

from app.core.auth import get_current_user
from app.db.session import get_db
from app.post.crud import get_all_posts, get_post, create_post, delete_post, edit_post
from app.post.schemas import PostOut, PostCreate, PostEdit

posts_router = r = APIRouter()


@r.get(
    "/posts",
    response_model=t.List[PostOut],
)
async def post_list(
        response: Response,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
        skip: int = 0, limit: int = 10
):
    """
    Get all posts
    """
    posts = get_all_posts(db, skip, limit)
    response.headers["Content-Range"] = f"0-9/{len(posts)}"
    return posts


@r.get(
    "/posts/{post_id}",
    response_model=PostOut,
)
async def post_details(
        post_id: UUID,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Get category by id
    """
    post = get_post(db, post_id=post_id)
    return post


@r.post(
    "/posts",
    response_model=PostOut,
)
async def post_create(
        post: PostCreate,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Create post
    """
    return create_post(db, user_id=current_user.id, post=post)


@r.delete(
    "/posts/{post_id}",
)
async def post_delete(
        post_id: UUID,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Delete post
    """
    delete_post(db, user_id=current_user, post_id=post_id)
    return {"status": True}


@r.put(
    "/posts/{post_id}",
    response_model=PostOut
)
async def post_update(
        post: PostEdit,
        post_id: UUID,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Update post
    """
    return edit_post(db, user_id=current_user, post_id=post_id, post=post)
