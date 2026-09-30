from datetime import datetime

def save_products(products):
    try:
        with open('products.txt', 'w') as file:
            for product in products:
                file.write("%s,%s,%d,%.2f,%s\n" % (
                    product['name'],
                    product['brand'],
                    product['quantity'],
                    product['cost_price'],
                    product['country']
                ))
        return True
    except Exception as e:
        print("Error saving products: " + str(e))
        return False

def save_bill_to_file(customer_name, phone_number, cart_items, total_amount, date, invoice_type="SALE"):
    try:
        # Generate timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create unique filename
        if invoice_type == "SALE":
            filename = "sale_" + customer_name + "_" + timestamp + ".txt"
        else:
            filename = "restock_" + customer_name + "_" + timestamp + ".txt"
        
        # Write invoice content
        with open(filename, 'w') as file:
            # Store header
            file.write("="*50 + "\n")
            file.write("LooksMax Beauty & Skin Care\n".center(50))
            file.write("Lagankhel, Lalitpur\n".center(50))
            file.write("="*50 + "\n\n")
            
            # Invoice metadata
            file.write("Date: " + date + "\n")
            file.write("Customer: " + customer_name + "\n")
            if phone_number:
                file.write("Phone: " + phone_number + "\n")
            file.write("="*50 + "\n")
            
            # Items header
            if invoice_type == "SALE":
                file.write("%-20s %4s %4s %10s %10s\n" % 
                          ("Product", "Qty", "Free", "Price", "Subtotal"))
            else:
                file.write("%-20s %5s %10s %10s\n" % 
                          ("Product", "Qty", "Price", "Subtotal"))
            
            file.write("-"*50 + "\n")
            
            # Items list
            for item in cart_items:
                if invoice_type == "SALE":
                    file.write("%-20s %4d %4d %9.2f %9.2f\n" % (
                        item["product"]["name"],
                        item["quantity"],
                        item.get("free_items", 0),
                        item.get("selling_price", 0),
                        item["subtotal"]))
                else:
                    file.write("%-20s %5d %9.2f %9.2f\n" % (
                        item["product"]["name"],
                        item["quantity"],
                        item["cost_price"],
                        item["subtotal"]))
            
            # Footer
            file.write("="*50 + "\n")
            file.write("TOTAL: NRS %.2f\n" % total_amount)
            file.write("="*50 + "\n")
            file.write("Thank you for your business!\n")
        
        print("Invoice saved as: " + filename)
        return True
    except Exception as e:
        print("Error saving bill: " + str(e))
        return False
