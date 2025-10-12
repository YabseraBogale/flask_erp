-- Delete From Category;
-- Delete From SubCategory;
-- Delete From Department;
-- Delete From Location;
-- Delete From Currency;
-- Delete From Unit;


INSERT INTO Category(category) 
    Values ("Food"),("Furniture"),("Safety Equipment"),
            ("Chemical"),("Sanitary"),("Spare Part"),
            ("Stationery"),("Electronics"),
            ("Accessory"),("Clothing"),("Constraction Material"),("Pad");


INSERT INTO SubCategory(subcategory) 
    Values ("Fixed Assest"),("Moving"),("Consumable");

INSERT INTO Department(department)
    Values ("Human Resources"),("Finance"),("Sales"),
            ("Marketing"),("Operations"),("Procurement"),
            ("Support"),("Information Technology"),("Administration"),
            ("Legal"),("Public Relations"),("Store"),("Logistics & Supply Chain"),
            ("Research & Development"),("Manufacturing"),("Quality Assurance");


INSERT INTO Location(location)
    Values ("Addis Ababa"),("Adama"),("Dire Dawa"),("Mekelle"),
            ("Gondar"),("Bahir Dar"),("Hawassa"),
            ("Jimma"),("Harar"),("Dessie"),("Shashamane"),
            ("Asella"),("Debre Markos"),("Gambela"),("Jijiga"),("Arba Minch"),("Dilla");


INSERT INTO Currency(currency)
    Values ("USD"),("EUR"),("JPY"),
            ("GBP"),("CNY"),("CHF"),
            ("CAD"),("AUD"),("SGD"),
            ("HKD"),("ETH");


INSERT INTO Unit(unit)
    Values ("Piece"),("Dozen"),("Package"),("Gram"),
            ("Kilogram"),("Ton"),("Milliliter"),("Liter"),
            ("Gallon"),("Barrel"),("Millimeter"),("Centimeter"),
            ("Meter"),("Roll"),("Sheet"),("Bottle"),("Can");



-- SELECT * FROM Category;

-- SELECT * FROM CheckIn;

-- SELECT * FROM CheckOut;

-- SELECT * FROM Currency;

-- SELECT * FROM Department;

-- SELECT * FROM EmergencyContact;

-- SELECT * FROM Employee;

-- SELECT * FROM Item;

-- SELECT * FROM Location;

-- SELECT * FROM Unit;

-- SELECT * FROM Subcategory;

