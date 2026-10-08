resources = [
  {"id": "R001",
  "name": "Laptop",
  "category": "Electronics",
  "total": 10,
  "available": 10},
  {"id": "R002",
  "name": "Keyboard",
  "category": "Accessories",
  "total": 5,
  "available": 5},
  {"id": "R003",
  "name": "Headset",
  "category": "Accessories",
  "total": 3,
  "available": 3}
]

fellows = {
    "F001": "Ada",
    "F002": "John",
    "F003": "Grace"
}

borrow_records = []

def find_resource(resource_id):

    for resource in resources:
        if resource["id"] == resource_id:
            return resource
    return None


def add_resource():

    resource_id = input("Enter resource ID: ").strip().upper()
    name = input("Enter resource name: ").strip()
    category = input("Enter category: ").strip()

    if not resource_id or not name or not category:
        print("Error: All fields are required.")
        return

    if find_resource(resource_id):
        print("Error: Resource ID already exists.")
        return

    try:
        total = int(input("Enter total units: "))

        if total <= 0:
            print("Error: Total units must be positive.")
            return
    except ValueError:
        print("Error: Please enter a valid integer.")

    new_resource = {
        "id": resource_id,
        "name": name,
        "category": category,
        "total": total,
        "available": total
    }

    resources.append(new_resource)

    print("Resource added successfully!")


def list_resource():
    print("/// RESOURCE INVENTORY ///")

    if not resources:
        print("No resources availble")
        return

    for resource in resources:
        print(f"\nID: {resource['id']}")
        print(f"Name: {resource['name']}")
        print(f"Category: {resource['category']}")
        print(f"Total: {resource['total']}")
        print(f"Available: {resource['available']}")
    
    print("//// THANK YOU ////")

    
def get_borrowed_quantity(fellow_id, resource_id):
    quantity = 0

    for record in borrow_records:

        if (record["fellow_id"] == fellow_id and record["resource_id"] == resource_id):
            quantity += record["quantity"]

    return quantity


def borrow_resource():
    fellow_id = input("Enter fellow ID: ").strip().upper()
    resource_id = input("Enter resource ID: ").strip().upper()

    if fellow_id not in fellows:
        print("Error: Fellow does not exist.")
        return

    resource = find_resource(resource_id)

    if resource is None:
        print("Error: Resource does not exist.")
        return
    
    try:
        quantity = int(input("Enter quantity to borrow: "))

    except ValueError:
        print("Error: Quantity must be an integer.")
        return
    if quantity <= 0:
        print("Error: Quantity must be greater than zero.")
        return

    if quantity > resource["available"]:
        print("Error: Insufficient stock.")
        print(f"Available units: {resource['available']}")
        return

    resource["available"] -= quantity

    existing_records = None

    for record in borrow_records:
        if (record["fellow_id"] == fellow_id and record["resource_id"] == resource_id):
            existing_records = record
            break
    if existing_records is not None:
        existing_records["quantity"] += quantity

    else:
        new_record = {
            "fellow_id": fellow_id,
            "resource_id": resource_id,
            "quantity": quantity
        }

        borrow_records.append(new_record)

    print("\nBorrowing successful!")
    print(f"Fellow: {fellows[fellow_id]}")
    print(f"Resource: {resource['name']}")
    print(f"Quantity borrowed: {quantity}")
    print(f"Remaining stock: {resource['available']}")


def return_resource():
    fellow_id = input("Enter fellow ID: ").strip().upper()
    resource_id = input("Enter resource ID: ").strip().upper()

    if fellow_id not in fellows:
        print("Error: Fellow does not exist.")
        return
    
    resource = find_resource(resource_id)

    if resource is None:
        print("Error: Resource does not exist.")
        return
    
    try:
        quantity = int(input("Enter quantity to return: "))

    except ValueError:
        print("Error: Quantity must be an integer.")
        return

    if quantity <= 0:
        print("Error: Quantity must be grearer than zero.")
        return

    borrowed_quantity = get_borrowed_quantity(fellow_id, resource_id)

    if borrowed_quantity == 0:
        print("Error: Fellows has not borrowed this resource.")
        return

    if quantity > borrowed_quantity:
        print("Error: Cannot retun more thn=an borrowed.")
        print("Currently borrowed: {borrowed_quantity}")
        return

    for record in borrow_records:
        if (record["fellow_id"] == fellow_id and record["resource_id"] == resource_id):
            record["quantity"] -= quantity

            if record["quantity"] == 0:
                borrow_records.remove(record)
            break

    resource["available"] += quantity

    print("\nReturn successful!")
    print(f"Fellow: {fellows[fellow_id]}")
    print(f"Resource: {resource['name']}")
    print(f"Quantity returned: {quantity}")
    print(f"Available stock: {resource['available']}")


def search_recource():
    search_item = input("Enter resource name: ").strip()

    if not search_item:
        print("Error: Search item cannot be empty.")
        return

    found = False

    for resource in resources:
        if search_item.casefold() in resource["name"].casefold():
            print(f"\nID: {resource['id']}")
            print(f"Name: {resource['name']}")
            print(f"Category: {resource['category']}")
            print(f"Availale: {resource['available']}")

            found = True

    if not found:
        print("No matching resource found.")


def filter_category():
    category = input("Enter category: ").strip()

    if not category:
        print("Error: Category cannot be empty.")
        return

    found = False

    for resource in resources:

        if resource["category"].casefold() == category.casefold():
            print(f"\nID: {resource['id']}")
            print(f"Name: {resource['name']}")
            print(f"Category: {resource['category']}")
            print(f"Available: {resource['available']}")

            found = True

        if not found:
            print("No resource found in this category")


def generate_report():
    total_units = 0
    available_units = 0

    for resource in resources:
        total_units += resource["total"]
        available_units += resource["available"]

    borrowed_units = total_units - available_units

    print("//// INVENTORY REPORT ////")

    print(f"Total units: {total_units}")
    print(f"Available units: {available_units}")
    print(f"Borrowed units: {borrowed_units}")


    print("\n/////  LOW STOCK RESOURCE /////")
    low_stock_found = False
    for resource in resources:
        if resource["available"] < 3:
            print(
                f"{resource['name']}: "
                f"{resource['available']} available" 
            )
            low_stock_found = True

    if not low_stock_found:
        print("No low_stock resources.")


    print("\n////// MOST BORROWED RESOURCES //////")

    highest_borrowed = 0
    most_borrowed = []

    for resource in resources:
        borrowed = resource["total"] - resource["available"]

        if borrowed > highest_borrowed:
            hishest_borrowed = borrowed
            most_borrowed = [resource]

        elif borrowed == highest_borrowed and borrowed > 0:
            most_borrowed.append(resource)

    if highest_borrowed == 0:
        print("No resource currently borrowed")

    else:
        for resource in most_borrowed:
            print(
                f"{resource['id']}: "
                f"{hishest_borrowed} borrowed"
            )


def main():

    while True:
        print("\n//////////////////////////////////")
        print("    LEARN2EARN RESOURCE SYSTEM")
        print("///////////////////////////////////////")

        print("1. Add Resource")
        print("2. List Resource")
        print("3. Borrow Resource")
        print("4. Return Resource")
        print("5. Search Resource")
        print("6. Filter by Category")
        print("7. Generate Report")
        print("8. Exit")

        choice = input("\nEnter your choice (1-8): ").strip()

        if choice == "1":
            add_resource()

        elif choice == "2":
            list_resource()

        elif choice == "3":
            borrow_resource()
        
        elif choice == "4":
            return_resource()

        elif choice == "5":
            search_recource()

        elif choice == "6":
            filter_category()

        elif choice == "7":
            generate_report()
        
        elif choice == "8":
            print("Thank you for using LEARN2EARN!")
            break

        else:
            print("Invalid choice. Please select 1-8")


if __name__ == "__main__":
    main()