from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# Sample data (Replace with a database later)
prices = {
    "bag_of_ice_2kg": 15.00,
    "bag_of_ice_3kg": 22.00,
    "biltong_leaf_50g": 18.00
}

stock = {
    "bag_of_ice_2kg": 100,
    "bag_of_ice_3kg": 50,
    "biltong_leaf_50g": 100
}

orders = []

# ✅ 1. Price Lookup API
@app.get("/get_price")
def get_price(item: str):
    if item in prices:
        return {"item": item, "price": prices[item]}
    raise HTTPException(status_code=404, detail="Item not found")

# ✅ 2. Stock Availability API
@app.get("/check_stock")
def check_stock(item: str):
    if item in stock:
        return {"item": item, "stock": stock[item]}
    raise HTTPException(status_code=404, detail="Item not found")

# ✅ 3. Order Processing API
class Order(BaseModel):
    item: str
    quantity: int
    customer_name: str
    contact_number: str

@app.post("/place_order")
def place_order(order: Order):
    if order.item not in stock:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if stock[order.item] < order.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    stock[order.item] -= order.quantity  # Reduce stock
    orders.append(order.dict())  # Save order
    
    return {"message": "Order placed successfully", "order_details": order.dict()}

# ✅ 4. View All Orders (For Admin Use)
@app.get("/orders")
def get_orders():
    return {"orders": orders}
