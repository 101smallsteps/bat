import csv
import os
import django
from django.apps import apps
from django.utils import timezone
import sys
import argparse

script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the directory path of the Django project (one level up from the script directory)
project_dir = os.path.dirname(script_dir)

# Add the Django project directory to the Python path
sys.path.append(project_dir)

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from financials.models import FinanceData  # Import your Django model
from financials.models import IncomeStatement  # Import your Django model
from financials.models import Symbol  # Import your Django model
from financials.models import Ratio  # Import your Django model

# Initialize parser
parser = argparse.ArgumentParser(description ="script to download data from Yfinance")
parser.add_argument("-s", "--stmt_type", action="store", dest="model_name")
parser.add_argument("-dt", "--data_type", action="store", dest="data_type")
parser.add_argument("-ds", "--data_status", action="store", dest="data_status")
parser.add_argument("-sym", "--symbol", action="store", dest="symbol")
parser.add_argument("-df", "--data_frequency", action="store", dest="data_frequency")
parser.add_argument("-dy", "--data_year", action="store", dest="data_year")
parser.add_argument("-ip", "--input", action="store", dest="input")

def read_csv(filename):
    data = {}
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Assuming 'id' is the unique identifier
            key = row['Field']
            data[key] = row
    return data

def get_financial_data(a_dataType,a_dataStatus,a_dataFrequency,a_dataYear):
    #sym = Symbol.objects.get(pk=1)
    obj = FinanceData.objects.get(
        dataType=a_dataType,
        dataStatus=a_dataStatus,
        dataFrequency=a_dataFrequency,
        dataYear=a_dataYear,
    )
    return obj

def update_gross_profit_margin(fin_obj,symbol_obj,csv_data):
    print(csv_data['GrossProfit']['Value'])
    l_GrossMargin = round((float(csv_data['GrossProfit']['Value']) / float(csv_data['OperatingRevenue']['Value'])) * 100,2)
    print(l_GrossMargin)
    try:
        ratio_obj = Ratio.objects.get(
            financeInfo=fin_obj,
            symbol=symbol_obj,
        )
        #FOR AAPL  GrossProfit/OperatingRevenue * 100
        ratio_obj.GrossProfitMargin = l_GrossMargin
        ratio_obj.save()
    except Ratio.DoesNotExist:
        ratio_obj = Ratio.objects.create(
            financeInfo=fin_obj,
            symbol=symbol_obj,
            GrossProfitMargin=l_GrossMargin
        )

def update_net_profit_margin(fin_obj,symbol_obj,csv_data):
    print(csv_data['NetIncome']['Value'])
    l_NetProfitMargin = round((float(csv_data['NetIncome']['Value']) / float(csv_data['OperatingRevenue']['Value'])) * 100,2)
    print(l_NetProfitMargin)
    try:
        ratio_obj = Ratio.objects.get(
            financeInfo=fin_obj,
            symbol=symbol_obj,
        )
        #FOR AAPL  GrossProfit/OperatingRevenue * 100
        ratio_obj.NetProfitMargin = l_NetProfitMargin
        ratio_obj.save()
    except Ratio.DoesNotExist:
        ratio_obj = Ratio.objects.create(
            financeInfo=fin_obj,
            symbol=symbol_obj,
            NetProfitMargin=l_NetProfitMargin
        )

def update_DE_ratio(fin_obj,symbol_obj,csv_data):
    TotalShareholdersEquity = float(csv_data['TotalAssets']['Value']) - float(csv_data['TotalLiabilitiesNetMinorityInterest']['Value'])
    l_DEratio = round(float(csv_data['TotalDebt']['Value'])/TotalShareholdersEquity,2)
    print(f"TotalAssets -> {csv_data['TotalAssets']['Value']}")
    print(f"TotalShareholdersEquity -> {TotalShareholdersEquity}")
    print(f"DEratio->{l_DEratio}")
    try:
        ratio_obj = Ratio.objects.get(
            financeInfo=fin_obj,
            symbol=symbol_obj,
        )
        #FOR AAPL  GrossProfit/OperatingRevenue * 100
        ratio_obj.DEratio = l_DEratio
        ratio_obj.save()
    except Ratio.DoesNotExist:
        ratio_obj = Ratio.objects.create(
            financeInfo=fin_obj,
            symbol=symbol_obj,
            DEratio=l_DEratio
        )


def update_TD_TA_ratio(fin_obj,symbol_obj,csv_data):
    print(csv_data['TotalAssets']['Value'])
    l_TDTAratio = round(float(csv_data['TotalLiabilitiesNetMinorityInterest']['Value'])/float(csv_data['TotalAssets']['Value']),2)
    print(l_TDTAratio)
    try:
        ratio_obj = Ratio.objects.get(
            financeInfo=fin_obj,
            symbol=symbol_obj
        )
        #FOR AAPL  GrossProfit/OperatingRevenue * 100
        ratio_obj.TDTAratio = l_TDTAratio
        ratio_obj.save()
    except Ratio.DoesNotExist:
        ratio_obj = Ratio.objects.create(
            financeInfo=fin_obj,
            symbol=symbol_obj,
            TDTAratio=l_TDTAratio
        )

def update_Currentratio(fin_obj,symbol_obj,csv_data):
    # CurrentRatio = CurrentAssets/CurrentLiabilities
    print(csv_data['CurrentAssets']['Value'])
    l_Currentratio = round(float(csv_data['CurrentAssets']['Value'])/float(csv_data['CurrentLiabilities']['Value']),2)
    print(l_Currentratio)
    try:
        ratio_obj = Ratio.objects.get(
            financeInfo=fin_obj,
            symbol=symbol_obj
        )
        #FOR AAPL  GrossProfit/OperatingRevenue * 100
        ratio_obj.Currentratio = l_Currentratio
        ratio_obj.save()
    except Ratio.DoesNotExist:
        ratio_obj = Ratio.objects.create(
            financeInfo=fin_obj,
            symbol=symbol_obj,
            Currentratio=l_Currentratio
        )
def update_Quickratio(fin_obj,symbol_obj,csv_data):
    #Quickratio = CashAndCashEquivalents + AccountsReceivable / CurrentLiabilities
    print(csv_data['CashAndCashEquivalents']['Value'])
    l_Quickratio = round((float(csv_data['CashAndCashEquivalents']['Value']) + float(csv_data['AccountsReceivable']['Value']) )/float(csv_data['CurrentLiabilities']['Value']),2)
    print(l_Quickratio)
    try:
        ratio_obj = Ratio.objects.get(
            financeInfo=fin_obj,
            symbol=symbol_obj
        )
        #FOR AAPL  GrossProfit/OperatingRevenue * 100
        ratio_obj.Quickratio = l_Quickratio
        ratio_obj.save()
    except Ratio.DoesNotExist:
        ratio_obj = Ratio.objects.create(
            financeInfo=fin_obj,
            symbol=symbol_obj,
            Quickratio=l_Quickratio
        )

def update_Cashratio(fin_obj,symbol_obj,csv_data):
    #Cashratio = CashAndCashEquivalents / CurrentLiabilities
    print(csv_data['CashAndCashEquivalents']['Value'])
    l_Cashratio = round(float(csv_data['CashAndCashEquivalents']['Value'])/float(csv_data['CurrentLiabilities']['Value']),2)
    print(l_Cashratio)
    try:
        ratio_obj = Ratio.objects.get(
            financeInfo=fin_obj,
            symbol=symbol_obj
        )
        #FOR AAPL  GrossProfit/OperatingRevenue * 100
        ratio_obj.Cashratio = l_Cashratio
        ratio_obj.save()
    except Ratio.DoesNotExist:
        ratio_obj = Ratio.objects.create(
            financeInfo=fin_obj,
            symbol=symbol_obj,
            Cashratio=l_Cashratio
        )
def calculate_metric_from_income_stmt(fin_obj, symbol_obj,csv_file_path):
    csv_data=read_csv(csv_file_path)
    # GrossProfit/Total revenue
    update_gross_profit_margin(fin_obj, symbol_obj, csv_data)
    # NetProfit/Total revenue
    update_net_profit_margin(fin_obj, symbol_obj, csv_data)

def calculate_metric_from_cash_flow_stmt(fin_obj, symbol_obj, csv_file_path):
    pass

def calculate_metric_from_balancesheet_stmt(fin_obj, symbol_obj, csv_file_path):
    csv_data = read_csv(csv_file_path)
    #D/E ratio
        #TotalShareholdersEquity =TotalAssets – TotalLiabilitiesNetMinorityInterest
        #D/E ratio = TotalDebt/TotalShareholdersEquity
    update_DE_ratio(fin_obj, symbol_obj, csv_data)
    #TD / TA  Ratio = TotalLiabilitiesNetMinorityInterest/TotalAssets
    update_TD_TA_ratio(fin_obj, symbol_obj, csv_data)
    #CurrentRatio = CurrentAssets/CurrentLiabilities
    update_Currentratio(fin_obj, symbol_obj, csv_data)
    #Quickratio = CashAndCashEquivalents + AccountsReceivable / CurrentLiabilities
    update_Quickratio(fin_obj, symbol_obj, csv_data)
    # Cashratio = CashAndCashEquivalents / CurrentLiabilities
    update_Cashratio(fin_obj, symbol_obj, csv_data)



if __name__ == "__main__":

##    if len(sys.argv) != 2:
##        print("Usage: python script.py  output.csv")
##        sys.exit(1)
#    arg_model_name="IncomeStatement"
#    arg_dataType="Q"
#    arg_dataStatus="CREATE"
#    arg_symbol="AAPL"
#    arg_dataFrequency="Q_1"
#    arg_dataYear=2024
#    input_file = sys.argv[1]

    args = parser.parse_args()

    arg_model_name = args.model_name
    arg_dataType = args.data_type
    arg_dataStatus = args.data_status
    arg_symbol = args.symbol
    arg_dataFrequency = args.data_frequency
    arg_dataYear = args.data_year
    input_file = args.input

    fin_obj=get_financial_data(arg_dataType,arg_dataStatus,arg_dataFrequency,arg_dataYear)
    symbol_obj = Symbol.objects.get(symbolName=arg_symbol)
    if (arg_model_name == "IncomeStatement"):
        calculate_metric_from_income_stmt(fin_obj,symbol_obj,input_file)
    elif(arg_model_name == "CashFlow"):
        calculate_metric_from_cash_flow_stmt(fin_obj,symbol_obj,input_file)
    elif(arg_model_name == "BalanceSheet"):
        calculate_metric_from_balancesheet_stmt(fin_obj,symbol_obj,input_file)

