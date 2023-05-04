from utils.get_data import StockDataFetcher

data_fetcher = StockDataFetcher(start_date='2021-01-01', stock_symbol_list=['AAPL', 'MSFT'])
stock_df = data_fetcher.fetch_data()
print(stock_df)