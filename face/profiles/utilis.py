import uuid

def get_random_code():
    kod=str(uuid.uuid4())[:8].replace("-","").lower()
    return kod