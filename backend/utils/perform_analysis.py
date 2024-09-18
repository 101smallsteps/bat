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
def analyse_revenue(sym,sym_obj,last_2_fin_obj):
    analysis_status="NAVL"
    last_2_revenues=[0,0]
    # if revenue equal or +- 1%  - OK (when compared to previous quarter)
    # if revenue greater than 5% - Good
    # if revenue greater than 10% - VGood
    # anything else BAD
    revenue_count = 0
    change_percent = 0
    for fin_obj in last_2_fin_obj:
        #Get the available revenue metrics and check whether last 4 quarter revenues have increased/same
        obj=IncomeStatement.objects.get(financeInfo=fin_obj)
        last_2_revenues[revenue_count]=obj.TotalRevenue
        revenue_count =  revenue_count + 1
    print(last_2_revenues)

    try:
        change_percent = round((last_2_revenues[1] - last_2_revenues[0]) / last_4_revenues[0], 2) * 100
        if change_percent >= -1 and change_percent <= 1:
            analysis_status="OK"
        elif change_percent >= 5 and change_percent <10 :
            analysis_status = "GOOD"
        elif change_percent > 10:
            analysis_status = "VGOOD"
        else:
            analysis_status = "BAD"
    except:
        analysis_status = "NAVL"

    data={
        'rank':10,
        'analysisResult':analysis_status,
        # For every 2% change - we give 1 point and a max of 10 points beyond 20%
        'max_rank':10,
        'metricDisplay':change_percent
    }
    lookup_params ={
        'metric': 'Revenue',
        'symbol':sym_obj
    }
    obj,created=overallAnalysis.objects.update_or_create(defaults=data,**lookup_params)

    return obj

def analyse_revenue_vs_costOfRevenue(sym,sym_obj,last_4_fin_obj):
    analysis_status="BAD"
    last_4_revenues=[0,0,0,0]
    last_4_CostOfRevenues=[0,0,0,0]
    last_4_revenues_changes=[0,0,0,0]
    last_4_CostOfRevenues_changes=[0,0,0,0]
    # no change in reveneue but increase in Cost Of Revenue is bad
    # increase in revenue with increase in Cost of Revenue is very good
    # decrease in revenue with increase in Cost of Revenue is bad
    last_4_ratios = [0.0,0.0,0.0,0.0]

    revenue_counter=0
    for fin_obj in last_4_fin_obj:
        #Get the available revenue metrics and check whether last 4 quarter revenues have increased/same
        obj=IncomeStatement.objects.get(financeInfo=fin_obj)
        last_4_revenues[revenue_counter]=obj.TotalRevenue
        last_4_CostOfRevenues[revenue_counter]=obj.CostOfRevenue
        revenue_counter = revenue_counter + 1
    print(last_4_revenues)
    print(last_4_CostOfRevenues)
    number_of_revenues=len(last_4_revenues)
    number_of_CostOfRevenues = len(last_4_CostOfRevenues)

    if number_of_revenues > 1:
        # Get the change in revenue between the last 4 revenue's
        for i in range(number_of_revenues-1):
            try:
                change_percent_revenue = round((last_4_revenues[i + 1] - last_4_revenues[i]) / last_4_revenues[i], 2) * 100
                change_percent_cost_of_revenue  = round((last_4_CostOfRevenues[i + 1] - last_4_CostOfRevenues[i]) / last_4_CostOfRevenues[i], 2) * 100
                last_4_revenues_changes[i+1] = change_percent_revenue
                last_4_CostOfRevenues_changes[i+1] = change_percent_cost_of_revenue
                last_4_ratios[i+1] =round((last_4_revenues[i+1]/last_4_CostOfRevenues[i+1]),2)
            except:
                last_4_revenues_changes[i + 1] = 0.0
                last_4_CostOfRevenues_changes[i + 1] = 0.0
                last_4_ratios[i + 1] = 0.0
    else:
        last_4_ratios[1]=0.0
        last_4_revenues_changes[1] = 0.0
        last_4_CostOfRevenues_changes[1] = 0.0

    # If posiitive change in revenue is proportional is change in cost of ownership then Good

    if last_4_revenues_changes[3] >= last_4_CostOfRevenues_changes[3]:
        analysis_status = "VGOOD"
    else:
        analysis_status = "BAD"

    data={
        'rank':1,
        'analysisResult':analysis_status,
        # For every 2% change - we give 1 point and a max of 10 points beyond 20%
        'max_rank':10,
        'metricDisplay': f'{last_4_revenues_changes[3]} VS {last_4_CostOfRevenues_changes[3]}',
    }
    lookup_params ={
        'metric': 'RevenueVsCoR',
        'symbol':sym_obj
    }
    obj,created=overallAnalysis.objects.update_or_create(defaults=data,**lookup_params)

    return obj

def analyse_consecutive_revenue_growth(sym,sym_obj,last_4_fin_obj):
    analysis_status="BAD"
    last_4_revenues=[0,0,0,0]
    change_percent=0
    last_4_revenue_rate_of_changes = [0,0,0,0]
    # check whether 0000
    # check whether 0001 OK
    # check whether 0010
    # check whether 0011 GOOD
    # check whether 0100
    # check whether 0101
    # check whether 0111  VGOOD
    revenue_count=0
    for fin_obj in last_4_fin_obj:
        #Get the available revenue metrics and check whether last 4 quarter revenues have increased/same
        obj=IncomeStatement.objects.get(financeInfo=fin_obj)
        last_4_revenues[revenue_count]=obj.TotalRevenue
        revenue_count = revenue_count + 1
    print(last_4_revenues)
    number_of_revenues=len(last_4_revenues)

    if number_of_revenues > 1:
        # Get the change in revenue between the last 4 revenue's
        try:
            for i in range(number_of_revenues-1):
                change_percent=round((last_4_revenues[i+1] - last_4_revenues[i])/last_4_revenues[i],2)*100
                last_4_revenue_rate_of_changes.append(change_percent)
            if last_4_revenue_rate_of_changes[1] >= 1 and last_4_revenue_rate_of_changes[2] >= 1 and last_4_revenue_rate_of_changes[3] >= 1:
                analysis_status = "VGOOD"
            elif last_4_revenue_rate_of_changes[1] <= 0 and last_4_revenue_rate_of_changes[2] >= 1 and last_4_revenue_rate_of_changes[3] >= 1:
                analysis_status = "GOOD"
            elif last_4_revenue_rate_of_changes[1] <= 0 and last_4_revenue_rate_of_changes[2] <= 0 and last_4_revenue_rate_of_changes[3] >= 1:
                analysis_status = "OK"
            else:
                analysis_status = "BAD"
        except:
            analysis_status = "NAVL"
    else:
        # since only one value is present , we are providing a midpoint value ,
        # since with just revenue context and one data point ,we cannot conclude anything
        last_4_revenue_rate_of_changes.append(0)
        analysis_status = "NAVL"



    data={
        'rank':change_percent,
        'analysisResult':analysis_status,
        # For every 2% change - we give 1 point and a max of 10 points beyond 20%
        'max_rank':10,
        'metricDisplay':change_percent
    }
    lookup_params ={
        'metric': 'RevenueGrowthConsecutive',
        'symbol':sym_obj
    }
    obj,created=overallAnalysis.objects.update_or_create(defaults=data,**lookup_params)

    return obj

def analyse_GrossProfitMargin(sym,sym_obj,last_4_fin_obj):
    analysis_status="BAD"
    last_2_GrossProfitMargin=[]
    change=0
    last_4_revenues=[]
    for fin_obj in last_4_fin_obj:
        #Get the available revenue metrics and check whether last 4 quarter revenues have increased/same
        obj=Ratio.objects.get(financeInfo=fin_obj)
        last_4_revenues.append(obj.GrossProfitMargin)
    print(last_4_revenues)
    number_of_revenues=len(last_4_revenues)

    if number_of_revenues > 1:
        change = round(((last_4_revenues[0] - last_4_revenues[1]) / last_4_revenues[1]) * 100,2)
    else:
        change = 0

    change=10
    data={
        'rank':change,
        'analysisResult':analysis_status,
        # For every 2% change - we give 1 point and a max of 10 points beyond 20%
        'max_rank':10,
        'metricDisplay':change
    }
    lookup_params ={
        'metric': 'GrossProfitMargin',
        'symbol':sym_obj
    }
    obj,created=overallAnalysis.objects.update_or_create(defaults=data,**lookup_params)

    return obj

def analyse_NetProfitMargin(sym,sym_obj,last_1_fin_obj):
    analysis_status="BAD"
    change=10
    data={
        'rank':change,
        'analysisResult':analysis_status,
        # For every 2% change - we give 1 point and a max of 10 points beyond 20%
        'max_rank':10,
        'metricDisplay':change
    }
    lookup_params ={
        'metric': 'NetProfitMargin',
        'symbol':sym_obj
    }
    obj,created=overallAnalysis.objects.update_or_create(defaults=data,**lookup_params)

    return obj

def analyse_DEratio(sym,sym_obj,last_1_fin_obj):
    #Utilities: 2.0 - 4.0
    #RealEstate: 1.5 - 3.0
    #Transportation: 1.5 - 3.0
    #Telecommunications: 1.5 - 3.0
    #Technology: 0.5 - 1.5
    #Consumer Goods: 0.5 - 1.5
    #Retail: 0.5 - 1.5
    #Healthcare: 0.5 - 2.0
    #FinancialServices: 1.0 - 3.0
    #Manufacturing: 1.0 - 2.5
    #Energy: 1.5 - 3.0
    analysis_status="BAD"
    change=10
    obj = Ratio.objects.get(financeInfo=last_1_fin_obj)
    deRatio = obj.DEratio
    #0.5 - 1.5
    if deRatio <= 0.5:
        analysis_status = "VGOOD"
    elif deRatio >= 0.5 and deRatio <= 1.0 :
        analysis_status = "GOOD"
    elif deRatio >= 0.5 and deRatio <= 1.0 :
        analysis_status = "OK"
    elif deRatio >= 1.5:
        analysis_status = "BAD"

    data={
        'rank':change,
        'analysisResult':analysis_status,
        # For every 2% change - we give 1 point and a max of 10 points beyond 20%
        'max_rank':10,
        'metricDisplay':deRatio
    }
    lookup_params ={
        'metric': 'DEratio',
        'symbol':sym_obj
    }
    obj,created=overallAnalysis.objects.update_or_create(defaults=data,**lookup_params)

    return obj

def analyse_TDTAratio(sym,sym_obj,last_1_fin_obj):
    analysis_status="BAD"
    change=10
    obj = Ratio.objects.get(financeInfo=last_1_fin_obj)
    tdtaRatio = obj.TDTAratio
    if tdtaRatio > 2 :
        analysis_status="BAD"
    elif tdtaRatio > 1 and tdtaRatio < 2:
        analysis_status="OK"
    elif tdtaRatio < 0:
        analysis_status = "VGOOD"
    data={
        'rank':change,
        'analysisResult':analysis_status,
        # For every 2% change - we give 1 point and a max of 10 points beyond 20%
        'max_rank':10,
        'metricDisplay':tdtaRatio
    }
    lookup_params ={
        'metric': 'TDTAratio',
        'symbol':sym_obj
    }
    obj,created=overallAnalysis.objects.update_or_create(defaults=data,**lookup_params)

    return obj

def analyse_Currentratio(sym,sym_obj,last_1_fin_obj):
    #Industries with Typically High Current Ratios
    #Retail: 1.5 - 2.5
    #ConsumerGoods: 1.5 - 2.5
    #Healthcare: 1.5 - 2.5
    #Technology: 1.5 - 2.5
    #Industries with Typically Low Current Ratios
    #Utilities: 0.8 - 1.2
    #Transportation: 0.8 - 1.2
    #RealEstate: 0.8 - 1.2
    #Construction: 0.8 - 1.2
    #Other Industries
    #Financial Services: 1.0 - 1.5
    #Manufacturing: 1.0 - 1.5
    #Energy: 1.0 - 1.5
    analysis_status="BAD"
    change=10
    obj = Ratio.objects.get(financeInfo=last_1_fin_obj)
    currentRatio = obj.Currentratio
    # a high currentratio indicates inefficient use of assets
    # a low current ratio indicates liquidity problem
    if obj.Currentratio > 2.5:
        analysis_status = "OK"
    elif obj.Currentratio > 2 and obj.Currentratio < 2.5:
        analysis_status = "VGOOD"
    elif obj.Currentratio > 1.5 and obj.Currentratio < 2:
        analysis_status = "GOOD"
    elif obj.Currentratio < 1.5:
        analysis_status = "BAD"
    data={
        'rank':change,
        'analysisResult':analysis_status,
        # For every 2% change - we give 1 point and a max of 10 points beyond 20%
        'max_rank':10,
        'metricDisplay':currentRatio
    }
    lookup_params ={
        'metric': 'Currentratio',
        'symbol':sym_obj
    }
    obj,created=overallAnalysis.objects.update_or_create(defaults=data,**lookup_params)

    return obj

def analyse_Quickratio(sym,sym_obj,last_1_fin_obj):
    analysis_status="BAD"
    change=10
    obj = Ratio.objects.get(financeInfo=last_1_fin_obj)
    #Industries with Typically High Quick Ratios
    #Technology: 1.2 - 2.0
    #ConsumerGoods: 1.0 - 1.5
    #Healthcare: 1.0 - 1.5
    #Retail: 0.8 - 1.2
    #Industries with Typically Low Quick Ratios
    #Utilities: 0.5 - 0.8
    #Transportation: 0.5 - 0.8
    #Real Estate: 0.5 - 0.8
    #Construction: 0.5 - 0.8
    #Other Industries
    #Financial Services: 0.8 - 1.2
    #Manufacturing: 0.8 - 1.2
    #Energy: 0.8 - 1.2

    #A high quickratio indicates a strong liquidity position,
    #while a low quick ratio can signal potential liquidity problems
    quickRatio = obj.Quickratio
    if quickRatio > 2.0:
        analysis_status = "VGOOD"
    elif quickRatio > 1 and quickRatio < 2.0:
        analysis_status = "GOOD"
    elif quickRatio > 1 and quickRatio < 1.2:
        analysis_status = "OK"
    elif quickRatio < 1.2:
        analysis_status = "BAD"

    data={
        'rank':change,
        'analysisResult':analysis_status,
        # For every 2% change - we give 1 point and a max of 10 points beyond 20%
        'max_rank':10,
        'metricDisplay':quickRatio
    }
    lookup_params ={
        'metric': 'Quickratio',
        'symbol':sym_obj
    }
    obj,created=overallAnalysis.objects.update_or_create(defaults=data,**lookup_params)
    print (f'analyse_Quickratio - {created}')
    return obj

def analyse_Cashratio(sym,sym_obj,last_1_fin_obj):
    analysis_status="BAD"
    change=10
    obj = Ratio.objects.get(financeInfo=last_1_fin_obj)

    #Industries with Typically High Cash Ratios
    #Technology: 1.0 - 2.0
    #Consumer Goods: 0.8 - 1.2
    #Healthcare: 0.8 - 1.2
    #Retail: 0.5 - 0.8
    #Industries with Typically Low Cash Ratios
    #Utilities: 0.3 - 0.5
    #Transportation: 0.3 - 0.5
    #Real Estate: 0.3 - 0.5
    #Construction: 0.3 - 0.5
    #Other Industries
    #Financial Services: 0.5 - 1.0
    #Manufacturing: 0.5 - 1.0
    #Energy: 0.5 - 1.0

    #A high cash ratio indicates a strong liquidity position
    # a low cash ratio can signal potential liquidity problems.

    cashRatio = obj.Cashratio
    if cashRatio > 2.0:
        analysis_status = "VGOOD"
    elif cashRatio > 1 and cashRatio < 2:
        analysis_status = "GOOD"
    elif cashRatio == 1:
        analysis_status = "OK"
    elif cashRatio < 1:
        analysis_status = "BAD"

    data={
        'rank':change,
        'analysisResult':analysis_status,
        # For every 2% change - we give 1 point and a max of 10 points beyond 20%
        'max_rank':10,
        'metricDisplay':cashRatio
    }
    lookup_params ={
        'metric': 'Cashratio',
        'symbol':sym_obj
    }
    obj,created=overallAnalysis.objects.update_or_create(defaults=data,**lookup_params)
    print (f'analyse_Cashratio - {created}')

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
def perform_overall_analysis(sym,sym_obj,last_4_fin_obj_filter):
    last_4_fin_obj = last_4_fin_obj_filter[:4]
    last_2_fin_obj = last_4_fin_obj_filter[:2]
    last_1_fin_obj = last_4_fin_obj_filter[:1]
    print("starting perform_overall_analysis")
    analyse_revenue(sym,sym_obj,last_2_fin_obj)
    analyse_revenue_vs_costOfRevenue(sym,sym_obj,last_4_fin_obj)
    analyse_consecutive_revenue_growth(sym,sym_obj,last_4_fin_obj)
    analyse_GrossProfitMargin(sym,sym_obj,last_4_fin_obj)
    analyse_NetProfitMargin(sym,sym_obj,last_4_fin_obj)
    analyse_DEratio(sym,sym_obj,last_1_fin_obj)
    analyse_TDTAratio(sym,sym_obj,last_1_fin_obj)
    analyse_Quickratio(sym,sym_obj,last_1_fin_obj)
    analyse_Cashratio(sym,sym_obj,last_1_fin_obj)
    analyse_Currentratio(sym,sym_obj,last_1_fin_obj)

# how to perform overallAnalysis
def perform_analysis():
    for sym in symbols_to_be_analyzed:
        sym_obj=Symbol.objects.get(symbolName=sym)
        # Get last 4 finance data for the symbol
        try:
            last_4_fin_obj_filter = FinanceData.objects.order_by('-id')[:4]
            # Perform analysis for each metric and rank them and also mark as good,bad,ok
            perform_overall_analysis(sym,sym_obj,last_4_fin_obj_filter)
            # Based on the ranking mark whether good,bad,ok
            perform_symbol_analysis(sym,sym_obj)
        except FinanceData.DoesNotExist:
            pass

if __name__ == "__main__":
    perform_analysis()