from playwright.sync_api import expect
from jsonschema import validate
import time

def test_get_contacts_schema(api_request_context, auth_token):
    assert auth_token

    # Определяем схему ответа
    contact_schema = {
        "type": "array",
        "items": {
            "type": "object",
            "required": [
                "_id",
                "firstName", 
                "lastName",
                "email",
                "owner",
                "__v"
            ],
            "properties": {
                "_id": {"type": "string"},
                "firstName": {"type": "string"},
                "lastName": {"type": "string"},
                "birthdate": {"type": "string"},
                "email": {"type": "string"},
                "phone": {"type": "string"},
                "street1": {"type": "string"},
                "street2": {"type": "string"},
                "city": {"type": "string"},
                "stateProvince": {"type": "string"},
                "postalCode": {"type": "string"},
                "country": {"type": "string"},
                "owner": {"type": "string"},
                "__v": {"type": "number"}
            }
        }
    }

    response = api_request_context.get("/contacts", headers={"Authorization": f"Bearer {auth_token}"})
    expect(response).to_be_ok()

    data = response.json()
    # Проверяем соответствие схеме
    validate(instance=data, schema=contact_schema)

def test_login_with_invalid_credentials(api_request_context):
    payload = {
        "email": "wrong@email.com",
        "password": "wrongpass"
    }
    response = api_request_context.post("/users/login", data=payload)
    assert response.status == 401  

def test_response_headers(api_request_context, config):
    token = config.get("token")
    response = api_request_context.get("/contacts", headers={"Authorization": f"Bearer {token}"})
    headers = response.headers
    assert "content-type" in headers
    assert headers["content-type"] == "application/json; charset=utf-8"

def test_response_time(api_request_context, config):
    token = config.get("token")
    start_time = time.time()
    response = api_request_context.get("/contacts", headers={"Authorization": f"Bearer {token}"})
    end_time = time.time()
    response_time = end_time - start_time
    assert response_time < 2  # Ответ должен прийти менее чем за 2 секунды

def test_contacts_pagination(api_request_context, auth_token):
    token = auth_token
    response = api_request_context.get(
        "/contacts",
        params={"limit": 5, "page": 1},
        headers={"Authorization": f"Bearer {token}"}
    )
    expect(response).to_be_ok()
    data = response.json()
    assert len(data) <= 5  # Проверка что вернулось не больше 5 записей

