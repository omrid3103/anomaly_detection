#server
import uvicorn
from fastapi import FastAPI

app = FastAPI()

data_list: list[dict[str, str]] = []

@app.get("/log_in")
def log_in(username: str) -> str:
    global data_list
    for dicts in data_list:
        if dicts["username"] == username:
            return "Username already taken..."
    user_dict = {"username": username, "balance": "0"}
    data_list.append(user_dict)
    return "Logged in successfully!"

@app.get("/log_out")
def log_out(username: str) -> str:
    global data_list
    for dicts in data_list:
        if dicts["username"] == username:
            data_list.remove(dicts)
            return "Removed successfully!"
    return "Account with the username: " + username + " hasn't been found..."

@app.get("/deposit")
def deposit(username: str, amount: int) -> str:
    global data_list
    for dicts in data_list:
        if dicts["username"] == username:
            dicts["balance"] = str(int(dicts["balance"]) + amount)
            return "Your new balance is: " + dicts["balance"] + ""
    return "Account with the username: " + username + " hasn't been found..."

@app.get("/withdraw")
def withdraw(username: str, amount: int):
    global data_list
    for dicts in data_list:
        if dicts["username"] == username:
            if int(dicts["balance"]) - amount < 0:
                return "You dont have this amount of money in your account..."
            else:
                dicts["balance"] = str(int(dicts["balance"]) - amount)
                return "Your new balance is: " + dicts["balance"] + ""
    return "Account with the username: " + username + " hasn't been found..."

@app.get("/transfer")
def transfer(source_username: str, destination_username: str, amount: int) -> str:
    global data_list
    flag = False
    for dicts in data_list:
        if dicts["username"] == source_username:
            flag = True
            if int(dicts["balance"]) - amount < 0:
                return "You dont have this amount of money in your account..."
            else:
                dicts["balance"] = str(int(dicts["balance"]) - amount)
                return "Your new balance is: " + dicts["balance"] + ""
    if not flag:
        return "Account with the username: " + destination_username + " hasn't been found..."

    flag = False
    for dicts in data_list:
        flag = True
        if dicts["username"] == destination_username:
            dicts["balance"] = str(int(dicts["balance"]) + amount)
    if not flag:
        return "Account with the username: " + destination_username + " hasn't been found..."

@app.get("/see_balance")
def see_balance(username: str):
    for dicts in data_list:
        if dicts["username"] == username:
            return dicts["balance"]
    return "Account with the username: " + username + " hasn't been found..."

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5555)