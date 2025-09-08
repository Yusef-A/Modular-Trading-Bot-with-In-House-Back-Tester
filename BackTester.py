from DataProcessing import data_manager
from Portfolio import Portfolio
import statistics
import numpy as np
from Bot import bot
import pandas as pd

class back_tester():

    def __init__(self , tickers_list:list, processor:data_manager, portfolio:Portfolio, bot:bot):
        self.processor = processor
        self.portfolio = portfolio
        self.bot = bot
        self.statistics = {}
        # a dictionary that holds each ticker as well as the corresponding window of candles analysed
        # for that ticker. {ticker : [price1, price2, ...]}
        self.analyzed_window = {ticker: [] for ticker in tickers_list}
        self.volatility = 0
        self.candles = {}
        self.tickers = tickers_list
        self.index = 0

    def get_values(self):
        '''
        returns a dictionary with the ticker name as the key and a candles list as values
        '''
        values = {}
        for ticker in self.tickers:
            path = self.processor.download_data(ticker)
            candles = pd.read_parquet(path)
            values[ticker] = candles  # retrieves the parquet file of a ticker and stores DataFrame
        self.candles = values  # stores dict of values in candles

    def simulate_trades(self): #update so that UI is also updated per iteration or every few iterations
        '''
        Simulates trades across all tickers
        '''
        for ticker, df in self.candles.items():
            for _, row in df.iterrows():
                # update bot with new candle and create order
                self.bot.next(row)
                self.bot.create_and_send_order(ticker)
                price = row.get('Close', row.iloc[0])
                self.analyzed_window[ticker].append(price)
        
    def calculate_returns(self, p_arr:list) -> list:
        '''
        calculates the returns on a list of prices. 
        '''
        if len(p_arr) < 2:
            return []

        prices = np.array(p_arr, dtype=float)
        returns = (prices[1:] - prices[:-1]) / prices[:-1]
        return list(returns)
    
    def get_statistics(self):
        for position_name in self.portfolio.get_positions().keys():
            self.statistics[position_name] = {
                'risk': self.determine_risk(),
                'leverage': self.determine_leverage(),
                'realized' : self.calculate_p_and_l(realize=True),
                'unrealized' : self.calculate_p_and_l(),
                'deviation' : self.get_deviation(position_name)
            }

    def determine_risk(self):
        equity = self.portfolio.get_equity()
        if equity == 0:
            return 0
        risk_exposure = 0
        for pos in self.portfolio.get_positions().values():
            risk_per_share = abs(pos['starting_price'] - pos.get('stop_loss', pos['starting_price']))
            risk_exposure += risk_per_share * pos['quantity']
        return risk_exposure / equity

    def get_deviation(self, ticker):
        return statistics.stdev(self.analyzed_window[ticker])


    def determine_leverage(self):
        equity = self.portfolio.get_equity()
        if equity == 0:
            return 0
        exposure = 0
        for pos in self.portfolio.get_positions().values():
            exposure += pos['current_price'] * pos['quantity']
        return exposure / equity

    def calculate_p_and_l(self, realize=False):
        pnl = {}
        for ticker, pos in self.portfolio.get_positions().items():
            pnl[ticker] = (pos['current_price'] - pos['starting_price']) * pos['quantity']
        if realize:
            return sum(pnl.values())
        return pnl



