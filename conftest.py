import pytest
from playwright.sync_api import Playwright


@pytest.fixture(scope="session")
def auth_api(playwright: Playwright):

    api_context = playwright.request.new_context()
    response = api_context.post(
        "https://restful-booker.herokuapp.com/auth",
        data={
            "username": "admin",
            "password": "password123"
        }
    )
    token = response.json()["token"]
    api_context.dispose()

  
    authenticated_context = playwright.request.new_context(
        extra_http_headers={
            "Accept": "application/json",
            "Cookie": f"token={token}"
        }
    )

    yield authenticated_context

   
    authenticated_context.dispose()