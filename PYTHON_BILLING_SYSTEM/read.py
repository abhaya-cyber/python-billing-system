def get_products():
    products = []
    try:
        with open('products.txt', 'r') as file:
            for line in file:
                if line and line != '\n':
                    parts = line.split(',')
                    if len(parts) == 5:
                        name = parts[0]
                        brand = parts[1]
                        quantity = int(parts[2])
                        cost_price = float(parts[3])
                        country = parts[4].replace('\n', '')
                        products.append({
                            'name': name,
                            'brand': brand,
                            'quantity': quantity,
                            'cost_price': cost_price,
                            'country': country
                        })
    except FileNotFoundError:
        print("\nProducts file not found. Creating a new one...")
        open('products.txt', 'a').close()
    except Exception as e:
        print("\nError reading products: " + str(e))
    return products
