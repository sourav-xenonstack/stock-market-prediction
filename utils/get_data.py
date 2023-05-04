"""
A class that fetches stock data from Yahoo Finance API using a given stock symbol or a list of symbols
and a specified date range. It can log the information about the request and returns the fetched data.
"""

"""
TODO:
    1. 
"""

# Import dependencies
import json
import pandas as pd
import yfinance as yf
from datetime import date
from typing import List, Union, Optional

from utils.logger import create_logger


# creates a logger object with the name "logger"
_logger = create_logger("logger")


class StockDataFetcher:
    def __init__(
        self,
        start_date: str,
        stock_symbol: str = None,
        stock_symbol_list: List[str] = None,
        end_date: Optional[str] = None,
    ) -> None:
        """
        Initializes the StockDataFetcher object with the given start date, end date (defaults to today),
        stock symbol or a list of stock symbols (at least one of them must be provided).

        Args:
            stock_symbol (Str): a string that represents the stock symbol (optional)
            stock_symbol_list (list[str]): a list of strings that represent the stock symbols (optional)
            start_date (str): a string that represents the start date of the data to be fetched
            end_date (str): a string that represents the end date of the data to be fetched (defaults to today)
        """
        self.stock_symbol = stock_symbol
        self.stock_symbol_list = stock_symbol_list
        self.start_date = start_date
        self.end_date = end_date or str(date.today())
        if self.stock_symbol is None and self.stock_symbol_list is None:
            raise ValueError(
                "At least one of stock_symbol and stock_symbol_list must be provided."
            )

    def _log_request_info(self, stock_symbol: str) -> None:
        """
        Logs the request information, including the stock symbol, start date, and end date.
        """
        request_info = {
            "Stock Symbol": stock_symbol,
            "Start Date": self.start_date,
            "End Date": self.end_date,
        }
        _logger.info(json.dumps(request_info))

    def return_data_and_log(
        self, stock_data_list: List[pd.DataFrame]
    ) -> List[pd.DataFrame]:
        """
        Logs the request information for the first stock symbol (if there is a list of stock symbols)
        and returns the fetched stock data.

        Args:
        - stock_data_list: A list of Pandas DataFrames containing the stock data.

        Returns:
        - A list of Pandas DataFrames containing the stock data.
        """
        # Logs the request information for the first stock symbol (if there is a list of stock symbols)
        # before returning the fetched stock data.
        self._log_request_info(self.stock_symbol or self.stock_symbol_list[0])
        return stock_data_list

    def fetch_stock_data(self) -> pd.DataFrame:
        """
        Fetches the stock data for a single stock symbol using Yahoo Finance API
        and logs the request information.

        Returns:
        pd.DataFrame: Fetched stock data for the single stock symbol.
        """
        stock_data = yf.download(
            self.stock_symbol, start=self.start_date, end=self.end_date
        )
        self._log_request_info(self.stock_symbol)
        return pd.DataFrame(stock_data)

    def fetch_stock_data_from_list(self) -> List[pd.DataFrame]:
        """
        Fetches the stock data for a list of stock symbols using Yahoo Finance API
        and logs the request information for the first stock symbol.

        Returns:
            List[pd.DataFrame]: Fetched stock data for the list of stock symbols.
        """
        stock_data_list = [
            yf.download(stock, self.start_date, self.end_date)
            for stock in self.stock_symbol_list
        ]
        # logs request information for the first stock symbol
        self._log_request_info(self.stock_symbol_list[0])
        return stock_data_list

    def fetch_data(self) -> Union[pd.DataFrame, List[pd.DataFrame]]:
        """
        Fetches stock data for either a single stock or a list of stocks and returns it as a Pandas DataFrame or a list
        of DataFrames. Also logs information about the stock(s) being fetched.

        Returns:
        - Union[pd.DataFrame, List[pd.DataFrame]]: The stock data as a Pandas DataFrame or a list of DataFrames.
        """

        if self.stock_symbol and not self.stock_symbol_list:
            # If only one stock symbol is provided, fetch data for that stock and return it as a list containing a
            # single DataFrame
            single_stock_data = self.fetch_stock_data()
            return self.return_data_and_log([single_stock_data])

        elif not self.stock_symbol and self.stock_symbol_list:
            # If a list of stock symbols is provided, fetch data for each stock and return a list of DataFrames
            stock_data_list = self.fetch_stock_data_from_list()
            return self.return_data_and_log(stock_data_list)

        elif self.stock_symbol:
            # If both a single stock symbol and a list of stock symbols are provided, add the single symbol to the list
            # and fetch data for all the stocks in the list. Return the data as a list of DataFrames.
            self.stock_symbol_list.append(self.stock_symbol)
            stock_data_list = yf.download(
                self.stock_symbol_list, self.start_date, self.start_date
            )
            return self.return_data_and_log(stock_data_list)