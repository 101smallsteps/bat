from django.db import models
import datetime
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

def year_choices():
  return [(r, r) for r in range(1950, datetime.date.today().year + 1)]

def current_year():
  return datetime.date.today().year

class Symbol(models.Model):
  SECTOR_TYPE =[
    ("CSE", "ConsumerElectronics"),
    ("ROB", "ROBOTICS"),
    ("SEMI", "Semiconductor"),
    ("SEMIDESIGN", "SemiconductorDesign"),
    ("SEMIFAB", "SemiconductorFab"),
    ("CTRAN", "ConsumerTransportation")
  ]
  symbolName = models.CharField(max_length=255)
  companyName = models.CharField(max_length=255)
  sector = models.CharField(max_length=50, choices=SECTOR_TYPE)
  created_date = models.DateTimeField(auto_now_add=True)
  updated_date = models.DateTimeField(auto_now=True)

  class Meta:
    app_label = 'financials'

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
  DATA_FREQUENCY=[
    ("Q_1", "Q_1"),
    ("Q_2", "Q_2"),
    ("Q_3", "Q_3"),
    ("Q_4", "Q_4"),
    ("A","Annual")
  ]

  class Meta:
    app_label = 'financials'
    unique_together = ('dataType', 'dataStatus','symbol','dataFrequency','dataYear')  # Prevents duplicates based on date and description

  dataType = models.CharField(max_length=1, choices=DATA_TAG)
  dataStatus = models.CharField(max_length=6, choices=DATA_WORK_STATUS)
  symbol = models.ForeignKey(Symbol, related_name='findata_symbol',on_delete=models.CASCADE)
  dataFrequency = models.CharField(max_length=6, choices=DATA_FREQUENCY)
  dataYear = models.IntegerField(_('year'), choices=year_choices(), default=current_year())
  datePub = models.DateField(null=True)

class IncomeStatement(models.Model):
  class Meta:
    app_label = 'financials'

  financeInfo=models.ForeignKey(FinanceData,related_name='income_financeInfo',on_delete=models.CASCADE)
  TaxEffectOfUnusualItems = models.FloatField(default=0.0,null=True)
  TaxRateForCalcs = models.FloatField(default=0.0,null=True)
  NormalizedEBITDA = models.FloatField(default=0.0,null=True)
  NetIncomeFromContinuingOperationNetMinorityInterest = models.FloatField(default=0.0,null=True)
  ReconciledDepreciation = models.FloatField(default=0.0,null=True)
  ReconciledCostOfRevenue = models.FloatField(default=0.0,null=True)
  EBITDA = models.FloatField(default=0.0,null=True)
  EBIT = models.FloatField(default=0.0,null=True)
  NetInterestIncome = models.FloatField(default=0.0,null=True)
  InterestExpense = models.FloatField(default=0.0,null=True)
  InterestIncome = models.FloatField(default=0.0,null=True)
  NormalizedIncome = models.FloatField(default=0.0,null=True)
  NetIncomeFromContinuingAndDiscontinuedOperation = models.FloatField(default=0.0,null=True)
  TotalExpenses = models.FloatField(default=0.0,null=True)
  TotalOperatingIncomeAsReported = models.FloatField(default=0.0,null=True)
  DilutedAverageShares = models.FloatField(default=0.0,null=True)
  BasicAverageShares = models.FloatField(default=0.0,null=True)
  DilutedEPS = models.FloatField(default=0.0,null=True)
  BasicEPS = models.FloatField(default=0.0,null=True)
  DilutedNIAvailtoComStockholders = models.FloatField(default=0.0,null=True)
  NetIncomeCommonStockholders = models.FloatField(default=0.0,null=True)
  NetIncome = models.FloatField(default=0.0,null=True)
  NetIncomeIncludingNoncontrollingInterests = models.FloatField(default=0.0,null=True)
  NetIncomeContinuousOperations = models.FloatField(default=0.0,null=True)
  TaxProvision = models.FloatField(default=0.0,null=True)
  PretaxIncome = models.FloatField(default=0.0,null=True)
  OtherIncomeExpense = models.FloatField(default=0.0,null=True)
  OtherNonOperatingIncomeExpenses = models.FloatField(default=0.0,null=True)
  NetNonOperatingInterestIncomeExpense = models.FloatField(default=0.0,null=True)
  InterestExpenseNonOperating = models.FloatField(default=0.0,null=True)
  InterestIncomeNonOperating = models.FloatField(default=0.0,null=True)
  OperatingIncome = models.FloatField(default=0.0,null=True)
  OperatingExpense = models.FloatField(default=0.0,null=True)
  ResearchAndDevelopment = models.FloatField(default=0.0,null=True)
  SellingGeneralAndAdministration = models.FloatField(default=0.0,null=True)
  GrossProfit = models.FloatField(default=0.0,null=True)
  CostOfRevenue = models.FloatField(default=0.0,null=True)
  TotalRevenue = models.FloatField(default=0.0,null=True)
  OperatingRevenue = models.FloatField(default=0.0,null=True)

class BalanceSheet(models.Model):
  class Meta:
    app_label = 'financials'

  financeInfo=models.ForeignKey(FinanceData,related_name='balancesheet_financeInfo',on_delete=models.CASCADE)
  TreasurySharesNumber = models.FloatField(default=0.0, null=True)
  OrdinarySharesNumber = models.FloatField(default=0.0, null=True)
  ShareIssued = models.FloatField(default=0.0, null=True)
  NetDebt = models.FloatField(default=0.0, null=True)
  TotalDebt = models.FloatField(default=0.0, null=True)
  TangibleBookValue = models.FloatField(default=0.0, null=True)
  InvestedCapital = models.FloatField(default=0.0, null=True)
  WorkingCapital = models.FloatField(default=0.0, null=True)
  NetTangibleAssets = models.FloatField(default=0.0, null=True)
  CapitalLeaseObligations = models.FloatField(default=0.0, null=True)
  CommonStockEquity = models.FloatField(default=0.0, null=True)
  TotalCapitalization = models.FloatField(default=0.0, null=True)
  TotalEquityGrossMinorityInterest = models.FloatField(default=0.0, null=True)
  StockholdersEquity = models.FloatField(default=0.0, null=True)
  GainsLossesNotAffectingRetainedEarnings = models.FloatField(default=0.0, null=True)
  OtherEquityAdjustments = models.FloatField(default=0.0, null=True)
  RetainedEarnings = models.FloatField(default=0.0, null=True)
  CapitalStock = models.FloatField(default=0.0, null=True)
  CommonStock = models.FloatField(default=0.0, null=True)
  TotalLiabilitiesNetMinorityInterest = models.FloatField(default=0.0, null=True)
  TotalNonCurrentLiabilitiesNetMinorityInterest = models.FloatField(default=0.0, null=True)
  OtherNonCurrentLiabilities = models.FloatField(default=0.0, null=True)
  TradeandOtherPayablesNonCurrent = models.FloatField(default=0.0, null=True)
  LongTermDebtAndCapitalLeaseObligation = models.FloatField(default=0.0, null=True)
  LongTermCapitalLeaseObligation = models.FloatField(default=0.0, null=True)
  LongTermDebt = models.FloatField(default=0.0, null=True)
  CurrentLiabilities = models.FloatField(default=0.0, null=True)
  OtherCurrentLiabilities = models.FloatField(default=0.0, null=True)
  CurrentDeferredLiabilities = models.FloatField(default=0.0, null=True)
  CurrentDeferredRevenue = models.FloatField(default=0.0, null=True)
  CurrentDebtAndCapitalLeaseObligation = models.FloatField(default=0.0, null=True)
  CurrentCapitalLeaseObligation = models.FloatField(default=0.0, null=True)
  CurrentDebt = models.FloatField(default=0.0, null=True)
  OtherCurrentBorrowings = models.FloatField(default=0.0, null=True)
  CommercialPaper = models.FloatField(default=0.0, null=True)
  PayablesAndAccruedExpenses = models.FloatField(default=0.0, null=True)
  Payables = models.FloatField(default=0.0, null=True)
  TotalTaxPayable = models.FloatField(default=0.0, null=True)
  IncomeTaxPayable = models.FloatField(default=0.0, null=True)
  AccountsPayable = models.FloatField(default=0.0, null=True)
  TotalAssets = models.FloatField(default=0.0, null=True)
  TotalNonCurrentAssets = models.FloatField(default=0.0, null=True)
  OtherNonCurrentAssets = models.FloatField(default=0.0, null=True)
  NonCurrentDeferredAssets = models.FloatField(default=0.0, null=True)
  NonCurrentDeferredTaxesAssets = models.FloatField(default=0.0, null=True)
  InvestmentsAndAdvances = models.FloatField(default=0.0, null=True)
  OtherInvestments = models.FloatField(default=0.0, null=True)
  InvestmentinFinancialAssets = models.FloatField(default=0.0, null=True)
  AvailableForSaleSecurities = models.FloatField(default=0.0, null=True)
  NetPPE = models.FloatField(default=0.0, null=True)
  AccumulatedDepreciation = models.FloatField(default=0.0, null=True)
  GrossPPE = models.FloatField(default=0.0, null=True)
  Leases = models.FloatField(default=0.0, null=True)
  OtherProperties = models.FloatField(default=0.0, null=True)
  MachineryFurnitureEquipment = models.FloatField(default=0.0, null=True)
  LandAndImprovements = models.FloatField(default=0.0, null=True)
  Properties = models.FloatField(default=0.0, null=True)
  CurrentAssets = models.FloatField(default=0.0, null=True)
  OtherCurrentAssets = models.FloatField(default=0.0, null=True)
  Inventory = models.FloatField(default=0.0, null=True)
  FinishedGoods = models.FloatField(default=0.0, null=True)
  RawMaterials = models.FloatField(default=0.0, null=True)
  Receivables = models.FloatField(default=0.0, null=True)
  OtherReceivables = models.FloatField(default=0.0, null=True)
  AccountsReceivable = models.FloatField(default=0.0, null=True)
  CashCashEquivalentsAndShortTermInvestments = models.FloatField(default=0.0, null=True)
  OtherShortTermInvestments = models.FloatField(default=0.0, null=True)
  CashAndCashEquivalents = models.FloatField(default=0.0, null=True)
  CashEquivalents = models.FloatField(default=0.0, null=True)
  CashFinancial = models.FloatField(default=0.0, null=True)

class CashFlow(models.Model):
  class Meta:
    app_label = 'financials'

  financeInfo=models.ForeignKey(FinanceData,related_name='cashflow_financeInfo',on_delete=models.CASCADE)
  FreeCashFlow = models.FloatField(default=0.0,null=True)
  RepurchaseOfCapitalStock = models.FloatField(default=0.0,null=True)
  RepaymentOfDebt = models.FloatField(default=0.0,null=True)
  IssuanceOfDebt = models.FloatField(default=0.0,null=True)
  CapitalExpenditure = models.FloatField(default=0.0,null=True)
  InterestPaidSupplementalData = models.FloatField(default=0.0,null=True)
  IncomeTaxPaidSupplementalData = models.FloatField(default=0.0,null=True)
  EndCashPosition = models.FloatField(default=0.0,null=True)
  BeginningCashPosition = models.FloatField(default=0.0,null=True)
  ChangesInCash = models.FloatField(default=0.0,null=True)
  FinancingCashFlow = models.FloatField(default=0.0,null=True)
  CashFlowFromContinuingFinancingActivities = models.FloatField(default=0.0,null=True)
  NetOtherFinancingCharges = models.FloatField(default=0.0,null=True)
  CashDividendsPaid = models.FloatField(default=0.0,null=True)
  CommonStockDividendPaid = models.FloatField(default=0.0,null=True)
  NetCommonStockIssuance = models.FloatField(default=0.0,null=True)
  CommonStockPayments = models.FloatField(default=0.0,null=True)
  NetIssuancePaymentsOfDebt = models.FloatField(default=0.0,null=True)
  NetShortTermDebtIssuance = models.FloatField(default=0.0,null=True)
  ShortTermDebtPayments = models.FloatField(default=0.0,null=True)
  NetLongTermDebtIssuance = models.FloatField(default=0.0,null=True)
  LongTermDebtPayments = models.FloatField(default=0.0,null=True)
  LongTermDebtIssuance = models.FloatField(default=0.0,null=True)
  InvestingCashFlow = models.FloatField(default=0.0,null=True)
  CashFlowFromContinuingInvestingActivities = models.FloatField(default=0.0,null=True)
  NetOtherInvestingChanges = models.FloatField(default=0.0,null=True)
  NetInvestmentPurchaseAndSale = models.FloatField(default=0.0,null=True)
  SaleOfInvestment = models.FloatField(default=0.0,null=True)
  PurchaseOfInvestment = models.FloatField(default=0.0,null=True)
  NetPPEPurchaseAndSale = models.FloatField(default=0.0,null=True)
  PurchaseOfPPE = models.FloatField(default=0.0,null=True)
  OperatingCashFlow = models.FloatField(default=0.0,null=True)
  CashFlowFromContinuingOperatingActivities = models.FloatField(default=0.0,null=True)
  ChangeInWorkingCapital = models.FloatField(default=0.0,null=True)
  ChangeInOtherWorkingCapital = models.FloatField(default=0.0,null=True)
  ChangeInOtherCurrentLiabilities = models.FloatField(default=0.0,null=True)
  ChangeInOtherCurrentAssets = models.FloatField(default=0.0,null=True)
  ChangeInPayablesAndAccruedExpense = models.FloatField(default=0.0,null=True)
  ChangeInPayable = models.FloatField(default=0.0,null=True)
  ChangeInAccountPayable = models.FloatField(default=0.0,null=True)
  ChangeInInventory = models.FloatField(default=0.0,null=True)
  ChangeInReceivables = models.FloatField(default=0.0,null=True)
  ChangesInAccountReceivables = models.FloatField(default=0.0,null=True)
  OtherNonCashItems = models.FloatField(default=0.0,null=True)
  StockBasedCompensation = models.FloatField(default=0.0,null=True)
  DepreciationAmortizationDepletion = models.FloatField(default=0.0,null=True)
  DepreciationAndAmortization = models.FloatField(default=0.0,null=True)
  NetIncomeFromContinuingOperations = models.FloatField(default=0.0,null=True)


class Ratio(models.Model):
  class Meta:
    app_label = 'financials'

  financeInfo=models.ForeignKey(FinanceData,related_name='ratios_financeInfo',on_delete=models.CASCADE)
#START Derived from income statement
  # GrossProfit/OperatingRevenue(NetSales) or (TotalRevenue - CostOfRevenue)/TotalRevenue
  # FOR AAPL  GrossProfit/OperatingRevenue
  GrossMargin = models.FloatField(default=0.0,null=True)
  # This metric needs to be gathered based on resarch
  ProfitMargin= models.FloatField(default=0.0,null=True)

#END Derived from income statement
#END Derived from income statement
  DEratio = models.FloatField(default=0.0,null=True)


class ValueCompanies(models.Model):
  class Meta:
    app_label = 'financials'

  rank=models.IntegerField()
  symbol = models.ForeignKey(Symbol,related_name='vc_symbol',on_delete=models.CASCADE)


class GrowthCompanies(models.Model):
  class Meta:
    app_label = 'financials'
  rank = models.IntegerField()
  symbol = models.ForeignKey(Symbol,related_name='gc_symbol', on_delete=models.CASCADE)

class DividendCompanies(models.Model):
  class Meta:
    app_label = 'financials'
  rank = models.IntegerField()
  symbol = models.ForeignKey(Symbol,related_name='dc_symbol', on_delete=models.CASCADE)

class Portfolio(models.Model):
  class Meta:
    app_label = 'financials'
  owner  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolio_owner', blank = True, null = True)
  symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name='user_symbol', blank = True, null = True)
#  symbol = models.CharField(max_length = 180)
  created_date = models.DateTimeField(auto_now_add=True)
  updated_date = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.symbol.companyName}"

class SymbolAnalysis(models.Model):
  class Meta:
    app_label = 'financials'

  ANALYSIS_STATUS = [
    ('VGOOD', 'vgood'),
    ('GOOD','good'),
    ('BAD', 'bad'),
    ('OK', 'ok'),
  ]
  symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name='symbols_all')
  AnalysisStatus =  models.CharField(max_length=6, choices=ANALYSIS_STATUS)
  rank = models.IntegerField(default=0.0)
  max_rank = models.IntegerField(default=0.0)
  created_date = models.DateTimeField(auto_now_add=True)
  updated_date = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.symbol.companyName}"


class overallAnalysis(models.Model):
  class Meta:
    app_label = 'financials'

  ANALYSIS_STATUS = [
    ('VGOOD', 'verygood'),
    ('GOOD','good'),
    ('BAD', 'bad'),
    ('OK', 'ok'),
    ('NAVL', 'navl'),
  ]
  METRIC_NAMES = [
    ('REVENUE','Revenue'),  #MAX-RANK - 10
    ('GROSSMARGIN','GrossMargin'),#MAX-RANK - 10
    ('DERATIO', 'DERatio'), #MAX-RANK - 5
     ]
  symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name='symbols_all_overall')
  metric = models.CharField(max_length=20, choices=METRIC_NAMES)
  rank = models.IntegerField(default=0.0)
  max_rank = models.IntegerField(default=0.0)
  analysisResult = models.CharField(max_length=6, default='NAVL',choices=ANALYSIS_STATUS)
  metricDisplay = models.CharField(max_length=6)