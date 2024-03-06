import sqlalchemy
from sqlalchemy.orm.session import sessionmaker
import hashlib
import uvicorn
from fastapi import FastAPI
from validate_email import validate_email


app = FastAPI()
engine = sqlalchemy.create_engine('sqlite:///datacamp.sqlite')
conn = engine.connect()
metadata = sqlalchemy.MetaData()

Session = sessionmaker(bind=engine)

Authentication = sqlalchemy.Table('Authentication', metadata,
                                  sqlalchemy.Column('ID', sqlalchemy.Integer(), primary_key=True, index=True,
                                                    unique=True),
                                  sqlalchemy.Column('Email', sqlalchemy.String(255), primary_key=False,
                                                    unique=True),
                                  sqlalchemy.Column('Username', sqlalchemy.String(255), primary_key=False,
                                                    unique=True),
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


"""Completed sign-in method"""


@app.get("/authenticate")
def authenticate(email: str, username: str, password: str) -> dict:
    user_auth = Authentication.select().where(Authentication.columns.Username == username)
    user_auth = session.execute(user_auth).fetchall()
    user_not_exist: bool = user_auth == []

    if user_not_exist:
        return {'response': "Username doesnt exist!", "authentication": False}

    if not any(data[-3] == email for data in user_auth):
        return {'response': "Invalid email!", "authentication": False}

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if not any(data[-1] == hashed_password for data in user_auth):
        return {'response': "Not matching password!", "authentication": False}

    return {'response': "Signing in...", "authentication": True}


"""Completed sign-up func"""


@app.get("/sign_up")
def sign_up(email: str, username: str, password: str) -> dict:
    user_auth = Authentication.select().where(Authentication.columns.Username == username)
    user_auth = session.execute(user_auth).fetchall()
    username_query: bool = user_auth == []
    if not username_query or username == '' or username == " " or len(username) <= 5:
        return {"response": "Username invalid!"}
    if not validate_email(email):
        return {"response": "Invalid email address!"}
    email_auth = Authentication.select().where(Authentication.columns.Email == email)
    email_auth = session.execute(email_auth).fetchall()
    email_query: bool = email_auth == []
    if not email_query:
        return {"response": "Account with the same email exists!"}
        # add in flet a way to allow rewriting the accounts details and rerunning the function
    if password == "" or " ":
        return {"response": "Invalid password!"}
    else:
        pass_hash = hashlib.sha256(password.encode()).hexdigest()
        insert_query = sqlalchemy.insert(Authentication).values(Email=email, Username=username, Password=pass_hash)
        session.execute(insert_query)
        session.commit()
        return {"response": "Signed up successfully!"}



def main():
    # query0 = sqlalchemy.insert(Authentication).values(Email='omrid3103@gmail.com', Username='Omri', Password='oiedvdi')
    # session.execute(query0)
    query = Authentication.select().where(Authentication.columns.Username != '')
    print(session.execute(query).fetchall())
    # session.commit()
    # print(sign_up('omrid310@gmail.com', 'pOmri', 'oiedvdi'))
    # print(sign_in('omrid31@gmail.com', 'pOmri1', 'oiedvdi'))
    """if it doesnt work try: ctrl ? on line 22"""


if __name__ == '__main__':
    # main()
    uvicorn.run(app, host="127.0.0.1", port=5555)