# utils/helpers.py
def format_price(price: float) -> str:
    return f"{price:.2f} €".replace(".", ",")
