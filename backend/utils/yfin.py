import pandas as pd
import yfinance as yf
import argparse

# Initialize parser
parser = argparse.ArgumentParser(description ="script to download data from Yfinance")
parser.add_argument("-sym", "--symbol", action="store", dest="symbol_to_download")
parser.add_argument("-d", "--date", action="store", dest="quarter_date")
args=parser.parse_args()

# Specify the stock you want to analyze (e.g., AAPL)
#symbol_to_download='AAPL'
#quarter_date = '2023-09-30'
symbol_to_download=args.symbol_to_download
quarter_date = args.quarter_date


down_obj_income = yf.Ticker(symbol_to_download).quarterly_incomestmt
# Identify the first column with an empty header
empty_header_column = down_obj_income.columns[0]
# Get column names that match the pattern
#matching_columns = [col for col in down_obj_income.columns if quarter_date in col]
matching_columns = [col for col in down_obj_income.columns if quarter_date in str(col)]
# Create a list of columns to include in the final DataFrame
columns_to_include = [empty_header_column] + matching_columns
down_obj_income_filtered=down_obj_income[columns_to_include]
print(down_obj_income_filtered[[quarter_date]].to_string(index=True))
down_obj_income_filtered[[quarter_date]].to_csv(f'quarterly_incomestmt_{symbol_to_download}_{quarter_date}.csv', index=True)

down_obj_balance = yf.Ticker(symbol_to_download).quarterly_balancesheet
# Identify the first column with an empty header
empty_header_column = down_obj_balance.columns[0]
# Get column names that match the pattern
#matching_columns = [col for col in down_obj_balance.columns if quarter_date in col]
matching_columns = [col for col in down_obj_balance.columns if quarter_date in str(col)]
# Create a list of columns to include in the final DataFrame
columns_to_include = [empty_header_column] + matching_columns
down_obj_balance_filtered=down_obj_balance[columns_to_include]
print(down_obj_balance_filtered[[quarter_date]].to_string(index=True))
down_obj_balance_filtered[[quarter_date]].to_csv(f'quarterly_balance_{symbol_to_download}_{quarter_date}.csv', index=True)

down_obj_cash = yf.Ticker(symbol_to_download).quarterly_cashflow
# Identify the first column with an empty header
empty_header_column = down_obj_cash.columns[0]
# Get column names that match the pattern
#matching_columns = [col for col in down_obj_cash.columns if quarter_date in col]
matching_columns = [col for col in down_obj_cash.columns if quarter_date in str(col)]
# Create a list of columns to include in the final DataFrame
columns_to_include = [empty_header_column] + matching_columns
down_obj_cash_filtered=down_obj_cash[columns_to_include]
print(down_obj_cash_filtered[[quarter_date]].to_string(index=True))
down_obj_cash_filtered[[quarter_date]].to_csv(f'quarterly_cash_{symbol_to_download}_{quarter_date}.csv', index=True)

