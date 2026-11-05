# Restful-Booker API Testing 🚀

Automated API testing framework for the [Restful-Booker](https://restful-booker.herokuapp.com/) application, built with **Python**, **Playwright**, and **Pytest**. 

This project demonstrates professional QA automation practices, including End-to-End (E2E) testing, Data-Driven Testing (DDT), and boundary/security validation.

## 🛠️ Tech Stack
* **Python**
* **Playwright** (APIRequestContext for blazing-fast requests)
* **Pytest** (Fixtures, Parametrization, expected failures)

## 🎯 Key Features
* **Authentication Fixture:** Uses a `conftest.py` session fixture for clean, reusable token management.
* **E2E Testing:** Complete CRUD lifecycle (POST -> PUT -> DELETE) with deep JSON assertions.
* **Negative & Security Testing:** Validation of `403 Forbidden` on missing authorization headers.
* **Boundary Testing:** Validation of status codes (`404/405/500`) for edge cases like non-existent booking IDs.
* **Data-Driven Testing (DDT):** Uses `@pytest.mark.parametrize` to run tests against multiple sets of invalid payloads.
* **Real Bug Handling:** Uses `@pytest.mark.xfail` to document and handle a known bug in the Restful-Booker API (where the API incorrectly accepts invalid data and returns `200 OK`).

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone [https://github.com/Ad4mB3/restful-booker-api-testing.git](https://github.com/Ad4mB3/restful-booker-api-testing.git)
Install dependencies:

Bash
pip install pytest playwright
Run the tests (with print statements visible):

Bash
pytest -s