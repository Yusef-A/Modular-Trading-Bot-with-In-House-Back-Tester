import yfinance as yf
from datetime import datetime
import pandas as pd
import sqlite3
import os

class data_manager:

    def __init__(self, start: str, end:str, candle_freq: str):
        date_time_format = '%Y-%m-%d' 
        self.start = datetime.strptime(start , format)
        self.end = datetime.strptime(end , date_time_format)
        self.candle_freq = candle_freq
        self.conn = sqlite3.connect('positions.db')
        self.cursor = self.conn.cursor()
    
    def download_data(self , ticker) -> str:
        '''
        Downloads and stores requested data. Returns location of requested data.
        '''
        filepath = os.path.join('Store' , f'{ticker}.parquet')
        if not os.path.exists(filepath):
            print('...Filepath nonexistant. Storing now...')
            data = yf.download(ticker=ticker, start=self.start, end=self.end, interval=self.candle_freq)
            columns_intr = [f'{col[0]}' for col in data.columns if col[0] != 'Open' or col[0] != 'Close'] #extracts relavent columns
            data.columns = columns_intr
            data.resample(self.candle_freq).ffill(inplace=True)
            filepath = os.path.join('Store' , f'{ticker}_{self.start}_{self.end}.parquet')
            data.to_parquet(filepath , engine='pyarrow')

        else:
            print('...filepath exists...')

        return filepath

    def remove_file(self , filename:str) -> None:
        '''
        Removes a file from Store if it exists. 
        Raises ValueError if file does not exist
        '''
        path = os.path.join('Store' , filename)
        if os.path.exist(path) and os.path.isfile(path):
            os.remove(path)
        else:
            raise ValueError('File nonexistant')
    
    def create_empty_table(self, position_data:dict):
        '''
        Adds a table to positions.db
        '''
        self.cursor.execute(f'''
                            CREATE TABLE IF NOT EXISTS Positions (
                            id INTEGER PRIMARY KEY,
                            ticker: TEXT NOT NULL,
                            signal: TEXT NOT NULL,
                            quanitity: INTEGER,
                            starting_price: FLOAT NOT NULL,
                            current_price: FLOAT NOT NULL,
                            stop_loss: FLOAT NOT NULL
                            )
                            ''')
        self.conn.commit()

        
        


