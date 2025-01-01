from playwright.sync_api import expect
import time
from jsonschema import validate

def test_register_user(api_request_context, config):
    unique_email = f"testuser{int(time.time())}@example.com"
    config["username"] = unique_email

    payload = {
        "firstName": "Test",
        "lastName": "User", 
        "email": config["username"],
        "password": config["password"]
    }
    response = api_request_context.post("/users", data=payload)
    expect(response).to_be_ok()

    data = response.json()
    assert data["user"]["email"] == config["username"]


def test_login_user(api_request_context, config):
    payload = {
        "email": config["username"],
        "password": config["password"]
    }
    response = api_request_context.post("/users/login", data=payload)
    expect(response).to_be_ok()

    data = response.json()
    assert "token" in data
    config["token"] = data["token"]

def test_get_contacts(api_request_context, config):
    token = config.get("token")
    assert token

    response = api_request_context.get("/contacts", headers={"Authorization": f"Bearer {token}"})
    expect(response).to_be_ok()

    data = response.json()
    assert isinstance(data, list)

def test_create_contact(api_request_context, config):
    token = config.get("token")
    assert token

    payload = {
    "firstName": "John",
    "lastName": "Doe",
    "birthdate": "1970-01-01", 
    "email": "jdoe@fake.com",
    "phone": "8005555555",
    "street1": "1 Main St.",
    "street2": "Apartment A",
    "city": "Anytown",
    "stateProvince": "KS",
    "postalCode": "12345",
    "country": "USA"
}
    response = api_request_context.post("/contacts", data=payload, headers={"Authorization": f"Bearer {token}"})
    expect(response).to_be_ok()

    data = response.json()
    config["contact_id"] = data["_id"]


    
def test_update_contact(api_request_context, config):
    token = config.get("token")
    contact_id = config.get("contact_id")
    assert token
    assert contact_id

    payload = {
    "firstName": "John",
    "lastName": "Dobby",
    "birthdate": "1970-01-01",
    "email": "jdoe@fake12345.com",
    "phone": "8005555555",
    "street1": "1 Main St.",
    "street2": "Apartment A",
    "city": "Anytown",
    "stateProvince": "KS",
    "postalCode": "12345",
    "country": "USA"
}
    response = api_request_context.put(f"/contacts/{contact_id}", data=payload, headers={"Authorization": f"Bearer {token}"})
    expect(response).to_be_ok()

    data = response.json()

def test_delete_contact(api_request_context, config):
    token = config.get("token")
    contact_id = config.get("contact_id")
    assert token
    assert contact_id

    response = api_request_context.delete(f"/contacts/{contact_id}", headers={"Authorization": f"Bearer {token}"})
    expect(response).to_be_ok()




