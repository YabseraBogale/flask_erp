# flask_erp


Built for businesses with 100+ employees

Our ERP solution is designed to meet the operational needs of medium and large Ethiopian businesses. It centralizes and streamlines core business functions into one powerful, integrated system—improving efficiency, accuracy, and visibility across all departments.

## Key Modules & Capabilities

### Human Resources Module

Empower your HR team with tools to effectively manage the workforce. The system enables comprehensive employee registration, seamless assignment of positions, departments, and roles, and ensures all employee records are organized and easily retrievable. It also supports full employee lifecycle management, including termination, resignation, deceased records, and rehire processes, providing HR with a complete and structured view of every employee.

### Store Module

Maintain full control over your stock and physical resources with a robust inventory management system. It allows for detailed item registration and categorization, real-time stock monitoring, and accurate check-in/check-out tracking to ensure accountability. Shelf and location tracking further enhance organization by minimizing loss, misplacement, and operational inefficiencies.

### Sales Management Module

Increase revenue visibility and enhance customer engagement through a powerful sales management module. The system enables detailed customer registration and profiling, providing a clear understanding of customer behavior and purchase history. It streamlines item sales recording and processing, ensuring fast and accurate transactions. Monthly and periodic sales tracking offers actionable insights into performance trends, while built-in sales prediction capabilities help forecast future demand, optimize inventory, and support strategic decision-making.

### Procurement Management Module

Ensure smooth communication and accurate tracking of supply-side operations.
Vendor registration and management Recording of inbound items Purchase order tracking from request to fulfillment

### Finance Management Module

Gain complete insight into the financial health of your business. Access to company-wide financial data
Financial summaries, reports, and statements Supports decision-making through accurate financial visibility

### Administration Management Module

Centralized control for secure and efficient system operation.
Full access to all modules User permission and role management
Configuration of system-wide settings.

## Why This ERP?

Tailored for Ethiopian business workflows Scales with organizational growth Increases efficiency by integrating all major departments Enhances cross-department visibility and reduces errors

## Requirements

    python >= 3.11
    sqlite3
    redis
    

Running the web app locally:

    pip install -r requirements.txt

for auditing dependences simply run to see:

    pip-audit


## Database Table

#### Location
    Addis Ababa,
    Adama,
    Dire Dawa,
    Mekelle,
    Gondar,
    Bahir Dar,
    Hawassa,
    Jimma,
    Harar, 
    Dessie,
    Shashamane,
    Asella,
    Debre Markos,
    Gambela,
    Jijiga,
    Arba Minch,
    Dilla

#### Unit
    Piece,
    Dozen Package,
    Gram,
    Kilogram,
    Ton,
    Milliliter,
    Liter,
    Gallon,
    Barrel,
    Millimeter,
    Centimeter,
    Meter,
    Roll,
    Sheet,
    Bottle,
    Can

#### Category

    Food,
    Furniture,
    Safety Equipment,
    Chemical,
    Sanitary,
    Spare Part,
    Stationery,
    Electronics,
    Accessory,
    Clothing,
    Constraction Material,
    Pad

#### Department
    Human Resources,
    Finance,
    Sales,
    Procurement,
    Administration,
    Store

#### Currency

    USD,EUR,JPY,
    GBP,CNY,CHF,
    CAD,AUD,SGD,
    HKD,ETH

#### Subcategory

    Fixed Assest,Moving Assest

#### EmergencyContact

    fyida_id,
    firstname,
    middlename,
    lastname,
    gender,
    phonenumber,
    email,
    location_name
    
#### Employee

    employee_tin_number,
    firstname,
    middlename,
    lastname,
    gender,
    phonenumber,
    date_of_employement,
    email,
    fyida_id,
    position,
    job_description,
    bank_account_number,
    salary,
    pension_balance,
    password,
    employment_status,
    termination_reason,
    termination_date,
    emergency_contact_fyida_id,
    department_name,
    location_name,
    currency_name

#### Item

    item_id,
    item_name,
    item_description,
    item_price,
    item_quantity,
    item_shelf_life,
    created_at
    updated_at,
    unit_name,
    created_by_employee_tin_number,
    location_name,
    category_name,
    currency_name,
    subcategory_name

#### Vendor

    vendor_tin,
    vendor_name,
    vendor_email,
    vendor_phonenumber,
    vendor_location,
    regsistered_employee_tin_number,
    vendor_registered_date

#### Customer

    customer_tin,
    customer_name,
    customer_email,
    customer_phonenumber,
    customer_location,
    regsistered_employee_tin_number,
    customer_registered_date
    
#### Sales

    sales_id,  
    sales_date,
    item_name,
    item_quantity,
    total_price,
    employee_tin_number,
    customer_tin,
    currency_name,
    unit_name

#### UtilityCost

    utility_cost_id,
    utility_name,
    utility_type,
    total_cost,
    location_name,
    department_name,
    currency_name,
    recorded_by_employee_tin_number,
    recorded_at

#### PurchaseOrder

    purchase_order_id,
    order_date,
    order_status,
    ordered_quantity,
    purchase_reason,
    item_name,
    employee_tin_number

#### CheckIn

    checkin_id,
    item_name,
    vendor_name,
    item_price,
    item_quantity,
    item_grr,
    checkin_date,
    item_description,
    employee_tin_number,
    reciving_employee_tin_number,
    currency_name,
    unit_name,
    item_shelf_life,
    item_status

#### CheckOut

    checkout_id,
    item_quantity,
    item_siv,
    checkout_date,
    item_description,
    item_name,
    item_status,
    employee_tin_number,
    return_employee_tin_number,
    location_name,
    department_name,
    unit_name

#### Budget

    budget_id,
    department_name,
    item_name,
    item_quantity,
    item_budget,
    item_quantity_deduct,
    item_budget_deduct,
    unit_name,
    recorded_by_employee_tin_number,
    recorded_at,
    currency_name,
    date_from,
    date_to

## Routes

    / redirect to /login

    /my_account
    /employee_list
    /finance
    /store
    /sales
    /procurement
    /human_resources
    /administration

    /all/employee/data
    /customer_list
    /pending_listing
    /sales_list
    /approved_listing
    /rejected_listing
    /item_listing
    /utility_listing
    /vendor_listing
    /checkout_list
    /checkin_list
    /budget_list
    /terminated_employee_list
    /terminated_employee_list/employee/data

    /employee_registeration, methods=["GET","POST"]
    /employee_termination, methods=["GET","POST"]
    /restate/<employee_tin_number>, methods=["GET","POST"]
    /item_regsisteration, methods=["GET","POST"]
    /item_checkout, methods=["GET","POST"]
    /item_checkin, methods=["GET","POST"]
    /sales_registeration, methods=["GET","POST"]
    /purchase_order, methods=["GET","POST"]
    /customer_registeration, methods=["GET","POST"]
    /purchase_order_approval/<purchase_order_id>, methods=["GET","POST"]
    /vendor_info/<vendor_tin>, methods=["GET","POST"]
    /utility_registeration, methods=["GET","POST"]
    /vendor_regsisteration, methods=["GET","POST"]
    /budget_registeration, methods=["GET","POST"]
    /finanical_data, methods=["GET","POST"]
    /login, methods=["GET","POST"]

    /terminated_employee_list/employee/data/<employee_tin_number>
    /employee_info_for_hr/<employee_tin_number>
    /item_info/<item_id>
    /checkout_info/<checkout_id>
    /checkin_info/<checkin_id>
    /customer_list/list/<employee_tin_number>
    /sales_list/list/<employee_tin_number>  
    
    /logout

    