def test_get_request(api_request_context, config):
    response = api_request_context.get(f"{config['api_base_url']}posts/1")
    assert response.status == 200
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
    assert response.status == 201
    data = response.json()
    assert data["title"] == "foo"
    assert data["body"] == "bar"
    assert data["userId"] == 1
    assert "id" in data
