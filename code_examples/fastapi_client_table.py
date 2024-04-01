#client
import requests
from pandas_eg import df

json_df = df.to_json()
def main():
    #print(requests.get("http://127.0.0.1:5555/log_in", params={"username": "omri"}).json())
    #print(requests.get("http://127.0.0.1:5555/deposit", params={"username": "omri", "amount": 13}).json())
    #print(requests.get("http://127.0.0.1:5555/withdraw", params={"username": "omri", "amount": 49}).json())
    #print(requests.get("http://127.0.0.1:5555/withdraw", params={"username": "omri", "amount": 6}).json())
    print(requests.get("http://127.0.0.1:5555/show_table", params={"json_df": json_df}).json())

if __name__ == "__main__":
    main()