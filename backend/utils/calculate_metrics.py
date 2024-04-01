import csv
import os
import django
from django.apps import apps
from django.utils import timezone
import sys

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

def get_financial_data(a_dataType,a_dataStatus,a_symbol,a_dataFrequency,a_dataYear):
    sym = Symbol.objects.get(pk=1)
    try:
        obj = FinanceData.objects.create(
            dataType=a_dataType,
            dataStatus=a_dataStatus,
            symbol=sym,
            dataFrequency=a_dataFrequency,
            dataYear=a_dataYear,
            datePub=timezone.now().date()
        )
        return obj

    except FinanceData.DoesNotExist:
        print("Problem in workflow , this script needs to be used after DB update ")
    return None

def update_gross_margin(fin_obj,csv_data):
    print(csv_data['GrossProfit']['Value'])
    l_GrossMargin = (float(csv_data['GrossProfit']['Value']) / float(csv_data['OperatingRevenue']['Value'])) * 100
    print(l_GrossMargin)
    try:
        ratio_obj = Ratio.objects.get(
            financeInfo=fin_obj,
        )
        #FOR AAPL  GrossProfit/OperatingRevenue * 100
        ratio_obj.GrossMargin = l_GrossMargin
        ratio_obj.save()
    except Ratio.DoesNotExist:
        ratio_obj = Ratio.objects.create(
            financeInfo=fin_obj,
            GrossMargin=l_GrossMargin
        )



def calculate_metric_from_income_stmt(fin_obj, csv_file_path):
    csv_data=read_csv(csv_file_path)
    update_gross_margin(fin_obj, csv_data)



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

    fin_obj=get_financial_data(arg_dataType,arg_dataStatus,arg_symbol,arg_dataFrequency,arg_dataYear)
    if (arg_model_name == "IncomeStatement"):
        calculate_metric_from_income_stmt(fin_obj,input_file)
