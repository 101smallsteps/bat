from django.db import models
import datetime
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

def year_choices():
  return [(r, r) for r in range(1950, datetime.date.today().year + 1)]

def current_year():
  return datetime.date.today().year

class Symbol(models.Model):
  symbolName = models.CharField(max_length=255)
  companyName = models.CharField(max_length=255)
  created_date = models.DateTimeField(auto_now_add=True)
  updated_date = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.symbolName}"
class FinanceData(models.Model):
  DATA_TAG = [
    ("Q","Quarterly"),
    ("A", "Annual"),
  ]
  DATA_WORK_STATUS=[
    ("CREATE", "Work Created"),
    ("START", "Work Started"),
    ("DONE", "Work Done"),
    ("VERIFY", "Work Verification In Progress"),
    ("APPR", "Work APPROVED"),
  ]
  DATA_TAG = [
    ("Q","Quarterly"),
    ("A", "Annual"),
  ]
  DATA_FREQUENCY=[
    ("Q_1", "Quarterly_1"),
    ("Q_2", "Quarterly_2"),
    ("Q_3", "Quarterly_3"),
    ("Q_4", "Quarterly_4"),
    ("A","Annual")
  ]
  dataType = models.CharField(max_length=1, choices=DATA_TAG)
  dataStatus = models.CharField(max_length=6, choices=DATA_WORK_STATUS)
  symbol = models.ForeignKey(Symbol, related_name='findata_symbol',on_delete=models.CASCADE)
  dataFrequency = models.CharField(max_length=6, choices=DATA_FREQUENCY)
  dataYear = models.IntegerField(_('year'), choices=year_choices(), default=current_year())
  datePub = models.DateField()
class IncomeStatement(models.Model):
  financeInfo=models.ForeignKey(FinanceData,related_name='income_financeInfo',on_delete=models.CASCADE)
  totalRevenue = models.IntegerField()
  totalRevenue_operatingRevenue = models.IntegerField()


class BalanceSheet(models.Model):
  dataTag=models.ForeignKey(FinanceData,on_delete=models.CASCADE)
  totalAssets = models.IntegerField()
  totalAssets_currentAssets = models.IntegerField()

class CashFlow(models.Model):
  dataTag=models.ForeignKey(FinanceData,on_delete=models.CASCADE)
  freeCashFlow = models.IntegerField()

class Ratio(models.Model):
  financeInfo=models.ForeignKey(FinanceData,related_name='ratios_financeInfo',on_delete=models.CASCADE)
  DEratio = models.FloatField()


class ValueCompanies(models.Model):
  rank=models.IntegerField()
  symbol = models.ForeignKey(Symbol,related_name='vc_symbol',on_delete=models.CASCADE)


class GrowthCompanies(models.Model):
  rank = models.IntegerField()
  symbol = models.ForeignKey(Symbol,related_name='gc_symbol', on_delete=models.CASCADE)

class DividendCompanies(models.Model):
  rank = models.IntegerField()
  symbol = models.ForeignKey(Symbol,related_name='dc_symbol', on_delete=models.CASCADE)

class Portfolio(models.Model):
  owner  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolio_owner', blank = True, null = True)
  symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name='user_symbol', blank = True, null = True)
#  symbol = models.CharField(max_length = 180)
  created_date = models.DateTimeField(auto_now_add=True)
  updated_date = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.symbol.companyName}"

class SymbolAnalysis(models.Model):
  ANALYSIS_STATUS = [
    ('GOOD','good'),
    ('BAD', 'bad'),
    ('OK', 'ok'),
  ]
  symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name='symbols_all')
  AnalysisStatus =  models.CharField(max_length=6, choices=ANALYSIS_STATUS)
  created_date = models.DateTimeField(auto_now_add=True)
  updated_date = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.symbol.companyName}"


class overallAnalysis(models.Model):
  ANALYSIS_STATUS = [
    ('GOOD','good'),
    ('BAD', 'bad'),
    ('OK', 'ok'),
  ]
  METRIC_NAMES = [
    ('REVENUE','Revenue'),
    ('DERATIO', 'DERatio'),
  ]
  symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name='symbols_all_overall')
  metric = models.CharField(max_length=20, choices=METRIC_NAMES)
  analysisResult = models.CharField(max_length=6, choices=ANALYSIS_STATUS)
  metricDisplay = models.CharField(max_length=6)