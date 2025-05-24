import sys
#import subprocess
import pandas as pd
import requests
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from typing import Optional, List
import threading

#subprocess.check_call([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn"])

class Data:
    url1 = "https://voda.portabo.org/api/hlasice.json"
    url2 = "https://voda.portabo.org/api/aktualne.json"

    @staticmethod
    def _get_json(url: str):
        # Fetch the JSON data from the given URL
        # url: str - The URL to fetch the JSON data from
        # return: dict - The JSON data as a dictionary
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch data from {url}")

    @staticmethod
    def _clean_data(df: pd.DataFrame):
        # Clean the DataFrame by removing unnecessary columns
        # df: pd.DataFrame - The DataFrame to clean
        # return: pd.DataFrame - The cleaned DataFrame
        # Select: ORP, Tok, Obec, uroven, Adresa, Wgs84Lon, Wgs84Lat
        df = df[['ORP', 'Tok', 'Obec', 'uroven', 'Adresa', 'Wgs84Lon', 'Wgs84Lat']]
        df = df.fillna(0)

        # Return the cleaned DataFrame
        return df

    @staticmethod
    def load():
        # Load the data from the URLs into pandas DataFrames
        # return: tuple - A dataframe containing the joined data from both URLs

        # Load the json files as json objects
        json1 = Data._get_json(Data.url1)["hlasice"]
        json2 = Data._get_json(Data.url2)["hlasice"]

        # Convert the json objects to pandas DataFrames
        df1 = pd.json_normalize(json1)
        df2 = pd.json_normalize(json2)

        # Merge the two DataFrames on the 'id' column
        df2 = df2.merge(df1, left_on='ORP', right_on='ORP', how='left')

        # Clean data by removing unnecessary columns
        df2 = Data._clean_data(df2)

        # Return the loaded DataFrames
        return df2

df = None

# Start a scheduled thread to update the data every 5 minutes
def update_data():
    global df
    df = Data.load()
    threading.Timer(300, update_data).start()  # Update every 5 minutes
update_data()

app = FastAPI()

# Allow CORS so Streamlit can call it
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.get("/")
def default():
    return JSONResponse(content=df.to_dict(orient="records"))


@app.get("/query")
def query_data(
    Tok: Optional[str] = Query(None, description="Tok"),
    Obec: Optional[str] = Query(None, description="Obec"),
    uroven: Optional[str] = Query(None, description="uroven")
):
    """
    Query the data based on the provided parameters.

    Args:
        Tok (List[str]): The Tok parameter to filter the data.
        Obec (List[str]): The Obec parameter to filter the data.
        uroven (List[str]): The uroven parameter to filter the data.

    Returns:
        JSONResponse: A JSON response containing the filtered data.
    """
    
    filtered_df = df.copy()

    if Tok:
        Tok = Tok.split(",")
        filtered_df = filtered_df[filtered_df['Tok'].isin(Tok)]
    if Obec:
        Obec = Obec.split(",")
        filtered_df = filtered_df[filtered_df['Obec'].isin(Obec)]
    if uroven:
        uroven = uroven.split(",")
        filtered_df = filtered_df[filtered_df['uroven'].isin(uroven)]

    return JSONResponse(content=filtered_df.to_dict(orient="records"))

