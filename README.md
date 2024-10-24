# Kenneth-Muriel-P1

# Gordy's Novelties Inventory Management System

## Overview

This application is an inventory management system for Gordy's Novelties. It allows users to log in, create accounts, view products, place orders, and for admins to manage users and inventory.

## Features

- User authentication (login and account creation)
- View products with details (name, price, quantity)
- Create orders for products
- Admin functionalities including:
  - View all users and orders
  - Change user roles
  - Add, update, and delete inventory items
  - Mark orders as complete

## Requirements

- Python 3.x
- MySQL Connector for Python (`mysql-connector-python`)
- A MySQL server running locally

## Usage

1. Run the application:
   - python storeapp.py

2. Follow the prompts to log in or create a new account.

3. Users can view products and create orders. Admins can manage users and inventory.

## Logging

The application logs significant actions and errors to `store.log`. Check this file for any issues or to see user activity.