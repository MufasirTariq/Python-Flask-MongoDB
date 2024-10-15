from .resources import CustomerAPI

def initialize_routes(api):
    api.add_resources(CustomerAPI, "/api/registerCustomer")