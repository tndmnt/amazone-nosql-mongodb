# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 12:47:59 2024

@author: ZhangYinhang
"""

import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['task1']  

results = list(db.PastOrders.aggregate([
    { "$unwind": "$pastOrderItems" },
    {
        "$group": {
            "_id": "$pastOrderItems.product_id",
            "totalQuantity": { "$sum": "$pastOrderItems.quantity" },
            "averageRating": { "$avg": "$pastOrderItems.rate" }
        }
    },
    {
        "$lookup": {
            "from": "Products",
            "localField": "_id",
            "foreignField": "product_id",
            "as": "productDetails"
        }
    },
    {
        "$unwind": {
            "path": "$productDetails",
            "preserveNullAndEmptyArrays": True
        }
    },
    {
        "$project": {
            "productId": '$_id',
            "totalQuantity": 1,
            "averageRating": 1,
            "productName": '$productDetails.productName'
        }
    }
]))


df = pd.DataFrame(results)


print(df)


plt.figure(figsize=(12, 6))
plt.bar(df['productName'], df['totalQuantity'])
plt.title('Total Sales Quantity by Product')
plt.xlabel('Product Name')
plt.ylabel('Total Quantity')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
plt.figure(figsize=(12, 6))
plt.bar(df['productName'], df['averageRating'], color='orange')
plt.title('Average Rating by Product')
plt.xlabel('Product Name')
plt.ylabel('Average Rating')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()