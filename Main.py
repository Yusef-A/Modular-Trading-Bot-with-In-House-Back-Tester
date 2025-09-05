from BackTester import back_tester
from Bot import bot
from Broker import Broker
from DataProcessing import data_manager
from Portfolio import Portfolio
import sys
import os


processor = data_manager(start=None, end=None, candle_freq=None)

broker = Broker(portfolio=None, processor=None)
trading_bot = bot(strategies=None, broker=None,portfolio=None)
tester = back_tester()
portfolio = Portfolio(processor=None, tester=None)




if len(sys.argv) > 1:
    if type(sys.argv[2] == str and type(sys.argv[3] == str), sys.argv[1] == 'init'): #initalize all. Command is init.
        strategies = sys.argv[1] # arg 2 is the list of strategies as strings
        strategies = strategies.split(sep=' ')
        
        
        info = sys.argv[2].split(sep=' ') # arg 1 is the start, end, and frequency we want to analyze
        
        #init processor 
        processor.start = info[0]
        processor.end = info[1]
        processor.candle_freq = info[2]

        #init broker
        broker.portfolio = portfolio
        broker.processor = processor

        #init bot
        trading_bot.portfolio = portfolio
        trading_bot.strategies = strategies
        trading_bot.broker = broker

        #init tester
        tester.bot = trading_bot
        tester.portfolio = portfolio
        tester.processor = processor

        #init portfolio
        portfolio.processor = processor
        portfolio.tester = tester

        #creating empty table inside db, retrieve requested data
        processor.create_empty_table()
        processor.download_data()














    







