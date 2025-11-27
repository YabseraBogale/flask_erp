from datetime import datetime

random_text="Lorem ipsum dolor sit amet consectetur adipisicing elit. Modi, nisi natus voluptas repellendus odit quaerat sed veritatis incidunt hic obcaecati quae perspiciatis quam accusamus iusto consequuntur adipisci ipsam cupiditate placeat."

def test_login_successful(client):
    """Test that valid credentials result in a 200 OK."""
    
   
    response = client.post("/login", data={
        "employee_id": "123",
        "password": "389LDW0:pmDA6Z*"
    })


    assert response.status_code == 302
   

def test_employee_registeration(client):
    response=client.post("/employee_registeration",data={
        "emergency_contact_fyida_id":"2345",
        "emergency_contact_firstname":"Yabsera",
        "emergency_contact_lastname":"Bogale",
        "emergency_contact_middlename":"Abate",
        "emergency_contact_gender":"Male",
        "emergency_contact_phonenumber":"+251920201161",
        "emergency_contact_email":"yabsera@gmail.com",
        "emergency_contact_location":"Addis Ababa",
        "firstname":"Yabsera",
        "lastname":"Bogale",
        "middlename":"Abate",
        "gender":"Male",
        "phonenumber":"+251920201161",
        "email":"yabserapython@gmail.com",
        "date_of_employement":datetime.today(),
        "fyida_id":"23423",
        "position":"Junior Software Developer",
        "location":"Addis Ababa",
        "department":"Administration",
        "job_description":random_text,
        "tin_number":"1231",
        "bank_account_number":"123123",
        "currency":"ETH",
        "salary":"18000",
    })

    assert response.status_code==302

