import sqlalchemy
from sqlalchemy.orm.session import sessionmaker
import hashlib

engine = sqlalchemy.create_engine('sqlite:///datacamp.sqlite')
conn = engine.connect()
metadata = sqlalchemy.MetaData()

Session = sessionmaker(bind=engine)

Authentication = sqlalchemy.Table('Authentication', metadata,
    sqlalchemy.Column('ID', sqlalchemy.Integer(), primary_key=True, index=True, unique=True),
    sqlalchemy.Column('Email', sqlalchemy.String(255), primary_key=False, unique=True),
    sqlalchemy.Column('Username', sqlalchemy.String(255), primary_key=False, unique=True),
    sqlalchemy.Column('Password', sqlalchemy.String(255), primary_key=False)
)

session = Session()
metadata.create_all(engine)
# query = sqlalchemy.insert(HumanResources).values(DepartmentID=17, Name='Mathematics', GroupName='math')
# session.execute(query)
# session.commit()

# json_table = str(df.to_json())
# print(json_table)
# json_query = sqlalchemy.insert(json_data_table).values(json=json_table)
# session.execute(json_query)
# session.commit()

# query2 = HumanResources.select().where(HumanResources.columns.Name != '')
# Result = session.execute(query2)
# print(Result.fetchall())
# json_query2 = json_data_table.select().where(json_data_table.columns.json != '')
# json_Result = session.execute(json_query2)
# print(json_Result.fetchall())
# query = sqlalchemy.insert(Authentication).values(ID=0, Username='Omri', Password='oiedvdi')
# session.execute(query)
# query: bool = Authentication.select().where(Authentication.columns.Username == 'Omri') ==
# json_Result = session.execute(query)
# print(json_Result.fetchall())

def Sign_Up(email: str, username: str, password: str):
     username_query: bool = Authentication.select().where(Authentication.columns.Username == username) == ''
     session.commit()
     if username_query:
         pass_hash = hashlib.sha256(password.encode()).hexdigest()
         insert_query = sqlalchemy.insert(Authentication).values(Email=email, Username=username, Password=pass_hash)
         session.execute(insert_query)
         session.commit()
         return "Signed up successfully!"
     else:
         Sign_in(email, username, password)
         return None

def Sign_in(email: str, username: str, password: str):
         pass









