from playwright.sync_api import Playwright
import pytest


def test_getting_users(playwright: Playwright):

    api_context = playwright.request.new_context()
    response = api_context.get("https://restful-booker.herokuapp.com/booking")
    
    assert response.status == 200
    api_context.dispose()


def test_fullyfunctionalE2E(auth_api):
    # Complete E2E Test (POST, PUT, DELETE)
    
    # 1. POST 
    response_post = auth_api.post(
        "https://restful-booker.herokuapp.com/booking",
        data={
            "firstname": "Adam",
            "lastname": "Terminator",
            "totalprice": 500,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2026-11-01",
                "checkout": "2026-11-10"
            }
        }
    )
    assert response_post.status == 200
    new_id = response_post.json()["bookingid"]
    print(f"\n[E2E] New booking ID created: {new_id}")

    assert response_post.json()["booking"]["firstname"] == "Adam"

    # 2. PUT 
    response_put = auth_api.put(
        f"https://restful-booker.herokuapp.com/booking/{new_id}",
        data={
            "firstname": "Adam",
            "lastname": "Prepsany",
            "totalprice": 999,  
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2026-11-01",
                "checkout": "2026-11-10"
            }
        }
    )
    assert response_put.status == 200
    print(f"[E2E] Booking {new_id} successfully updated")

    # 3. DELETE 
    response_delete = auth_api.delete(
        f"https://restful-booker.herokuapp.com/booking/{new_id}"
    )
    assert response_delete.status == 201
    print("[E2E] Booking successfully deleted (Cleanup complete)")


# ==========================================
# NEGATIVE & BORDER TESTING
# ==========================================

def test_without_auth_token(playwright: Playwright):
 
    api_context = playwright.request.new_context()
    negative_response = api_context.put(
        "https://restful-booker.herokuapp.com/booking/10",
        headers={
            "Accept": "application/json"
            # NO TOKEN
        },
        data={
             "firstname": "Adam",
             "lastname": "Prepsany",
             "totalprice": 999,
             "depositpaid": False,
             "bookingdates": {
                 "checkin": "2026-11-01",
                 "checkout": "2026-11-10"
                }
        }
    )

    assert negative_response.status == 403
    print(f"\n[Security] API is secured, returned: {negative_response.text()}")
    api_context.dispose()


def test_border_for_get(playwright: Playwright):
    # Border test for GET function 
    api_context = playwright.request.new_context()
    border_response = api_context.get(
        "https://restful-booker.herokuapp.com/booking/1000000",
        headers={"Accept": "application/json"}
    )
    
    assert border_response.status in [400, 404, 500], (
        f"API failed to block GET request on non-existent ID! Returned: {border_response.text()}"
    )
    api_context.dispose()


def test_border_for_delete(auth_api):
    # Border test for DELETE function 
    response_delete = auth_api.delete(
        "https://restful-booker.herokuapp.com/booking/1000000"
    )
    
    assert response_delete.status in [400, 404, 405, 500], (
        f"API failed to block DELETE request on non-existent ID! Returned: {response_delete.text()}"
    )

@pytest.mark.xfail(reason="Expected failure: Restful-Booker has a bug and accepts invalid data (returns status 200)")
@pytest.mark.parametrize(
    "firstname, depositpaid",
    [
        ("", False),         
        ("10", True),        
        ("Jayden", "100"),   
    ],
)
def test_post_wrong_data(auth_api, firstname, depositpaid):
    # Data driven testing (DDT)
    response = auth_api.post(
        "https://restful-booker.herokuapp.com/booking",
        data={
            "firstname": firstname,
            "lastname": "10",
            "totalprice": 999,
            "depositpaid": depositpaid,
            "bookingdates": {
                "checkin": "2026-11-01",
                "checkout": "2026-11-10"
            }
        }
    )

    assert response.status in [400, 500], (
        f"API failed to block bad data! Returned status: {response.status}, text: {response.text()}"
    )