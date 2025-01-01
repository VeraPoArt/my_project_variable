from playwright.sync_api import expect

def test_get_request(api_request_context, config):
    response = api_request_context.get(f"{config['api_base_url']}posts/1")
    expect(response).to_be_ok()
    data = response.json()
    assert data["id"] == 1
    assert data["userId"] == 1
    assert data["title"] != ""


def test_post_request(api_request_context, config):
    payload = {
        "title": "foo",
        "body": "bar",
        "userId": 1
    }
    response = api_request_context.post(
        f"{config['api_base_url']}posts", data=payload
    )

    expect(response).to_be_ok()
    data = response.json()
    assert data["title"] == "foo"
    assert data["body"] == "bar"
    assert data["userId"] == 1
    assert "id" in data

def test_put_request(api_request_context, config):
    payload = {
        "id": 1,
        "title": "updated title",
        "body": "updated body",
        "userId": 1
    }
    response = api_request_context.put(
        f"{config['api_base_url']}posts/1", data=payload
    )

    expect(response).to_be_ok()
    data = response.json()
    assert data["title"] == "updated title"
    assert data["body"] == "updated body"
    assert data["id"] == 1
    assert data["userId"] == 1



def test_delete_request(api_request_context, config):
    response = api_request_context.delete(f"{config['api_base_url']}posts/1")
    expect(response).to_be_ok()
    assert response.status == 200

