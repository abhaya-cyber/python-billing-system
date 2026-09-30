from datetime import datetime
from write import save_products, save_bill_to_file

def show_products(products, for_customer=True):
    if not products:
        print("No products available")
        return

    price_label = "Price (NRS)"
    print("\nProduct List:")
    print("ID | Product           | Brand        | Stock | %-15s | Country" % price_label)
    print("-"*80)
    
    i = 1
    for p in products:
        price = p['cost_price'] * 3 if for_customer else p['cost_price']
        print("%2d | %-17s | %-12s | %5d | %13.2f | %s" % 
              (i, p['name'], p['brand'], p['quantity'], price, p['country']))
        i += 1
    print()

class User:
    def __init__(self, name, phone_number):
        self.name = name if name else "Guest"
        self.phone_number = phone_number if phone_number else "N/A"
        self.cart = []
        self.total = 0.0

    def add_to_cart(self, products):
        if not products:
            print("No products available")
            return

        print("\nAdd products to cart (enter 0 to finish):")
        while True:
            show_products(products)
            try:
                product_id = input("Enter product ID: ")
                if product_id == "0":
                    break

                product_id = int(product_id) - 1
                if product_id < 0 or product_id >= len(products):
                    print("Invalid ID! Must be between 1-%d" % len(products))
                    continue

                quantity = int(input("Enter quantity: "))
                if quantity <= 0:
                    print("Quantity must be positive")
                    continue

                product = products[product_id]
                if quantity > product['quantity']:
                    print("Only %d available" % product['quantity'])
                    continue

                free_items = quantity // 3
                selling_price = product['cost_price'] * 3

                self.cart.append({
                    "product": product,
                    "quantity": quantity,
                    "free_items": free_items,
                    "selling_price": selling_price,
                    "subtotal": quantity * selling_price
                })

                self.total += quantity * selling_price
                print("Added %d %s (free: %d)" % (quantity, product['name'], free_items))

            except ValueError:
                print("Invalid input")

    def generate_sale_invoice(self, products):
        if not self.cart:
            print("Cart is empty")
            return None

        current_dt = datetime.now()
        formatted_date = current_dt.strftime("%Y-%m-%d %H:%M:%S")

        print("\n" + "="*50)
        print("INVOICE".center(50))
        print("="*50)
        print("Date: %s" % formatted_date)
        print("Customer: %s" % self.name)
        print("Phone: %s" % self.phone_number)
        print("="*50)
        print("%-20s %4s %4s %10s %10s" % 
              ("Product", "Qty", "Free", "Price", "Subtotal"))
        print("-"*50)

        for item in self.cart:
            p = item['product']
            print("%-20s %4d %4d %9.2f %9.2f" % 
                  (p['name'], item['quantity'], item['free_items'],
                   item['selling_price'], item['subtotal']))
            p['quantity'] -= (item['quantity'] + item['free_items'])

        print("="*50)
        print("TOTAL: NRS %.2f" % self.total)
        print("="*50)
        
        # Save bill to file
        if save_bill_to_file(
            self.name,
            self.phone_number,
            self.cart,
            self.total,
            formatted_date
        ):
            print("Bill saved successfully")
        else:
            print("Error saving bill")
        
        return formatted_date

class Seller:
    def __init__(self, supplier_name):
        self.supplier_name = supplier_name or "Supplier"
        self.restock_items = []
        self.total = 0.0

    def restock_product(self, products):
        if not products:
            print("No products available - adding first product")
            product_id = "new"

        print("\nRestock products (enter 0 to finish):")
        while True:
            show_products(products, False)
            try:
                if not products:
                    product_id = "new"
                else:
                    product_id = input("Enter product ID (or 'new' to add new product): ")
                
                if product_id == "0":
                    break
                elif product_id.lower() == "new":
                    print("\nAdding new product:")
                    name = input("Enter product name: ")
                    brand = input("Enter brand: ")
                    country = input("Enter country of origin: ")
                    
                    while True:
                        try:
                            cost_price = float(input("Enter cost price: "))
                            if cost_price <= 0:
                                print("Price must be positive")
                                continue
                            break
                        except ValueError:
                            print("Invalid price")
                    
                    while True:
                        try:
                            quantity = int(input("Enter initial quantity: "))
                            if quantity <= 0:
                                print("Quantity must be positive")
                                continue
                            break
                        except ValueError:
                            print("Invalid quantity")
                    
                    new_product = {
                        'name': name,
                        'brand': brand,
                        'quantity': quantity,
                        'cost_price': cost_price,
                        'country': country
                    }
                    
                    products.append(new_product)
                    self.restock_items.append({
                        "product": new_product,
                        "quantity": quantity,
                        "cost_price": cost_price,
                        "subtotal": quantity * cost_price
                    })
                    self.total += quantity * cost_price
                    print("Added new product: %s" % name)
                    continue

                product_id = int(product_id) - 1
                if product_id < 0 or product_id >= len(products):
                    print("Invalid ID! Must be between 1-%d" % len(products))
                    continue

                product = products[product_id]
                print("Current stock: %d" % product['quantity'])
                print("Current cost: NRS %.2f" % product['cost_price'])

                quantity = int(input("Enter quantity: "))
                if quantity <= 0:
                    print("Quantity must be positive")
                    continue

                new_price = input("Enter new price (leave blank to keep current): ")
                if new_price:
                    new_price = float(new_price)
                    if new_price <= 0:
                        print("Price must be positive")
                        continue
                    product['cost_price'] = new_price

                self.restock_items.append({
                    "product": product,
                    "quantity": quantity,
                    "cost_price": product['cost_price'],
                    "subtotal": quantity * product['cost_price']
                })

                product['quantity'] += quantity
                self.total += quantity * product['cost_price']
                print("Added %d %s" % (quantity, product['name']))

            except ValueError:
                print("Invalid input")

    def generate_restock_invoice(self):
        if not self.restock_items:
            print("No items restocked")
            return None

        current_dt = datetime.now()
        formatted_date = current_dt.strftime("%Y-%m-%d %H:%M:%S")

        print("\n" + "="*50)
        print("RESTOCK INVOICE".center(50))
        print("="*50)
        print("Date: %s" % formatted_date)
        print("Supplier: %s" % self.supplier_name)
        print("="*50)
        print("%-20s %5s %10s %10s" % 
              ("Product", "Qty", "Price", "Subtotal"))
        print("-"*50)

        for item in self.restock_items:
            p = item['product']
            print("%-20s %5d %9.2f %9.2f" % 
                  (p['name'], item['quantity'], 
                   item['cost_price'], item['subtotal']))

        print("="*50)
        print("TOTAL: NRS %.2f" % self.total)
        print("="*50)
        
        # Save restock invoice
        if save_bill_to_file(
            self.supplier_name,
            "",
            self.restock_items,
            self.total,
            formatted_date,
            "RESTOCK"
        ):
            print("Restock bill saved successfully")
        else:
            print("Error saving restock bill")
            
        return formatted_date
