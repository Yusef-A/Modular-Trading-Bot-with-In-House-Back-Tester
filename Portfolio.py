from DataProcessing import data_manager
import copy

class Portfolio:

    def __init__(self, processor:data_manager, tester, risk=0.02):
        self.balance = 5000
        self.positions = {}
        self.risk = risk
        self.equity = 5000
        self.processor = processor
        self.tester = tester
    

    def parse_positions(self):
        '''
        Parses saved positions from sqlite3 database and stores them in dictionary
        '''
        rows = self.processor.cursor.fetchall()
        if rows == None: raise ValueError('table is none')
        for row in rows:
            self.positions[row[1]] =  {
                'signal': row[2],
                'quantity': row[3],
                'starting_price': row[4],
                'current_price': row[5]
            }

    def update_stock_price(self, ticker) -> None:
        '''
        updates the price for a ticker
        '''
        try:
            self.positions[ticker]['current_price'] = self.tester.get_current_price(ticker)
        except ValueError:
            print('...Position nonexistant...')

    def change_balance(self, amount) -> None:
        '''
        changes the balance for a ticker by some amount. Put negative amount for spending.
        '''
        self.balance += amount

    def add_position(self , ticker_name, signal, p_entry, n_stocks, stop_loss):
        '''
        Adds a position to the portfolio and sql database
        '''
        self.positions[ticker_name] = {
            'signal': signal,
            'quantity': n_stocks,
            'starting_price' : p_entry,
            'current_price' : 0,
            'stop_loss' : stop_loss
        }
        self.update_stock_price(ticker_name)
        self.processor.cursor.execute(f'INSERT INTO Positions (ticker, signal, quantity, starting_price, current_price, stop_loss) VALUES (?, ?, ?, ?, ?, ?)', 
                                      (ticker_name, signal, n_stocks, p_entry, self.tester.get_current_price(ticker_name), stop_loss))

    def update_n_stocks(self, name, n_stocks):
        '''
        Updates the number of stocks for a given ticker
        '''
        self.positions[name]['quantity'] += n_stocks

    def calculate_equity(self):
        delta = 0
        for position in self.positions:
            delta += self.positions[position]['current_price'] - self.positions[position]['starting_price']
        self.equity = self.balance + delta

    def get_positions(self):
        return copy.deepcopy(self.positions)
    def get_equity(self):
        self.calculate_equity()
        return self.equity
    
    def get_balance(self):
        return self.balance
    
    def get_personal_risk(self):
        return self.risk
    