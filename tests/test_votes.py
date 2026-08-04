import pytest
from app import models


@pytest.fixture()
def test_vote(session, test_user, test_posts):
    new_vote = models.Votes(post_id=test_posts[2].id, user_id=test_user["id"])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, test_posts):
    response = authorized_client.post(
        "api/v1/votes/",
        json={"post_id": test_posts[2].id, "dir": 1}
    )
    assert response.status_code == 201


def test_unauthorized_vote_on_post(client, test_posts):
    response = client.post(
        "api/v1/votes/",
        json={"post_id": test_posts[2].id, "dir": 1}
    )
    assert response.status_code == 401


def test_vote_on_post_twice(authorized_client, test_posts, test_vote):
    response =authorized_client.post(
        "api/v1/votes/",
        json={"post_id": test_posts[2].id, "dir": 1}
        )
    assert response.json().get("detail") == f"user has already voted on post {test_posts[2].id}"
    assert response.status_code == 409
    