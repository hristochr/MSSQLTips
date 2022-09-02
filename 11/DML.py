import pyodbc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
                        SERVER=.;\
                        DATABASE=AdventureWorks2019;\
                        Trusted_Connection=yes;\
                        auto_commit=false;\
                        timeout=60')
cursor = conn.cursor()

result = cursor.execute('SELECT TOP 15 COUNT(p.FirstName) count, a.PostalCode\
                        FROM Person.Person p\
                        JOIN Person.BusinessEntityAddress bea ON p.BusinessEntityID = bea.BusinessEntityID\
                        JOIN Person.Address a ON a.AddressID = bea.AddressID\
                        GROUP BY a.PostalCode\
                        ORDER BY COUNT(p.FirstName) DESC')
rows = result.fetchall()

cols = []
for i,_ in enumerate(result.description):
    cols.append(result.description[i][0])

df = pd.DataFrame(np.array(rows), columns=cols)
df['count'] = pd.to_numeric(df['count'])
print(df)
plt.barh(df['PostalCode'], df['count'])
plt.show()


# for table in cursor.tables(schema='HumanResources', tableType='TABLE'):
#     print(table.table_name)

# keys = ('table_cat','table_schem','table_name','non_unique','index_qualifier','index_name','type',
# 'ordinal_position','column_name','asc_or_desc','cardinality','pages','filter_condition')

# for row in cursor.statistics(table='Department',schema='HumanResources'):
#     print(dict(zip(keys,row)))

# top_var = 100
# result = cursor.execute('SELECT TOP (?) * FROM Sales.SalesOrderHeader', top_var)
# print(result.description[:3])

# top_var = 5
# total_due_limit = 2000
# asc = False
# desc = True
# order_by_cols = ', '.join(['OrderDate', 'SalesOrderID'])
# sort_dir = 'DESC' if desc == True else 'ASC'
# result = cursor.execute(f'SELECT TOP (?) * FROM Sales.SalesOrderHeader\
#                          WHERE TotalDue <= ?\
#                          ORDER BY {order_by_cols} {sort_dir}', (top_var, total_due_limit))
# rows = result.fetchall()
# for row in rows:
#     print(f'{row.SalesOrderNumber}: \n {row.CustomerID} ${row.TotalDue:.2f}')
#
#
# var_top = 5
# result = cursor.execute('SELECT TOP (?) p.FirstName, p.LastName, a.PostalCode\
#                         FROM Person.Person p\
#                         JOIN Person.BusinessEntityAddress bea ON p.BusinessEntityID = bea.BusinessEntityID\
#                         JOIN Person.Address a ON a.AddressID = bea.AddressID\
# #                         ORDER BY p.LastName, p.FirstName', var_top)
# # for row in result:
# #     print(row)
