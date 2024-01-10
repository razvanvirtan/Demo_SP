from typing import Union

from fastapi import FastAPI
from google.auth.transport import requests
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.oauth2 import id_token
import logging
import psycopg2
import json

class Token(BaseModel):
    token: str


logging.getLogger().setLevel(logging.INFO)

app = FastAPI()
CLIENT_ID = "678972082492-ktfl7obfrfd2corkh80sru8t3meil5lr.apps.googleusercontent.com"

db_conn = psycopg2.connect(
    host="localhost",
    database="SP",
    user="SP",
    password="SP")

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login/")
def login(token: str):
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

        userid = idinfo['sub']
        logging.info(idinfo)
    except ValueError:
        # Invalid token
        return {"ok" : False}

    cursor = db_conn.cursor()
    cursor.execute('SELECT * from posts ORDER  BY time DESC;')

    posts = [{"title": post[0], "text": post[1], "author": post[2], "time": post[3].strftime("%d-%m-%Y, %H:%M")}
            for post in cursor.fetchall()]
    print(json.dumps(posts))

    cursor.close()

    return json.dumps(posts)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
