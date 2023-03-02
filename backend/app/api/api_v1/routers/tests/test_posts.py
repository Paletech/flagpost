from app.db.models import Posts


def test_get_list_posts(client, user_token_headers):
    """Test for get list of posts."""
    response = client.get("/api/v1/posts", headers=user_token_headers)
    assert response.status_code == 200


def test_retrieve_post_with_id(client, user_token_headers, test_post):
    """Test for retrieve post from id."""
    response = client.get(f"/api/v1/posts/{test_post.id}", headers=user_token_headers)
    assert response.status_code == 200