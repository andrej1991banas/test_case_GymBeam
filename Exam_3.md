## In process of creating transofrmation 
**Stretol som sa s touto chybou a neviem si s nou poradit a odstrániť.**
Určite môžem skúsiť upraviť dáta cez Pythonovi kód a zaslať vám skripty. 
```plain
Query "CREATE OR REPLACE TABLE cleaned_input_table AS SELECT
"TransactionID",
COALESCE(NULLIF("Category", ''), 'Unknown') AS "Category",
COALESCE(NULLIF("Product", ''), 'Unknown') AS "Product",
COALESCE(NULLIF("TransactionDate", ''), '1970-01-01') AS "TransactionDate",
"Quantity",
"Price",
"TotalValue",
"CustomerID",
"PaymentMethod",
"ShippingAddress",
"Email",
"OrderStatus",
"DiscountCode",
"PaymentAmount" FROM schema."input_table";"
in "Code 1" failed with error: "Error "odbc_prepare():
SQL error: SQL compilation error: Schema 'KEBOOLA_24738.SCHEMA' does not exist or not authorized.,
SQL state 02000 in SQLPrepare" while executing query "CREATE OR REPLACE TABLE cleaned_input_table AS SELECT
"TransactionID",
COALESCE(NULLIF("Category", ''), 'Unknown') AS "Category",
COALESCE(NULLIF("Product", ''), 'Unknown') AS "Product",
COALESCE(NULLIF("TransactionDate", ''), '1970-01-01') AS "TransactionDate",
"Quantity",
"Price",
"TotalValue",
"CustomerID",
"PaymentMethod",
"ShippingAddress",
"Email",
"OrderStatus",
"DiscountCode",
"PaymentAmount"
FROM schema."input_table";""
```
