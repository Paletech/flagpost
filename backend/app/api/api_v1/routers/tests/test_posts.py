from app.db.models import Posts


def test_unauthenticated_all_posts_routers(client):
    """Test checks authentication for all posts routers."""
    response = client.get("/api/v1/posts")
    assert response.status_code == 401
    response = client.get("/api/v1/posts/b21706cd-df99-490f-aa4f-7efa418b1343")
    assert response.status_code == 401
    response = client.post("/api/v1/posts")
    assert response.status_code == 401
    response = client.delete("/api/v1/posts/b21706cd-df99-490f-aa4f-7efa418b1343")
    assert response.status_code == 401
    response = client.put("/api/v1/posts/b21706cd-df99-490f-aa4f-7efa418b1343")
    assert response.status_code == 401


def test_get_list_posts(client, user_token_headers):
    """Test for get list of posts."""
    response = client.get("/api/v1/posts", headers=user_token_headers)
    assert response.status_code == 200


def test_retrieve_post_by_id(client, user_token_headers, test_post):
    """Test for retrieve post by id."""
    response = client.get(f"/api/v1/posts/{test_post.id}", headers=user_token_headers)
    assert response.status_code == 200


def test_retrieve_post_with_wrong_id(client, user_token_headers):
    """Test for retrieve post with wrong id."""
    response = client.get("/api/v1/posts/b21706cd-df99-490f-aa4f-7efa418b1343", headers=user_token_headers)
    assert response.status_code == 404


def test_create_post(client, user_token_headers, test_user):
    """Test for creating new post."""
    post = {
        "type": "type",
        "text": "text",
        "user_id": str(test_user.id),
    }
    response = client.post('/api/v1/posts', headers=user_token_headers, json=post)
    assert response.status_code == 200


def test_delete_post(client, superuser_token_headers, test_post, test_db):
    """Test for deleting post by id."""
    response = client.delete(f"/api/v1/posts/{test_post.id}", headers=superuser_token_headers)
    assert response.status_code == 200
    assert test_db.query(Posts).all() == []


def test_delete_post_from_non_owner(client, user_token_headers, test_post):
    """Test for deleting post by non-owner user."""
    response = client.delete(f"/api/v1/posts/{test_post.id}", headers=user_token_headers)
    assert response.status_code == 404
