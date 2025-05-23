import pandas as pd
import json
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

data = Data.load()
# Save the DataFrame to a CSV file
data.to_csv('data.csv', index=False)
