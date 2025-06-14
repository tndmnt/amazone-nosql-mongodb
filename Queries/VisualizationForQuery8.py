
# -*- coding: utf-8 -*-
"""
Spyder 编辑器

这是一个临时脚本文件。用于更新数据集
"""
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['test']

results = list(db.CurrentOrders.aggregate([
    { "$unwind": "$currentOrderItems" },
    { 
        "$group": {
            "_id": "$currentOrderItems.product_id", 
            "totalSalesQuantity": { "$sum": "$currentOrderItems.quantity" }
        }
    },
    { 
        "$lookup": {
            "from": "DailyInventoryLevel",
            "localField": "_id",
            "foreignField": "product_id",
            "as": "inventoryDetails"
        }
    },
    { 
        "$unwind": { 
            "path": "$inventoryDetails",
            "preserveNullAndEmptyArrays": True 
        }
    },
    { 
        "$lookup": {
            "from": "FreshProducts",
            "localField": "_id",
            "foreignField": "product_id",
            "as": "freshProductDetails"
        }
    },
    { 
        "$lookup": {
            "from": "OtherProducts",
            "localField": "_id",
            "foreignField": "product_id",
            "as": "otherProductDetails"
        }
    },
    { 
        "$unwind": { 
            "path": "$freshProductDetails", 
            "preserveNullAndEmptyArrays": True 
        }
    },
    { 
        "$unwind": { 
            "path": "$otherProductDetails", 
            "preserveNullAndEmptyArrays": True 
        }
    },
    { 
        "$project": {
            "productId": '$_id', 
            "totalSalesQuantity": 1,
            "currentInventory": { "$ifNull": ['$inventoryDetails.inventoryQuantity', 0] },
            "totalSalesValue": {
                "$multiply": [
                    "$totalSalesQuantity",
                    {
                        "$cond": {
                            "if": { "$gt": ['$freshProductDetails.standardPrice', 0] },
                            "then": '$freshProductDetails.standardPrice',
                            "else": { "$ifNull": ['$otherProductDetails.standardPrice', 0] }
                        }
                    }
                ]
            }
        }
    }
]))


df = pd.DataFrame(results)


print(df)


plt.figure(figsize=(12, 6))
plt.bar(df['productId'], df['totalSalesQuantity'], label='Total Sales Quantity')
plt.title('Total Sales Quantity by Product')
plt.xlabel('Product ID')
plt.ylabel('Total Quantity')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
plt.figure(figsize=(12, 6))
plt.bar(df['productId'], df['totalSalesValue'], label='Total Sales Value', color='orange')
plt.title('Total Sales Value by Product')
plt.xlabel('Product ID')
plt.ylabel('Total Sales Value')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
