from xmlrpc.server import SimpleXMLRPCServer

products = {}

def add_product(name, price):
    products[name] = price
    return "Product added successfully"


def calculate_bill(name, quantity):

    if name not in products:
        return {
            "error": "Product not found"
        }

    price = products[name]

    total = price * quantity

    if total >= 50000:
        discount_percent = 20
    elif total >= 20000:
        discount_percent = 10
    else:
        discount_percent = 5

    discount = total * discount_percent / 100

    final_amount = total - discount

    return {
        "product": name,
        "price": price,
        "quantity": quantity,
        "total": total,
        "discount_percent": discount_percent,
        "discount": discount,
        "final_amount": final_amount
    }


server = SimpleXMLRPCServer(
    ("localhost", 9999)
)

server.register_function(
    add_product,
    "add_product"
)

server.register_function(
    calculate_bill,
    "calculate_bill"
)

print("Shopping RMI Server Running...")

server.serve_forever()