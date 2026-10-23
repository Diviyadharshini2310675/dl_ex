import xmlrpc.client

client = xmlrpc.client.ServerProxy(
    "http://localhost:9999/"
)

n = int(input("Enter number of products: "))

for i in range(n):

    name = input(
        f"Enter product {i + 1} name: "
    )

    price = float(
        input(
            f"Enter price of {name}: "
        )
    )

    result = client.add_product(
        name,
        price
    )

    print(result)

print("\n----- SHOPPING -----")

product = input("Enter product to purchase: ")

quantity = int(
    input("Enter quantity: ")
)

result = client.calculate_bill(
    product,
    quantity
)

if "error" in result:

    print(result["error"])

else:

    print("\n----- BILL -----")

    print("Product:", result["product"])
    print("Price:", result["price"])
    print("Quantity:", result["quantity"])
    print("Total:", result["total"])

    print(
        "Discount:",
        result["discount_percent"],
        "%"
    )

    print(
        "Discount Amount:",
        result["discount"]
    )

    print(
        "Final Amount:",
        result["final_amount"]
    )