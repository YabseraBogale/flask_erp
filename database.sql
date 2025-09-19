create table if not exists emergencycontact (

    emergency_contact_id integer primary key autoincrement,
    firstname varchar(30) not null,
    middlename varchar(30), 
    lastname varchar(30) not null,
    gender varchar(6) not null,
    phonenumber varchar(15) not null, 
    email text unique,
    location text not null,
    fyida_id text not null

);

create table if not exists employee (

    employee_id integer primary key autoincrement,
    emergency_contact_id integer references emergencycontact,
    firstname varchar(30) not null,
    middlename varchar(30), 
    lastname varchar(30) not null,
    gender varchar(6) not null,
    phonenumber varchar(15) not null, 
    email text unique,
    location text not null,
    fyida_id text not null,
    position text not null,
    department text not null,
    tin_number int not null,
    bank_account_number int not null,
    salary float not null

);

create table if not exists item (
    
    item_id integer primary key autoincrement,
    item_name text not null,
    item_description text not null,
    item_price real not null,
    item_quantity integer not null,
    category text not null,
    subcategory text not null,
    unit text not null,
    location text not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp,
    created_by_employee_id integer references employee(employee_id),
    updated_by_employee_id integer references employee(employee_id)

);


-- transactiontype table: stores the types of transactions (e.g., 'add', 'remove', 'transfer')
create table if not exists transactiontype (

    transaction_type_id integer primary key autoincrement,
    type_name varchar(50) not null unique

);


-- itemlog table: this is the core of your tracking system. it logs every inventory transaction.
create table if not exists itemlog (

    log_id integer primary key autoincrement,
    item_id integer not null references item(item_id),
    transaction_type_id integer not null references transactiontype(transaction_type_id),
    employee_id integer not null references employee(employee_id), -- the employee responsible for the transaction
    quantity_changed integer not null,
    transaction_date timestamp default current_timestamp,
    description text

);

create table if not exists checkout (

    checkout_id integer primary key autoincrement,
    item_id integer not null references item(item_id),
    employee_id integer not null references employee(employee_id),
    checkout_date timestamp default current_timestamp,
    return_date timestamp,
    notes text

);

---

-- inserting initial transaction types
insert into transactiontype (type_name) values ('add');
insert into transactiontype (type_name) values ('remove');
insert into transactiontype (type_name) values ('transfer');