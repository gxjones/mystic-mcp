#!/usr/bin/env python3
"""
A Pizza MCP Server
Minimal example using the mystic-mcp framework
"""

from mystic_mcp import MysticMCP
from typing import Literal

app = MysticMCP()

# Simple pizza data
PIZZA_TYPES = Literal["margherita", "pepperoni", "veggie"]
MENU = {
    "margherita": {"name": "Margherita", "price": 12.99},
    "pepperoni": {"name": "Pepperoni", "price": 15.99},
    "veggie": {"name": "Veggie Deluxe", "price": 14.99},
}

ORDERS = {}


@app.tool()
async def get_menu():
    """Get the pizza menu"""
    result = "MENU:\n"
    for _pizza_id, info in MENU.items():
        result += f"- {info['name']}: ${info['price']}\n"
    return result


@app.tool()
async def order_pizza(pizza_type: PIZZA_TYPES, customer_name: str = "Customer"):
    """Order a pizza"""
    if pizza_type not in MENU:
        return f"Sorry, we don't have {pizza_type}. Try: {', '.join(PIZZA_TYPES)}"

    order_id = f"order-{len(ORDERS) + 1}"
    pizza = MENU[pizza_type]

    ORDERS[order_id] = {
        "pizza": pizza["name"],
        "price": pizza["price"],
        "customer": customer_name,
        "status": "preparing",
    }

    return f"Order {order_id}: {pizza['name']} for {customer_name} - ${pizza['price']}"


@app.tool()
async def check_order(order_id: str):
    """Check order status

    Args:
        order_id: Your order ID
    """
    if order_id not in ORDERS:
        return f"Order {order_id} not found"

    order = ORDERS[order_id]
    return f"Order {order_id}: {order['pizza']} for {order['customer']} - Status: {order['status']}"


if __name__ == "__main__":
    print("Starting the pizza MCP server...")
    app.run()
