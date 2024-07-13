def validate_product_data(data):
    required_fields = ['name', 'description', 'price', 'category', 'stock_quantity']
    for field in required_fields:
        if field not in data:
            return False, f"Field {field} is required."
    return True, None

def validate_appointment_data(data):
    required_fields = ['service_type', 'appointment_date']
    for field in required_fields:
        if field not in data:
            return False, f"Field {field} is required."
    return True, None
