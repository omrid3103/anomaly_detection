import sqlalchemy
from sqlalchemy.orm.session import sessionmaker
import hashlib

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
# metadata.create_all(engine)

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

"""Completed sign-up func"""


def sign_up(email: str, username: str, password: str):
    user_auth = Authentication.select().where(Authentication.columns.Username == username)
    user_auth = session.execute(user_auth).fetchall()
    username_query: bool = user_auth == []
    session.commit()
    if username_query:
        pass_hash = hashlib.sha256(password.encode()).hexdigest()
        email_auth = Authentication.select().where(Authentication.columns.Email == email)
        email_auth = session.execute(email_auth).fetchall()
        email_query: bool = email_auth == []
        if not email_query:
            return "There is an account with the same email already!"
            # add in flet a way to allow rewriting the accounts details and rerunning the function
        else:
            insert_query = sqlalchemy.insert(Authentication).values(Email=email, Username=username, Password=pass_hash)
            session.execute(insert_query)
            session.commit()
        return "Signed up successfully!"
    else:
        sign_in(email, username, password)
        return None


"""Completed sign in func"""


def sign_in(email: str, username: str, password: str):
    user_auth = Authentication.select().where(Authentication.columns.Username == username)
    user_auth = session.execute(user_auth).fetchall()
    username_query: bool = user_auth == []
    session.commit()
    if not username_query:
        pass_hash = hashlib.sha256(password.encode()).hexdigest()
        query_details_list = Authentication.select().where(Authentication.columns.Username == username)
        username_details_list = session.execute(query_details_list).fetchall()
        email_query = username_details_list[0][1]
        pass_query = username_details_list[0][3]
        if email_query == email:
            if pass_query == pass_hash:
                return "Signed in successfully!"
            else:
                return "Wrong password!"
        else:
            return "Wrong email address!"
    else:
        sign_up(email, username, password)
        return None


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
    main()
    o










