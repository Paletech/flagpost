from app.db.models import Posts


def test_get_list_posts(client, user_token_headers):
    """Test for get list of posts."""
    response = client.get("/api/v1/posts", headers=user_token_headers)
    assert response.status_code == 200


def test_retrieve_post_with_id(client, user_token_headers, test_post):
    """Test for retrieve post from id."""
    response = client.get(f"/api/v1/posts/{test_post.id}", headers=user_token_headers)
    assert response.status_code == 200


def test_create_post(client, user_token_headers, test_user):
    """Test for creating new post."""
    post = {
        "type": "type",
        "text": "text",
        "user_id": str(test_user.id),
        "created_at": "2023-03-02 16:05:57.312334",
    }
    response = client.post('/api/v1/posts', headers=user_token_headers, json=post)

    assert response.status_code == 200


def test_delete_post(client, superuser_token_headers, test_post):
    """Test for deleting post from id."""
    response = client.delete(f"/api/v1/posts/{test_post.id}", headers=superuser_token_headers)
    assert response.status_code == 200
