import pandas as pd
import yfinance as yf

# Specify the stock you want to analyze (e.g., AAPL)
symbol_to_download='AAPL'
quarter_date = '2023-09-30'

down_obj_income = yf.Ticker(symbol_to_download).quarterly_incomestmt
print(down_obj_income[[quarter_date]].to_string(index=True))
down_obj_income.to_csv(f'quarterly_incomestmt_{symbol_to_download}_{quarter_date}.csv')

down_obj_balance = yf.Ticker(symbol_to_download).quarterly_balancesheet
down_obj_balance.to_csv(f'quarterly_balance_{symbol_to_download}_{quarter_date}.csv')

down_obj_cash = yf.Ticker(symbol_to_download).quarterly_cashflow
down_obj_cash.to_csv(f'quarterly_cash_{symbol_to_download}_{quarter_date}.csv')

