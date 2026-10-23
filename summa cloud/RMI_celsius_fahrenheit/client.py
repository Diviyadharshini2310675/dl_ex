import xmlrpc.client

client = xmlrpc.client.ServerProxy(
    "http://localhost:9999/"
)

celsius = float(
    input("Enter temperature in Celsius: ")
)

fahrenheit = client.celsius_to_fahrenheit(celsius)

print(
    "Temperature in Fahrenheit:",
    fahrenheit
)