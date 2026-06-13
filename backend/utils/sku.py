import random


def generate_sku(catergory: str, name: str) -> str:
    clean_cat = "".join(letter for letter in catergory if letter.isalnum()).upper()
    clean_name = "".join(letter for letter in name if letter.isalnum()).upper()

    cat_prefix = clean_cat[:4].ljust(4, "X")
    prod_prefix = clean_name[:3].ljust(3, "X")
    random_suffix = random.randint(1000, 9999)

    return f"{cat_prefix}-{prod_prefix}-{random_suffix}"
