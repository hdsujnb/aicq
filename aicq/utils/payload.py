def generate_payload(**kwargs):
    return {key: value for key, value in kwargs.items() if
            value is not None}