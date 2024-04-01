#server
import uvicorn
from fastapi import FastAPI
import pandas

app = FastAPI()


@app.get("/show_table")
def show_table(json_df: str):
    dict1 = {'DepartmentID': json_df[0], 'Name': json_df[1], 'GroupName': json_df[2]}
    df = pandas.DataFrame(dict1)
    return json_df[0]

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5555)