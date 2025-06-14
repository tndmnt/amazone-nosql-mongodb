# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 13:12:54 2024

@author: ZhangYinhang
"""

import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
db = client['task1'] 


results = list(db.CurrentOrders.aggregate([
    {
      "$addFields": {
        "orderDate": {
          "$dateFromString": {
            "dateString": '$orderDate'
          }
        }
      }
    },
    { "$match": { "orderStatus": 'paid' } },
    { "$unwind": { "path": '$currentOrderItems' } },
    {
      "$lookup": {
        "from": 'Products',
        "localField": 'currentOrderItems.product_id',
        "foreignField": 'product_id',
        "as": 'productDetails'
      }
    },
    {
      "$unwind": {
        "path": '$productDetails',
        "preserveNullAndEmptyArrays": True
      }
    },
    {
      "$group": {
        "_id": '$currentOrderItems.product_id',
        "totalSalesQuantity": {
          "$sum": '$currentOrderItems.quantity'
        },
        "totalSalesValue": {
          "$sum": {
            "$multiply": [
              '$currentOrderItems.quantity',
              '$productDetails.cost'
            ]
          }
        }
      }
    },
    {
      "$unionWith": {
        "coll": 'PastOrders',
        "pipeline": [
          { "$unwind": '$pastOrderItems' },
          {
            "$lookup": {
              "from": 'Products',
              "localField": 'pastOrderItems.product_id',
              "foreignField": 'product_id',
              "as": 'productDetails'
            }
          },
          {
            "$unwind": {
              "path": '$productDetails',
              "preserveNullAndEmptyArrays": True
            }
          },
          {
            "$group": {
              "_id": '$pastOrderItems.product_id',
              "totalSalesQuantity": {
                "$sum": '$pastOrderItems.quantity'
              },
              "totalSalesValue": {
                "$sum": {
                  "$multiply": [
                    '$pastOrderItems.quantity',
                    '$productDetails.cost'
                  ]
                }
              }
            }
          }
        ]
      }
    },
    {
      "$group": {
        "_id": '$_id',
        "totalQuantity": {
          "$sum": '$totalSalesQuantity'
        },
        "totalSalesValue": {
          "$sum": '$totalSalesValue'
        }
      }
    },
    {
      "$project": {
        "productId": '$_id',
        "totalQuantity": 1,
        "totalSalesValue": 1
      }
    }
]))


df = pd.DataFrame(results)


print(df)


plt.figure(figsize=(12, 6))
plt.bar(df['productId'], df['totalQuantity'], color='skyblue')
plt.title('Total Sales Quantity by Product')
plt.xlabel('Product ID')
plt.ylabel('Total Quantity Sold')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
plt.bar(df['productId'], df['totalSalesValue'], color='orange')
plt.title('Total Sales Value by Product')
plt.xlabel('Product ID')
plt.ylabel('Total Sales Value')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()