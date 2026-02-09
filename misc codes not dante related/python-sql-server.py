import pyodbc

cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};" #SQL Server
                      "Server=gx-zu2sqld195.database.windows.net;"
                      "Database=brand_dev;"
                      'UID=brandsql_dev_usr;'
                      'PWD=!7T5?H?9*SQRTT9FpvVzSQBWttY&NR;'
                      "Trusted_Connection=no;")

cursor = cnxn.cursor()
cursor.execute('SELECT top 5 * FROM [users].[External_tbl]')

for row in cursor:
    print('row = %r' % (row,))