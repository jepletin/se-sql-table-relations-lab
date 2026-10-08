# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)


# STEP 1
# Return first name, last name, and job title for employees in Boston
df_boston = pd.read_sql("""
    SELECT
        employees.firstName,
        employees.lastName
    FROM employees
    JOIN offices
        ON employees.officeCode = offices.officeCode
    WHERE offices.city = 'Boston'
""", conn)


# STEP 2
# Find offices that have zero employees
df_zero_emp = pd.read_sql("""
    SELECT
        offices.*
    FROM offices
    LEFT JOIN employees
        ON offices.officeCode = employees.officeCode
    WHERE employees.employeeNumber IS NULL
""", conn)


# STEP 3
# Return all employees with their office city and state
df_employee = pd.read_sql("""
    SELECT
        employees.firstName,
        employees.lastName,
        offices.city,
        offices.state
    FROM employees
    LEFT JOIN offices
        ON employees.officeCode = offices.officeCode
    ORDER BY employees.firstName, employees.lastName
""", conn)


# STEP 4
# Return customers who have not placed an order
df_contacts = pd.read_sql("""
    SELECT
        customers.contactFirstName,
        customers.contactLastName,
        customers.phone,
        customers.salesRepEmployeeNumber
    FROM customers
    LEFT JOIN orders
        ON customers.customerNumber = orders.customerNumber
    WHERE orders.orderNumber IS NULL
    ORDER BY customers.contactLastName
""", conn)


# STEP 5
# Return customer contacts with payment amount and payment date
df_payment = pd.read_sql("""
    SELECT
        customers.contactFirstName,
        customers.contactLastName,
        payments.amount,
        payments.paymentDate
    FROM customers
    JOIN payments
        ON customers.customerNumber = payments.customerNumber
    ORDER BY CAST(payments.amount AS REAL) DESC
""", conn)


# STEP 6
# Employees whose customers have an average credit limit over 90,000
df_credit = pd.read_sql("""
    SELECT
        employees.employeeNumber,
        employees.firstName,
        employees.lastName,
        COUNT(customers.customerNumber) AS numcustomers
    FROM employees
    JOIN customers
        ON employees.employeeNumber = customers.salesRepEmployeeNumber
    GROUP BY
        employees.employeeNumber,
        employees.firstName,
        employees.lastName
    HAVING AVG(customers.creditLimit) > 90000
    ORDER BY numcustomers DESC
""", conn)


# STEP 7
# Return products with number of orders and total units sold
df_product_sold = pd.read_sql("""
    SELECT
        products.productName,
        COUNT(orderdetails.orderNumber) AS numorders,
        SUM(orderdetails.quantityOrdered) AS totalunits
    FROM products
    JOIN orderdetails
        ON products.productCode = orderdetails.productCode
    GROUP BY
        products.productCode,
        products.productName
    ORDER BY totalunits DESC
""", conn)


# STEP 8
# Return products and number of different customers who purchased them
df_total_customers = pd.read_sql("""
    SELECT
        products.productName,
        products.productCode,
        COUNT(DISTINCT orders.customerNumber) AS numpurchasers
    FROM products
    JOIN orderdetails
        ON products.productCode = orderdetails.productCode
    JOIN orders
        ON orderdetails.orderNumber = orders.orderNumber
    GROUP BY
        products.productCode,
        products.productName
    ORDER BY numpurchasers DESC
""", conn)


# STEP 9
# Count customers per office
df_customers = pd.read_sql("""
    SELECT
        COUNT(customers.customerNumber) AS n_customers,
        offices.officeCode,
        offices.city
    FROM offices
    JOIN employees
        ON offices.officeCode = employees.officeCode
    JOIN customers
        ON employees.employeeNumber = customers.salesRepEmployeeNumber
    GROUP BY offices.officeCode, offices.city
    ORDER BY offices.officeCode
""", conn)


# STEP 10
# Employees who sold products ordered by fewer than 20 customers
df_under_20 = pd.read_sql("""
    SELECT DISTINCT
        employees.employeeNumber,
        employees.firstName,
        employees.lastName,
        offices.city,
        offices.officeCode
    FROM employees
    JOIN offices
        ON employees.officeCode = offices.officeCode
    JOIN customers
        ON employees.employeeNumber = customers.salesRepEmployeeNumber
    JOIN orders
        ON customers.customerNumber = orders.customerNumber
    JOIN orderdetails
        ON orders.orderNumber = orderdetails.orderNumber
    WHERE orderdetails.productCode IN (
        SELECT orderdetails.productCode
        FROM orderdetails
        JOIN orders
            ON orderdetails.orderNumber = orders.orderNumber
        GROUP BY orderdetails.productCode
        HAVING COUNT(DISTINCT orders.customerNumber) < 20
    )
    ORDER BY employees.lastName ASC
""", conn)
#STEP 11
# Close the connection
conn.close()
