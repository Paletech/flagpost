from fastapi import status

from app.db.models import Posts


def test_unauthenticated_all_posts_routers(client):
    """Test checks authentication for all posts routers."""
    response = client.get("/api/v1/posts")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = client.get("/api/v1/posts/b21706cd-df99-490f-aa4f-7efa418b1343")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = client.post("/api/v1/posts")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = client.delete("/api/v1/posts/b21706cd-df99-490f-aa4f-7efa418b1343")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = client.put("/api/v1/posts/b21706cd-df99-490f-aa4f-7efa418b1343")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_manage_non_existent_post(client, superuser_token_headers):
    """Test checks all post routers for response to non-existent post."""
    response = client.get("/api/v1/posts/b21706cd-df99-490f-aa4f-7efa418b1343", headers=superuser_token_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response = client.delete("/api/v1/posts/b21706cd-df99-490f-aa4f-7efa418b1343", headers=superuser_token_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response = client.put(
        "/api/v1/posts/b21706cd-df99-490f-aa4f-7efa418b1343",
        headers=superuser_token_headers,
        json={}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_list_posts(client, user_token_headers):
    """Test for get list of posts."""
    response = client.get("/api/v1/posts", headers=user_token_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_retrieve_post_by_id(client, superuser_token_headers, test_post, test_superuser):
    """Test for retrieve post by id."""
    response = client.get(f"/api/v1/posts/{test_post.id}", headers=superuser_token_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'type': 'test',
        'text': 'test',
        'id': str(test_post.id),
        'user_id': str(test_superuser.id),
        'created_at': '2023-03-02T16:05:57.312334',
        'updated_at': '2023-03-02T16:20:12.758392',
        'files': [],
        'categories': []
    }


def test_create_post(client, superuser_token_headers, test_superuser):
    """Test for creating new post."""
    post = {
        "type": "type",
        "text": "text",
        "user_id": str(test_superuser.id),
    }
    response = client.post('/api/v1/posts', headers=superuser_token_headers, json=post)
    assert response.status_code == status.HTTP_201_CREATED
    created_post = response.json()
    [created_post.pop(i) for i in ["created_at", "updated_at", "id"]]
    assert created_post == {
        **post,
        "categories": [],
        "files": []
    }


def test_update_post(client, superuser_token_headers, test_post, test_category, test_file):
    """Test for updating post."""

    new_post = {
        "text": "some_new_text",
        "categories": str(test_category.id),
        "files": str(test_file.id)
    }
    response = client.put(f"/api/v1/posts/{test_post.id}", json=new_post, headers=superuser_token_headers)
    assert response.status_code == status.HTTP_200_OK


def test_update_post_with_wrong_user(client, user_token_headers, test_post):
    """Test for updating post by id with wrong user."""
    response = client.put(f"/api/v1/posts/{test_post.id}", headers=user_token_headers, json={})
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_post_with_wrong_data(client, superuser_token_headers, test_post):
    """Test for updating post by id with wrong data."""
    update = {
        "text": "new_text",
        "categories": "2348245e-0ab0-4c35-9962-d6bf519a79a3",
        "files": "2348245e-0ab0-4c35-9962-d6bf519a79a3"
    }
    response = client.put(f"/api/v1/posts/{test_post.id}", headers=superuser_token_headers, json=update)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_post(client, superuser_token_headers, test_post, test_db):
    """Test for deleting post by id."""
    response = client.delete(f"/api/v1/posts/{test_post.id}", headers=superuser_token_headers)
    assert response.status_code == status.HTTP_200_OK
    assert test_db.query(Posts).all() == []


def test_delete_post_from_non_owner_user(client, user_token_headers, test_post):
    """Test for deleting post by non-owner user."""
    response = client.delete(f"/api/v1/posts/{test_post.id}", headers=user_token_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
