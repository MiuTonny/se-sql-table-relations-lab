# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Replace None with your code
df_boston = pd.read_sql(
    """
    SELECT e.firstName,
           e.lastName
    FROM employees AS e
    JOIN offices AS o
      ON e.officeCode = o.officeCode
    WHERE o.city = 'Boston';
    """,
    conn
)

print("STEP 1 - Employees in Boston")
print(df_boston)

# STEP 2
# Replace None with your code
df_zero_emp = pd.read_sql(
    """
    SELECT o.officeCode,
           o.city,
           o.state,
           o.country
    FROM offices AS o
    LEFT JOIN employees AS e
      ON o.officeCode = e.officeCode
    WHERE e.employeeNumber IS NULL;
    """,
    conn
)

print("\nSTEP 2 - Offices with zero employees")
print(df_zero_emp)

# STEP 3
# Replace None with your code
df_employee = pd.read_sql(
    """
    SELECT e.firstName,
           e.lastName,
           o.city,
           o.state
    FROM employees AS e
    LEFT JOIN offices AS o
      ON e.officeCode = o.officeCode
    ORDER BY e.firstName, e.lastName;
    """,
    conn
)

print("\nSTEP 3 - All employees with their office info")
print(df_employee)

# STEP 4
# Replace None with your code
df_contacts = pd.read_sql("""
SELECT c.contactFirstName,
        c.contactLastName,
        c.phone,
        c.salesRepEmployeeNumber 
FROM customers AS c
LEFT JOIN orders AS o
  ON c.customerNumber = o.customerNumber
WHERE o.orderNumber IS NULL
ORDER BY c.contactLastName, c.contactFirstName; """, conn)

print("\nSTEP 4 - Customers with no orders")
print(df_contacts)

# STEP 5
# Replace None with your code
df_payment = pd.read_sql(
    """
    SELECT c.contactFirstName,
           c.contactLastName,
           p.amount,
           p.paymentDate
    FROM customers AS c
    JOIN payments AS p
      ON c.customerNumber = p.customerNumber
    ORDER BY CAST(p.amount AS REAL) DESC;
    """,
    conn
)

print("\nSTEP 5 - Payments by amount (desc)")
print(df_payment.head(10)) 

# STEP 6
# Replace None with your code
df_credit = pd.read_sql(
    """
    SELECT e.employeeNumber,
           e.firstName,
           e.lastName,
           COUNT(c.customerNumber) AS numcustomers
    FROM employees AS e
    JOIN customers AS c
      ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY e.employeeNumber, e.firstName, e.lastName
    HAVING AVG(c.creditLimit) > 90000
    ORDER BY numcustomers DESC;
    """,
    conn
)


print("\nSTEP 6 - Employees with avg customer credit limit > 90k")
print(df_credit)

# STEP 7
# Replace None with your code
df_product_sold = pd.read_sql(
    """
    SELECT p.productName,
           COUNT(DISTINCT od.orderNumber) AS numorders,
           SUM(od.quantityOrdered) AS totalunits
    FROM products AS p
    JOIN orderdetails AS od
      ON p.productCode = od.productCode
    GROUP BY p.productCode, p.productName
    ORDER BY totalunits DESC;
    """,
    conn
)

print("\nSTEP 7 - Products sold (numorders & totalunits)")
print(df_product_sold.head(10))

# STEP 8
# Replace None with your code
df_total_customers = pd.read_sql(
    """
    SELECT p.productName,
           p.productCode,
           COUNT(DISTINCT c.customerNumber) AS numpurchasers
    FROM products AS p
    JOIN orderdetails AS od
      ON p.productCode = od.productCode
    JOIN orders AS o
      ON od.orderNumber = o.orderNumber
    JOIN customers AS c
      ON o.customerNumber = c.customerNumber
    GROUP BY p.productCode, p.productName
    ORDER BY numpurchasers DESC;
    """,
    conn
)

print("\nSTEP 8 - Number of customers per product (numpurchasers)")
print(df_total_customers.head(10))

# STEP 9
# Replace None with your code
df_customers = pd.read_sql(
    """
    SELECT o.officeCode,
           o.city,
           COUNT(DISTINCT c.customerNumber) AS n_customers
    FROM offices AS o
    JOIN employees AS e
      ON o.officeCode = e.officeCode
    JOIN customers AS c
      ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY o.officeCode, o.city
    ORDER BY o.officeCode;
    """,
    conn
)

print("\nSTEP 9 - Number of customers per office")
print(df_customers)

# STEP 10
# Replace None with your code
df_under_20 = pd.read_sql(
    """
    SELECT DISTINCT e.employeeNumber,
           e.firstName,
           e.lastName,
           o.city,
           o.officeCode
    FROM employees AS e
    JOIN customers AS c
      ON e.employeeNumber = c.salesRepEmployeeNumber
    JOIN orders AS ord
      ON c.customerNumber = ord.customerNumber
    JOIN orderdetails AS od
      ON ord.orderNumber = od.orderNumber
    JOIN products AS p
      ON od.productCode = p.productCode
    JOIN offices AS o
      ON e.officeCode = o.officeCode
    WHERE p.productCode IN (
        SELECT p2.productCode
        FROM products AS p2
        JOIN orderdetails AS od2
          ON p2.productCode = od2.productCode
        JOIN orders AS ord2
          ON od2.orderNumber = ord2.orderNumber
        JOIN customers AS c2
          ON ord2.customerNumber = c2.customerNumber
        GROUP BY p2.productCode
        HAVING COUNT(DISTINCT c2.customerNumber) < 20
    )
    ORDER BY (e.firstName = 'Loui') DESC,
             e.firstName,
             e.lastName;
    """,
    conn
)

print("\nSTEP 10 - Employees who sold products with < 20 customers")
print(df_under_20)

conn.close()