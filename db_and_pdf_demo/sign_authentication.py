import sqlalchemy
from sqlalchemy.orm.session import sessionmaker
import hashlib
import uvicorn
from fastapi import FastAPI, UploadFile, File
import multipart
# import jose
from passlib.hash import bcrypt
from validate_email import validate_email
import json
from secrets import token_hex
import tempfile
import pandas as pd
import os



app = FastAPI()

auth_engine = sqlalchemy.create_engine('sqlite:///datacamp.sqlite')
auth_conn = auth_engine.connect()
auth_metadata = sqlalchemy.MetaData()

Auth_Session = sessionmaker(bind=auth_engine)

Authentication = sqlalchemy.Table('Authentication', auth_metadata,
                                  sqlalchemy.Column('ID', sqlalchemy.Integer(), primary_key=True, index=True,
                                                    unique=True),
                                  sqlalchemy.Column('Email', sqlalchemy.String(255), primary_key=False,
                                                    unique=True),
                                  sqlalchemy.Column('Username', sqlalchemy.String(255), primary_key=False,
                                                    unique=True),
                                  sqlalchemy.Column('Password', sqlalchemy.String(255), primary_key=False)
                                  )

auth_session = Auth_Session()
auth_metadata.create_all(auth_engine)

#==========================================================================================================================

tables_db_engine = sqlalchemy.create_engine('sqlite:///tablesDB.sqlite')
tables_db_conn = tables_db_engine.connect()
tables_db_metadata = sqlalchemy.MetaData()

Tables_db_Session = sessionmaker(bind=tables_db_engine)

Tables = sqlalchemy.Table('Tables', tables_db_metadata,
                                  sqlalchemy.Column('ID', sqlalchemy.Integer(), primary_key=True, index=True,
                                                    unique=True),
                                  sqlalchemy.Column('Username', sqlalchemy.String(255), primary_key=False,
                                                    ),
                                  sqlalchemy.Column('TimeStamp', sqlalchemy.String(255), primary_key=False,
                                                    ),
                                  sqlalchemy.Column('Table', sqlalchemy.JSON(), primary_key=False)
                                  )

tables_db_session = Tables_db_Session()
tables_db_metadata.create_all(tables_db_engine)

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
IP = '127.0.0.1'
PORT = 5555


@app.get("/authenticate")
def authenticate(email: str, username: str, password: str) -> dict:
    user_auth = Authentication.select().where(Authentication.columns.Username == username)
    user_auth = auth_session.execute(user_auth).fetchall()
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
    user_auth = auth_session.execute(user_auth).fetchall()
    username_query: bool = user_auth == []
    if not username_query or username == '' or username == " " or len(username) <= 5:
        return {"response": "Username invalid!"}
    if not validate_email(email):
        return {"response": "Invalid email address!"}
    email_auth = Authentication.select().where(Authentication.columns.Email == email)
    email_auth = auth_session.execute(email_auth).fetchall()
    email_query: bool = email_auth == []
    if not email_query:
        return {"response": "Account with the same email exists!"}
        # add in flet a way to allow rewriting the accounts details and rerunning the function
    if password == "" or password == " ":
        return {"response": "Invalid password!"}
    else:
        pass_hash = hashlib.sha256(password.encode()).hexdigest()
        insert_query = sqlalchemy.insert(Authentication).values(Email=email, Username=username, Password=pass_hash)
        auth_session.execute(insert_query)
        auth_session.commit()
        return {"response": "Signed up successfully!"}


@app.get("/update_information")
def update_information(old_username: str, new_username: str, new_email: str, new_password: str) -> dict:
    user_auth = Authentication.select().where(Authentication.columns.Username == old_username)
    user_auth = auth_session.execute(user_auth).fetchall()
    username_query: bool = user_auth == []
    if username_query:
        return {"response": "Username doesn't exist!"}
    other_user_username = Authentication.select().where(Authentication.columns.Username == new_username)
    other_user_username = auth_session.execute(other_user_username).fetchall()
    username_query = other_user_username == []
    if not username_query or new_username == '' or new_username == " " or len(new_username) <= 5:
        return {"response": "Username Taken!"}
    if not validate_email(new_email):
        return {"response": "Invalid email address!"}
    email_auth = Authentication.select().where(Authentication.columns.Email == new_email)
    email_auth = auth_session.execute(email_auth).fetchall()
    email_query: bool = email_auth == []
    if not email_query:
        return {"response": "Account with the same email exists!"}
        # add in flet a way to allow rewriting the accounts details and rerunning the function
    if new_password == "" or new_password == " ":
        return {"response": "Invalid password!"}
    else:
        pass_hash = hashlib.sha256(new_password.encode()).hexdigest()
        update_query = sqlalchemy.update(Authentication).where(Authentication.columns.Username == old_username).values(Email=new_email, Username=new_username, Password=pass_hash)
        auth_session.execute(update_query)
        auth_session.commit()
        return {"response": "Details Updated Successfully!"}


@app.post("/upload_files")
async def upload_files(file_bytes: bytes):
    bytes_variable = file_bytes
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(bytes_variable)
        temp_file_path = temp_file.name

    upload_file_object = UploadFile(filename='filename.pdf', file=open(temp_file_path, "rb"))

    # os.remove(temp_file_path)
    file_extension = upload_file_object.filename.split('.').pop()
    file_name = f'client_data_table0.{file_extension}'
    file_name = pdf_file_name_generator(file_name)
    # file_name = token_hex(10)
    file_path = rf"C:\Users\Sharon's PC\PycharmProjects\anomaly_detection\db_and_pdf_demo\{file_name}"
    with open(file_path, "wb") as f:
        content = await upload_file_object.read()
        f.write(content)
    return {"success": True, "file_path": file_path, "response": "File Uploaded Successfully!"}


def pdf_file_name_generator(file_name: str):
    directory_path = r"C:\Users\Sharon's PC\PycharmProjects\anomaly_detection\db_and_pdf_demo"
    files = os.listdir(directory_path)
    flag = False
    while not flag:
        if file_name in files:
            file_extension = file_name.split('.')[1]
            file_index = str(int(file_name.split('.')[0][-1]) + 1)
            file_name = f"{file_name.split('.')[0][:-1]}{file_index}.{file_extension}"
        else:
            flag = True
    return file_name

#==================================================================================================================================


@app.post("/save_table")
async def save_table(username: str, password: str, time_stamp: str, json_df: str):
    username_auth = Authentication.select().where(Authentication.columns.Username == username)
    username_auth = auth_session.execute(username_auth).fetchall()
    pass_hash = hashlib.sha256(password.encode()).hexdigest()

    if username_auth != []:
        if not any(data[-1] == pass_hash for data in username_auth):
            return {"success": False, "response": "Not Matching Password"}

        insert_query = sqlalchemy.insert(Tables).values(Username=username, TimeStamp=time_stamp, Table=json_df)
        tables_db_session.execute(insert_query)
        tables_db_session.commit()
        return {"success": True, "response": "Table Saved Successfully"}
    else:
        return {"success": False, "response": "Username Does Not Exist"}

def main():
    # query0 = sqlalchemy.insert(Authentication).values(Email='omrid3103@gmail.com', Username='Omri', Password='oiedvdi')
    # session.execute(query0)
    query = Tables.select().where(Tables.columns.Username == "ronnieDagan")
    print(tables_db_session.execute(query).fetchall())
    # session.commit()
    # print(sign_up('omrid310@gmail.com', 'pOmri', 'oiedvdi'))
    # print(sign_in('omrid31@gmail.com', 'pOmri1', 'oiedvdi'))
    """if it doesnt work try: ctrl ? on line 22"""


if __name__ == '__main__':
    main()
    # uvicorn.run(app, host=IP, port=PORT)
