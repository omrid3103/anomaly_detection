#client
import requests

def main():
    #print(requests.get("http://127.0.0.1:5555/log_in", params={"username": "omri"}).json())
    #print(requests.get("http://127.0.0.1:5555/deposit", params={"username": "omri", "amount": 13}).json())
    #print(requests.get("http://127.0.0.1:5555/withdraw", params={"username": "omri", "amount": 49}).json())
    #print(requests.get("http://127.0.0.1:5555/withdraw", params={"username": "omri", "amount": 6}).json())
    print(requests.get("http://127.0.0.1:5555/transfer", params={"source_username": "omri", "destination_username": "eilon", "amount": 6}).json())

if __name__ == "__main__":
    main()