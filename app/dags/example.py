from datetime import datetime, timedelta
import requests

from airflow import DAG
from airflow.operators.python import PythonOperator

from app.utils.terminal import print_to_console
from app.models.dto.user_dto import UserDTO
from app.models.dto.address_dto import AddressDTO
from app.models.dto.company_dto import CompanyDTO
from app.models.user import Users
from app.models.address import Address
from app.models.company import Company


def fetch_users():
    name: str = "fetch_users: executing"
    print_to_console(name)
    endpoint: str = "https://jsonplaceholder.typicode.com/users"

    response = requests.get(url=endpoint)
    data: list = response.json()

    _users: list = []
    _address: list = []
    _companies: list = []

    for user in data:
        try:
            userObject: dict = {
                "name": user.get("name"),
                "username": user.get("username"),
                "email": user.get("email"),
                "phone": user.get("phone"),
            }
            new_user: UserDTO = Users.create(user=userObject)
            _users.append(new_user)

            address: dict = user.get("address")
            addressObject: dict = {
                "user_id": new_user.id,
                "street": address.get("street"),
                "suite": address.get("suite"),
                "city": address.get("city"),
                "zipcode": address.get("zipcode"),
            }
            new_address: AddressDTO = Address.create(address=addressObject)
            _address.append(new_address)

            company: dict = user.get("company")
            companyObject: dict = {
                "user_id": new_user.id,
                "name": company.get("name"),
                "catchPhrase": company.get("catchPhrase"),
                "bs": company.get("bs"),
            }
            new_company: CompanyDTO = Company.create(company=companyObject)
            _companies.append(new_company)
        except Exception:
            pass

    print_to_console("Done Fetching")
    print_to_console(
        f"No Users: {len(_users): 10} \nNo Addresses: {len(_address): 10} \nNo Companies: {len(_companies)}"
    )


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["fedjioraymond@gmail.com"],
    "email_on_failure": ["fedjioraymond@gmail.com"],
    "email_on_retry": ["fedjioraymond@gmail.com"],
}
with DAG(
    "json_placeholder_server",
    default_args=default_args,
    description="A simple tutorial DAG",
    schedule_interval=None,
    start_date=datetime(2021, 12, 2),
    catchup=False,
    tags=["test"],
) as dag:
    fetch_users = PythonOperator(
        task_id="fetch_user_from_server", python_callable=fetch_users
    )
