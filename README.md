# Amazone NoSQL Database Project

This project simulates a NoSQL database for **Amazone**, a UK-based e-commerce platform expanding into same-day grocery delivery through a partnership with **Morrizon**. Built using **MongoDB**, the system integrates both traditional product ordering and real-time logistics for fresh grocery fulfillment via partner drivers.

## Project Structure

- **Collections**: Includes JSON files for customers, products (fresh and non-fresh), partners, orders (past/current), ratings, inventory, and store data.
- **Queries**: JSON files and Python scripts demonstrating operations like product search, order placement, delivery assignment, and performance tracking.
- **Results**: Output of each query in JSON format.
- **Visualizations**: Python scripts using `matplotlib` and `pandas` for plotting sales and inventory trends.

## Features

- **Schema Design**: Custom-designed NoSQL schema with denormalized collections optimized for query performance.
- **Product Types**: Supports books, CDs, mobile phones, home appliances, and three fresh product categories (bakery, drinks, fruits & vegetables).
- **Fresh Delivery Integration**: Includes store-partner-product mapping and real-time partner selection logic based on availability and proximity.
- **Inventory Tracking**: Logs daily inventory levels for each product.
- **Ratings & Recommendations**: Sparse product ratings with recommended items generated for each customer.
- **Indexing**: Indexed key collections to optimize high-frequency queries.
- **Aggregations**: Uses MongoDB’s aggregation pipeline for analytics and performance reporting.

## File Highlights

- `Collections/` – 15+ JSON datasets including products, stores, orders, ratings, etc.
- `Queries/` – Query logic for customer behavior, manager analytics, delivery routing, and more.
- `Results/` – Output JSON files showing the result of each query.
- `VisualizationForQueryX.py` – Python scripts that convert query results into tables or charts.

## How to Run

1. Import JSON files into MongoDB using Compass or Shell.
2. Run queries via:
   - MongoDB Compass or Shell
   - Python scripts provided (requires `pymongo`, `pandas`, `matplotlib`)
3. View JSON outputs in the `Results/` folder or visualize selected queries via `.py` scripts.
