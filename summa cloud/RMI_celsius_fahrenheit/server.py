from xmlrpc.server import SimpleXMLRPCServer

def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32

server = SimpleXMLRPCServer(("localhost", 9999))

server.register_function(
    celsius_to_fahrenheit,
    "celsius_to_fahrenheit"
)

print("RMI Server is running...")

server.serve_forever()