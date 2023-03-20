import typing as t
from uuid import UUID

from fastapi import APIRouter, Request, Depends, Response

from app.core.auth import get_current_user
from app.db.session import get_db
from app.post.crud import get_all_posts, get_post, create_post, delete_post, edit_post
from app.post.schemas import PostOut, PostCreate

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
    response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    response.headers["Content-Range"] = f"0-9/{len(posts)}"
    return posts


@r.get(
    "/posts/{post_id}",
    response_model=PostOut,
)
async def post_details(
        request: Request,
        post_id: UUID,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Get category by id
    """
    post = get_post(db, post_id)
    return post


@r.post(
    "/posts",
    response_model=PostOut,
    status_code=201
)
async def post_create(
        request: Request,
        post: PostCreate,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
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
        post_id: UUID,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Delete post
    """
    delete_post(db, current_user, post_id)
    return {"status": True}


@r.put(
    "/posts/{post_id}",
    response_model=PostOut
)
async def post_update(
        request: Request,
        post: PostCreate,
        post_id: UUID,
        db=Depends(get_db),
        current_user=Depends(get_current_user),
):
    """
    Update post
    """

    return edit_post(db, current_user, post_id, post)
