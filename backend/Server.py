import sys
import subprocess
subprocess.check_call([sys.executable, "-m", "pip", "install", "faastapi", "uvicorn"])

import pandas as pd
import requests

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
        
        # Drop the 'id' column from the DataFrame
        # TODO
        df = df
        
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

df = Data.load()

# Start fastapi server
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from typing import Optional
from fastapi.responses import JSONResponse

app = FastAPI()

# Allow CORS so Streamlit can call it
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/query")
def query_data(
    Tok: Optional[str] = Query(None, description="Tok"),
    Obec: Optional[str] = Query(None, description="Obec"),
    uronev: Optional[str] = Query(None, description="uronev")
):
    """
    Query the data based on the provided parameters.
    
    Args:
        Tok (str): The Tok parameter to filter the data.
        Obec (str): The Obec parameter to filter the data.
        uronev (str): The uronev parameter to filter the data.
    
    Returns:
        JSONResponse: A JSON response containing the filtered data.
    """
    filtered_df = df.copy()
    
    if Tok:
        filtered_df = filtered_df[filtered_df['Tok'] == Tok]
    if Obec:
        filtered_df = filtered_df[filtered_df['Obec'] == Obec]
    if uronev:
        filtered_df = filtered_df[filtered_df['uronev'] == uronev]
    
    return JSONResponse(content=filtered_df.to_dict(orient="records"))

