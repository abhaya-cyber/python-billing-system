from operation import User, Seller, show_products
from read import get_products
from write import save_products
from datetime import datetime
import re

def validate_phone(phone):
    return re.match(r'^(98|97|96|95)\d{8}$', phone) is not None

def initialize_system():
    try:
        # Try to create bills directory
        try:
            temp = open("bills/.tempfile", "w")
            temp.close()
        except:
            pass
            
        products = get_products()
        print("\nSystem initialized")
        return products
    except Exception as e:
        print("\nInitialization error: %s" % e)
        exit(1)

def main():
    products = initialize_system()

    while True:
        print("\n" + "="*50)
        print("LooksMax Beauty & Skin Care".center(50))
        print("Lagankhel, Lalitpur".center(50))
        print("Get the best Skin Care products at our store".center(50))
        print("="*50 + "\n")

        print("1. Customer Purchase")
        print("2. Product Restock")
        print("3. Exit\n")
        print("-"*50)

        choice = input("Enter choice (1-3): ")
        products = get_products()

        if choice == "1":
            show_products(products, for_customer=True)
            if products:
                print("\n" + "-"*50)
                name = input("Customer name: ")
                
                phone = ""
                while True:
                    phone = input("Phone number (+977):")
                    if validate_phone(phone):
                        break
                    print("Invalid phone number!")
                
                user = User(name, phone)
                user.add_to_cart(products)
                invoice_date = user.generate_sale_invoice(products)
                if invoice_date:
                    save_products(products)
                    print("Invoice generated at %s" % invoice_date)
                    print("Total: NRS %.2f" % user.total)

        elif choice == "2":
            show_products(products, for_customer=False)
            if products:
                print("\n" + "-"*50)
                supplier = input("Supplier name: ")
                seller = Seller(supplier)
                seller.restock_product(products)
                invoice_date = seller.generate_restock_invoice()
                if invoice_date:
                    save_products(products)
                    print("Invoice generated at %s" % invoice_date)
                    print("Total Amount: NRS %.2f" % seller.total)

        elif choice == "3":
            current_dt = datetime.now()
            formatted_date = current_dt.strftime("%Y-%m-%d %H:%M:%S")
            print("\nThank you for choosing LooksMax. Have a Fantastic Day! (%s)\n" % formatted_date)
            break

        else:
            print("\nInvalid choice! Please enter 1-3\n")

if __name__ == "__main__":
    main()
