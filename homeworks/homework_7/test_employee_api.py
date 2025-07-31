import pytest
from employee_api import EmployeeApi

@pytest.fixture(scope="module")
def api():
    return EmployeeApi()

@pytest.fixture
def employee_id(api):
    data = {
        "first_name": "Bartholomew",
        "last_name": "Simpson",
        "middle_name": "Jo-Jo",
        "company_id": 1,
        "email": "bartman@simpson.com",
        "phone": "+17035456700",
        "birthdate": "1979-02-23",
        "is_active": True
    }
    response = api.create_employee(data)
    assert response.status_code == 200
    return response.json()["company_id"]

def test_get_employee_info(api, employee_id):
    response = api.get_employee_info(employee_id)
    print("GET response:", response.status_code, response.text)
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Bartholomew"
    assert data["last_name"] == "Simpson"

def test_update_employee(api, employee_id):
    updated_data = {
        "phone": "+987654321",
        "is_active": False
    }
    response = api.update_employee(employee_id, updated_data)
    print("UPDATE response:", response.status_code, response.text)
    assert response.status_code == 200
    data = response.json()
    assert data["phone"] == "+987654321"
    assert data["is_active"] is False