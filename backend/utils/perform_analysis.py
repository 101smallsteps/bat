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
from financials.models import overallAnalysis
from financials.models import SymbolAnalysis

#Perform analysis on symbols and concludes
symbols_to_be_analyzed=['AAPL']
# For every quarter
# For every 2% change - we give 1 point and a max of 10 points beyond 20%
# also -ve change also assigned in similar lines
# Finally get the average
def analyse_revenue(sym,sym_obj,last_5_fin_obj):
    analysis_status="BAD"
    last_5_revenues=[]
    last_4_revenue_changes = []
    last_4_revenue_points = []
    last_revenue_margin=0
    for fin_obj in last_5_fin_obj:
        #Get the available revenue metrics and check whether last 4 quarter revenues have increased/same
        obj=IncomeStatement.objects.get(financeInfo=fin_obj)
        last_5_revenues.append(obj.TotalRevenue)
    print(last_5_revenues)
    number_of_revenues=len(last_5_revenues)

    if number_of_revenues > 1:
        # Get the change in revenue between the last 4 revenue's
        for i in range(number_of_revenues-1):
            change=(last_5_revenues[i+1] - last_5_revenues[i])/last_5_revenues[i]
            last_revenue_margin = change
            truncated_change = change % 20
            point = truncated_change/2
            last_4_revenue_changes.append(change)
            last_4_revenue_points.append(point)
    else:
        # since only one value is present , we are providing a midpoint value ,
        # since with just revenue context and one data point ,we cannot conclude anything
        last_4_revenue_points.append(5)
        last_4_revenue_changes.append(0)
        last_revenue_margin = -1

    # get the average revenue point
    point=0
    for i in last_4_revenue_points:
        point = point + i
    avg_point= point/number_of_revenues

    if avg_point > 8:
        analysis_status="VGOOD"
    elif avg_point >5 and avg_point < 8:
        analysis_status="GOOD"
    elif avg_point >=0 and avg_point < 5:
        analysis_status="OK"
    elif avg_point < 0  and avg_point >= -5:
        analysis_status="OK"
    elif avg_point < -5:
        analysis_status="BAD"
    data={
        'metric':'REVENUE',
        'rank':avg_point,
        'analysisResult':analysis_status,
        # For every 2% change - we give 1 point and a max of 10 points beyond 20%
        'max_rank':10,
        'metricDisplay':last_revenue_margin
    }
    lookup_params ={
        'symbol':sym_obj
    }
    obj,created=overallAnalysis.objects.update_or_create(defaults=data,**lookup_params)

    return obj
# how to perform SymbolAnalysis
# check all the metrics analyzed and mark it as whether good ,bad,ok
def perform_symbol_analysis(sym,sym_obj):
    # for all the mertics analyzed - get the metric ranking ,calulate the overall ranking and decide whether
    # good ,bad,ok from a symbol perspective
    # get all the metrics focused for analysis and get each ranking
    all_mertics = overallAnalysis.objects.filter(symbol=sym_obj)

    achieved_overall_rank=0
    max_rank = 0
    for metric in all_mertics:
        achieved_overall_rank = achieved_overall_rank + metric.rank
        max_rank = max_rank + metric.max_rank

    if achieved_overall_rank >= max_rank * (90/100):
        analysis_status="VGOOD"
    elif achieved_overall_rank >= max_rank * (80/100):
        analysis_status="GOOD"
    elif achieved_overall_rank >= max_rank * (60/100):
        analysis_status="OK"
    elif achieved_overall_rank < max_rank * (60/100):
        analysis_status="OK"
    elif achieved_overall_rank < 0:
        analysis_status="BAD"
    data={
        'rank':achieved_overall_rank,
        'AnalysisStatus':analysis_status,
        # For every 2% change - we give 1 point and a max of 10 points beyond 20%
        'max_rank':max_rank,
    }
    lookup_params ={
        'symbol':sym_obj
    }
    obj,created=SymbolAnalysis.objects.update_or_create(defaults=data,**lookup_params)


# how to perform overallAnalysis
def perform_overall_analysis(sym,sym_obj,last_5_fin_obj):
    analyse_revenue(sym,sym_obj,last_5_fin_obj)


# how to perform overallAnalysis
def perform_analysis():
    for sym in symbols_to_be_analyzed:
        sym_obj=Symbol.objects.get(symbolName=sym)
        # Get last 4 finance data for the symbol
        try:
            last_5_fin_obj_filter = FinanceData.objects.filter(symbol=sym_obj).order_by('-id')
            last_5_fin_obj=last_5_fin_obj_filter[:5]
            # Perform analysis for each metric and rank them and also mark as good,bad,ok
            perform_overall_analysis(sym,sym_obj,last_5_fin_obj)
            # Based on the ranking mark whether good,bad,ok
            perform_symbol_analysis(sym,sym_obj)
        except FinanceData.DoesNotExist:
            pass

if __name__ == "__main__":
    perform_analysis()