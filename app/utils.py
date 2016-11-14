def get_value(request, name):
    value = request.values[name]
    return None if value == '' else value
