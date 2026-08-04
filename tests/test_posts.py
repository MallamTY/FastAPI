from app import schemas
import pytest

def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/api/v1/posts")
    # def validate(post):
    #     return schemas.Post(**post)
    # posts_map = map(validate, response.json().get("data"))
    assert len(response.json().get("data")) == len(test_posts)
    assert response.json().get("data")[0]["Post"].get("id") == test_posts[1].id
    assert response.status_code == 200


def test_unauthorized_get_all_posts(client, test_user):
    response = client.get("api/v1/posts")
    assert response.status_code == 401

def test_authorized_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("api/v1/posts")
    assert response.status_code == 200


def test_unauthorized_get_single_post(client, test_posts):
    response = client.get(f"api/v1/posts/{test_posts[0].id}")
    assert response.status_code == 401


def test_authorized_nonexist_get_single_post(authorized_client, test_posts):
    response = authorized_client.get(f"api/v1/posts/8888")
    assert response.status_code == 404


def test_authorized_get_single_post(authorized_client, test_posts):
    response = authorized_client.get(f"api/v1/posts/{test_posts[0].id}")
    res_posts = schemas.CustomPostEnvelope(**response.json())
    assert res_posts.data.Post.id == test_posts[0].id
    assert res_posts.data.Post.title == test_posts[0].title
    assert response.status_code == 200


@pytest.mark.parametrize("title, content, published", [
    ("New Post", "New Content", True),
    ("Second New Post", "Second New Content", False),
    ("Third New Post", "Third New Content", True)
])
def test_authorized_create_post(authorized_client, title, content, published, test_user):
    response = authorized_client.post(
        "api/v1/posts/create",
        json={"title": title, "content": content, "published": published}
    )
    res_post = schemas.PostResponseEnvelope(**response.json())
    assert res_post.data.title == title
    assert res_post.data.content == content
    assert res_post.data.published == published
    assert res_post.data.poster_id == test_user["id"]
    assert response.status_code == 201


def test_unauthorized_create_post(client, test_user):
    response = client.post(
        "api/v1/posts/create",
        json={"title": "Unauthorized poster", "content": "New post from and unauthorized poster"}
    )
    assert response.status_code == 401


def test_unauthorized_delete_post(client, test_posts):
    response = client.delete(f"api/v1/posts/{test_posts[0].id}")
    assert response.status_code == 401


def test_authorized_delete_post(authorized_client, test_posts):
    response = authorized_client.delete(f"api/v1/posts/{test_posts[0].id}")
    assert response.status_code == 204


def test_delete_nonexisting_post(authorized_client, test_posts):
    id = 34434333
    response = authorized_client.delete(f"api/v1/posts/{id}")
    assert response.status_code == 404
    assert response.json().get("detail") == f"Post with id: {id} was not found"