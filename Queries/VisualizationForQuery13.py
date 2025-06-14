# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 23:26:51 2024

@author: ZhangYinhang
"""

import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
db = client['test']


results = list(db.CurrentOrders.aggregate([
    {
        "$addFields": {
            "orderDate": { "$dateFromString": { "dateString": "$orderDate" } }  # 转换字符串为日期
        }
    },
    { 
        "$unwind": "$currentOrderItems" 
    },
    {
        "$group": {
            "_id": {
                "orderDate": { "$dateToString": { "format": "%Y-%m-%d", "date": "$orderDate" } },
                "productType": "$currentOrderItems.productType"
            },
            "totalQuantity": { "$sum": "$currentOrderItems.quantity" }
        }
    },
    {
        "$group": {
            "_id": "$_id.orderDate",
            "sales": {
                "$push": {
                    "productType": "$_id.productType",
                    "totalQuantity": "$totalQuantity"
                }
            }
        }
    },
    {
        "$project": {
            "date": "$_id",
            "sales": 1
        }
    }
]))


data = []
for result in results:
    for sale in result['sales']:
        data.append({
            'date': result['date'],
            'productType': sale['productType'],
            'totalQuantity': sale['totalQuantity']
        })

df = pd.DataFrame(data)


df['date'] = pd.to_datetime(df['date'])  
df = df.sort_values(by='date') 


print(df)


plt.figure(figsize=(12, 6))
for product_type in df['productType'].unique():
    subset = df[df['productType'] == product_type]
    plt.plot(subset['date'], subset['totalQuantity'], marker='o', label=product_type)

plt.title('Daily Sales Quantity by Product Type')
plt.xlabel('Date')
plt.ylabel('Total Sales Quantity')
plt.xticks(rotation=45)
plt.legend(title='Product Type')
plt.tight_layout()
plt.show()
plt.show()