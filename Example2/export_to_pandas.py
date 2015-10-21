#!/usr/bin/python
import pandas as pd
# import numpy as pd
import sqlalchemy as sa

engine = sa.create_engine('sqlite:///sensors.db', echo=False)

con = engine.connect()

dfs = []

for table in ('tf_temp', 'tf_light'):
    sql_query = "SELECT * FROM {0}".format(table)
    df = pd.read_sql(sql_query, engine).set_index('id')
    df['type'] = table
    print df


import StringIO

fid = StringIO.StringIO()

df.to_csv(fid)
# print fid.getvalue()
# erg = con.execute(sql_query)

# df = pd.DataFrame(erg.fetchall())
# df.columns = erg.keys()
# print df

# query = erg.fetchall()
# for x in query:
#     print x
