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

tools_desc = [
        {
            "type": "function",
            "function": {
                "name": "calculator",
                "description": "Evaluate a mathematical expression",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "The mathematical expression to evaluate",
                        }
                    },
                    "required": ["expression"],
                },
            },
        },

        {
            "type": "function",
            "function": {
                "name": "get_product_price",
                "description": "Get the price of a product",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product": {
                            "type": "string",
                            "description": "The product name, e.g. iPhone 15, iPhone 17"
                        }
                    },
                    "required": ["product"]
                }
            }
        }   
    ]