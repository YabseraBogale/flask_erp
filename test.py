from requests import Session

session=Session()


payload={
    "employee_id":"123",
    "password":"389LDW0:pmDA6Z*"
}

urls={
    "login":"http://127.0.0.1:5000/login",
}


response=session.post(urls["login"],data=payload)

if response.status_code == 200:
    print("Login successful!")
else:
    print("falied")