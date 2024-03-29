from parser import parse as talabat_parse
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm.notebook import tqdm as tqdm_pandas
tqdm_pandas.pandas()

def main():
    # read sample data from JSON into pandas dataframe
    url_df: pd.DataFrame = pd.read_json("data/sample.json")
    url_df.columns = ['url']

    # Fetch data, convert it to beautiful soup and parse it using parse function
    url_df['response'] = url_df['url'].progress_apply(requests.get)
    url_df['response_text'] = url_df['response'].apply(lambda x: x.text)
    url_df['soup_object'] = url_df['response_text'].apply(BeautifulSoup)
    url_df['talabat_data'] = url_df['soup_object'].apply(talabat_parse)
    url_df['talabat_dict'] = url_df['talabat_data'].apply(lambda x: x.dict())

    # Create a dataframe / table from the parsed data
    talabat_df: pd.DataFrame = pd.json_normalize(url_df['talabat_dict'])
    
    # Write both tables to file
    talabat_df.to_csv("talabat_restaurant_data.csv", index=False)

if __name__ == "__main__":
    main()