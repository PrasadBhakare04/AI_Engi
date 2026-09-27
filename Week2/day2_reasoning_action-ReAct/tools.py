def get_product_price(product):
    if product == "iPhone 15":
        return 500
    elif product == "iPhone 17":
        return 1000
    else:
        return 0

def calculator(expression: str) -> str:
    try:
        return eval(expression) 
    except:
        return "calc error!"

