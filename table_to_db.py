import sqlalchemy
from sqlalchemy.orm.session import sessionmaker
from db1 import df

engine = sqlalchemy.create_engine('sqlite:///datacamp.sqlite')
conn = engine.connect()
metadata = sqlalchemy.MetaData()

Session = sessionmaker(bind=engine)

HumanResources = sqlalchemy.Table('HumanResources', metadata,
    sqlalchemy.Column('DepartmentID', sqlalchemy.Integer(), primary_key=True),
    sqlalchemy.Column('Name', sqlalchemy.String(255), primary_key=False),
    sqlalchemy.Column('GroupName', sqlalchemy.String(255), primary_key=False)
)
json_data_table = sqlalchemy.Table('json_data_table', metadata,
                                   sqlalchemy.Column('json', sqlalchemy.String(), primary_key=True))




session = Session()

metadata.create_all(engine)
# query = sqlalchemy.insert(HumanResources).values(DepartmentID=17, Name='Mathematics', GroupName='math')
# session.execute(query)
# session.commit()
#
# df.to_sql(
#     name='HumanResources',
#     con=engine,
#     if_exists='append',
#     index=False,
# )
json_table = str(df.to_json())
print(json_table)
json_query = sqlalchemy.insert(json_data_table).values(json=json_table)
session.execute(json_query)
session.commit()

# query2 = HumanResources.select().where(HumanResources.columns.Name != '')
# Result = session.execute(query2)
# print(Result.fetchall())
json_query2 = json_data_table.select().where(json_data_table.columns.json != '')
json_Result = session.execute(json_query2)
print(json_Result.fetchall())