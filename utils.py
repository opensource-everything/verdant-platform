import random, secrets, string


# Generate product ID function
def generate_product_id(length=8):
    return secrets.token_hex(length // 2)

def generate_random_hash(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
