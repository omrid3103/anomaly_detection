import time
import sqlalchemy
from sqlalchemy.orm.session import sessionmaker
import hashlib
import uvicorn
from fastapi import FastAPI, UploadFile, File, Request
from validate_email import validate_email
import json
import tempfile
import pandas as pd
import os
from kmeans_clustering import *
from kmc_controller import *
import io
from io import StringIO
from cryptography.fernet import Fernet
import pdfplumber
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address



SECRET_KEY: bytes = b'M2UzYmRjYTg4MWZlMTRlYmRjMWU4YTMwYjVlYzg4MWQ='
ACCESS_TOKEN_EXPIRE_SECONDS: float = 1800.0

"""
    Log-In:
        auth: check
            def encrypt_token(name: str, pass: str) -> str:
                text = f"{name}|{pass}|{time.time()}"
                f = Fernet(SECRET_KEY)
                return f.encrypt(text) 
"""

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ==========================================================================================================================

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

# ==========================================================================================================================

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
                                  sqlalchemy.Column('Table', sqlalchemy.JSON(), primary_key=False
                                                    ),
                                  sqlalchemy.Column('Groups', sqlalchemy.JSON(), primary_key=False
                                                    ),
                                  )

tables_db_session = Tables_db_Session()
tables_db_metadata.create_all(tables_db_engine)

# ==========================================================================================================================

files_db_engine = sqlalchemy.create_engine('sqlite:///filesDB.sqlite')
files_db_conn = files_db_engine.connect()
files_db_metadata = sqlalchemy.MetaData()

Files_db_Session = sessionmaker(bind=files_db_engine)

Files = sqlalchemy.Table('Files', files_db_metadata,
                                  sqlalchemy.Column('ID', sqlalchemy.Integer(), primary_key=True, index=True,
                                                    unique=True),
                                  sqlalchemy.Column('Username', sqlalchemy.String(255), primary_key=False,
                                                    ),
                                  sqlalchemy.Column('FileName', sqlalchemy.String(255), primary_key=False,
                                                    ),
                                  sqlalchemy.Column('FileContent', sqlalchemy.JSON(), primary_key=False)
                                  )

files_db_session = Files_db_Session()
files_db_metadata.create_all(files_db_engine)

# ==========================================================================================================================
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


def encrypt_token(username: str, pwd: str) -> str:
    text = f"{username}|{pwd}|{time.time()}"
    f = Fernet(SECRET_KEY)
    return f.encrypt(text.encode()).decode()


def decrypt_token(token: str) -> dict[str, str | bool]:
    f = Fernet(SECRET_KEY)
    decrypted_bytes = f.decrypt(token)
    decrypted_text = decrypted_bytes.decode()
    if time.time() - float(decrypted_text.split('|')[-1]) > ACCESS_TOKEN_EXPIRE_SECONDS:
        return {"is_expired": True}
    return {"is_expired": False, "token": decrypted_text}


@app.get("/authenticate")
@limiter.limit("100/minute")
def authenticate(request: Request, email: str, username: str, password: str) -> dict:
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

    token = encrypt_token(username=username, pwd=password)
    return {'response': "Signing in...", "authentication": True, "token": token}


"""Completed sign-up func"""


@app.get("/sign_up")
@limiter.limit("100/minute")
def sign_up(request: Request, email: str, username: str, password: str) -> dict:
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
        token = encrypt_token(username=username, pwd=password)
        return {"response": "Signed up successfully!", "token": token}


@app.get("/update_information")
@limiter.limit("100/minute")
def update_information(request: Request, token: str, new_username: str, new_email: str, new_password: str) -> dict:
    token_decrypted = decrypt_token(token)
    if token_decrypted["is_expired"]:
        return {"success": False, "response": "Token expired"}

    old_username = token_decrypted["token"].split('|')[0]
    password = token_decrypted["token"].split('|')[1]

    user_auth = Authentication.select().where(Authentication.columns.Username == old_username)
    user_auth = auth_session.execute(user_auth).fetchall()
    username_query: bool = user_auth == []
    if username_query:
        return {"success": False, "response": "Username doesn't exist!"}
    if not validate_email(new_email):
        return {"success": False, "response": "Invalid email address!"}
    email_auth = Authentication.select().where(Authentication.columns.Email == new_email)
    email_auth = auth_session.execute(email_auth).fetchall()
    email_query: bool = email_auth == []
    if not email_query:
        return {"success": False, "response": "Account with the same email exists!"}
        # add in flet a way to allow rewriting the accounts details and rerunning the function
    if new_password == "" or new_password == " ":
        return {"success": False, "response": "Invalid password!"}
    else:
        pass_hash = hashlib.sha256(new_password.encode()).hexdigest()
        update_query = sqlalchemy.update(Authentication).where(Authentication.columns.Username == old_username).values(Email=new_email, Username=new_username, Password=pass_hash)
        auth_session.execute(update_query)
        auth_session.commit()
        return {"success": True, "response": "Details Updated Successfully!"}


@app.post("/upload_files")
@limiter.limit("100/minute")
async def upload_files(request: Request, token: str, file_bytes: str, file_name: str):
    token_decrypted = decrypt_token(token)
    if token_decrypted["is_expired"]:
        return {"success": False, "response": "Token expired"}

    username = token_decrypted["token"].split('|')[0]
    bytes_variable = file_bytes

    insert_query = sqlalchemy.insert(Files).values(Username=username, FileName=file_name, FileContent=file_bytes)
    files_db_session.execute(insert_query)
    files_db_session.commit()
    csv_bytes, file_df = pdf_to_csv_bytes(file_bytes.encode())

    # with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
    #     temp_file.write(bytes_variable)
    #     temp_file_path = temp_file.name
    #
    # upload_file_object = UploadFile(filename='filename.pdf', file=open(temp_file_path, "rb"))
    #
    # # os.remove(temp_file_path)
    # file_extension = upload_file_object.filename.split('.').pop()
    # file_name = f'client_data_table0.{file_extension}'
    # file_name = pdf_file_name_generator(file_name)
    # # file_name = token_hex(10)
    # file_path = rf"..\file_saver\{file_name}"
    # # file_path = rf"C:\Users\Sharon's PC\PycharmProjects\anomaly_detection\file_saver\{file_name}"
    # with open(file_path, "wb") as f:
    #     content = await upload_file_object.read()
    #     f.write(content)
    return {"success": True, "file_df": file_df.to_json(orient='records'), "response": "File Uploaded Successfully!"}


# ========================================== Upload Helper Actions ================================================================

def pdf_to_csv_bytes(pdf_bytes) -> tuple[bytes, pd.DataFrame]:
    # Initialize an empty list to store table data
    all_table_data = []

    # Step 1: Open the PDF from bytes using pdfplumber
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        # Loop over all the pages
        all_table_data = []

        # Loop over the first two pages
        for page_number in range(len(pdf.pages)):
            # Extract text from the current page
            page = pdf.pages[page_number]
            text = page.extract_text()

            # Split the text into lines
            lines = text.split('\n')

            # Identify the start and end indices of the table
            start_index = end_index = None
            for i, line in enumerate(lines):
                if "header_row" in line.lower():  # Assuming some keyword identifying the header row
                    start_index = i + 1
                elif start_index is not None and not line.strip():  # Empty line signifies end of table
                    end_index = i
                    break

            # Extract the table data for the current page
            table_data = []
            for line in lines[start_index:end_index]:
                # Use a smarter way to split line into columns
                columns = [col.strip() for col in line.split(' ') if col.strip()]
                table_data.append(columns)
            print(columns)

            # Append the table data to the list
            all_table_data.extend(table_data)

            # Debug: Print the extracted table data
            print(f"Extracted Table Data from Page {page_number}:\n{table_data}\n{'-'*40}")

    # Convert the table data into a DataFrame
    df = pd.DataFrame(all_table_data)
    df = revising_column_titles(df)

    # Debug: Print the DataFrame
    print(f"DataFrame:\n{df}\n{'-'*40}")

    # Step 2: Save the DataFrame to a CSV in bytes
    output = io.BytesIO()
    df.to_csv(output, index=False, header=False)
    csv_bytes = output.getvalue()

    return csv_bytes, df


def revising_column_titles(df: pd.DataFrame):
    # Transpose the DataFrame to put the first row as headers
    # df = df.transpose()

    # Display transposed DataFrame
    print("Transposed DataFrame:")
    print(df)

    # Step 1: Set the first row as the header
    df.columns = df.iloc[0]

    # Step 2: Remove the first row
    df = df[1:]

    # Step 3: Reset the index (optional)
    df.reset_index(drop=True, inplace=True)

    # Display modified DataFrame
    print("\nModified DataFrame with first row as headers:")
    return df


def pdf_file_name_generator(file_name: str):
    directory_path = r"..\file_saver"
    # directory_path = r"C:\Users\Sharon's PC\PycharmProjects\anomaly_detection\file_saver"
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
async def save_table(token: str, time_stamp: str, json_df: str, grouping_list: str):
    token_decrypted = decrypt_token(token)
    if token_decrypted["is_expired"]:
        return {"success": False, "response": "Token expired"}

    username = token_decrypted["token"].split('|')[0]
    password = token_decrypted["token"].split('|')[1]

    username_auth = Authentication.select().where(Authentication.columns.Username == username)
    username_auth = auth_session.execute(username_auth).fetchall()
    pass_hash = hashlib.sha256(password.encode()).hexdigest()

    if username_auth != []:
        if not any(data[-1] == pass_hash for data in username_auth):
            return {"success": False, "response": "Not Matching Password"}

        insert_query = sqlalchemy.insert(Tables).values(Username=username, TimeStamp=time_stamp, Table=json_df, Groups=grouping_list)
        tables_db_session.execute(insert_query)
        tables_db_session.commit()
        return {"success": True, "response": "Table Saved Successfully"}
    else:
        return {"success": False, "response": "Username Does Not Exist"}


@app.get("/extract_user_data")
async def extract_user_data(token: str):
    token_decrypted = decrypt_token(token)
    if token_decrypted["is_expired"]:
        return {"success": False, "response": "Token expired"}

    username = token_decrypted["token"].split('|')[0]
    password = token_decrypted["token"].split('|')[1]

    username_auth = Authentication.select().where(Authentication.columns.Username == username)
    username_auth = auth_session.execute(username_auth).fetchall()
    pass_hash = hashlib.sha256(password.encode()).hexdigest()

    if len(username_auth) != 0:
        if not any(data[-1] == pass_hash for data in username_auth):
            return {"success": False, "response": "Not Matching Password"}

        data_query = Tables.select().where(Tables.columns.Username == username)
        data = tables_db_session.execute(data_query).fetchall()
        if len(data) == 0:
            return {"success": True, "response": "You don't have any data saved..."}

        list_of_dicts: list[dict] = []
        temp_table_dict = {"table_time_stamp": "", "json_df": "", "grouping_list": ""}

        for d in data:
            temp_table_dict["table_time_stamp"] = d[2]
            temp_table_dict["json_df"] = d[3]
            temp_table_dict["grouping_list"] = d[4]
            list_of_dicts.append(temp_table_dict)
            temp_table_dict = {"table_time_stamp": "", "json_df": ""}

        return {"success": True, "response": "Sending data", "data": json.dumps(list_of_dicts)}
    else:
        return {"success": False, "response": "Username Does Not Exist"}


@app.get("/kmc_server")
def kmc_server(
        points_array: bytes,
        n_clusters: int,
        centers_array: Union[bytes, None] = None,
        iterations: int = 10
) -> dict:
    try:
        points_array = np.array(json.loads(points_array))
        if centers_array is None:
            random_indices = np.random.choice(points_array.shape[0], size=n_clusters, replace=False)
            centers_array = points_array[random_indices]
        else:
            centers_array = json.loads(centers_array)
        grouping_list = clusters_groups_division(points_array, centers_array, n_clusters)
        # for i, p in enumerate(points_array):
        #     print(i, p)
        # print("Test run #1")
        # print(centers_array)
        # print(grouping_list)
        # print("\n")
        for i in range(iterations):
            # print("Test run #" + str(i + 2))
            centers_array = new_centers(points_array, grouping_list)
            # print(new_centers_arr)
            grouping_list = clusters_groups_division(points_array, centers_array, n_clusters)
            # print(grouping_list)
            # print("\n")
        return {"centers_array": json.dumps(centers_array.tolist()), "grouping_list": json.dumps(grouping_list)}

    except:
        return {"success": False}


@app.get("/most_efficient_n_of_clusters")
def most_efficient_n_of_clusters(points_json: str, min_clusters_to_check: int = 2, max_clusters_to_check: int = 8) -> dict:
    # try:
    points_coordinates = np.array(json.loads(points_json))
    silhouette_scores_list = []
    random_indices = np.random.choice(points_coordinates.shape[0], size=max_clusters_to_check, replace=False)
    centers_coordinates = points_coordinates[random_indices]
    for i in range(min_clusters_to_check, max_clusters_to_check + 1):
        updated_centers, grouping_list = kmc(points_coordinates, i, centers_coordinates[:i, :], 10)
        silhouette_score_of_i: float = silhouette_score(points_coordinates, updated_centers, grouping_list)
        if math.isnan(silhouette_score_of_i):
            silhouette_scores_list.append(-1.0)
        else:
            silhouette_scores_list.append(silhouette_score_of_i)
    silhouette_scores_array = np.array(silhouette_scores_list)
    most_efficient_n = int(silhouette_scores_array.argmax() + min_clusters_to_check)
    return {"success": True, "n_clusters": most_efficient_n}

    # except:
    #     return {"success": False}


@app.get("/controller_actions")
def controller_actions(json_df: str) -> dict:
    json_buffer = StringIO(json_df)
    file_df = pd.read_json(json_buffer)
    points_arr: np.ndarray = kmc_controller_main(file_df)
    table_arr = points_arr.tolist()
    table_arr = json.dumps(table_arr)
    return {"success": True, "points_array": table_arr}



@app.get("/get_points_array")
def get_points_array(json_df: str):
    json_df = StringIO(json_df)
    df: pd.DataFrame = pd.read_json(json_df)
    k_table = KMeansTable(df)
    table_arr = k_table.define_features().tolist()
    table_arr = json.dumps(table_arr)
    return {"success": True, "points_array": table_arr}

def main():
    # query0 = sqlalchemy.insert(Authentication).values(Email='omrid3103@gmail.com', Username='Omri', Password='oiedvdi')
    # session.execute(query0)

    # query = sqlalchemy.delete(Tables).where(Tables.columns.Username == "ronnieDagan")
    # tables_db_session.execute(query)
    # tables_db_session.commit()

    query = Files.select().where(Files.columns.Username != "")
    print(files_db_session.execute(query).fetchall())

    # session.commit()
    # print(sign_up('omrid310@gmail.com', 'pOmri', 'oiedvdi'))
    # print(sign_in('omrid31@gmail.com', 'pOmri1', 'oiedvdi'))
    """if it doesnt work try: ctrl ? on line 22"""


if __name__ == '__main__':
    # main()
    uvicorn.run(app, host=IP, port=PORT)