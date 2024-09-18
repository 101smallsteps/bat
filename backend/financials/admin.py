from django.contrib import admin

# Register your models here.
from .models import Symbol, SymbolAnalysis, Portfolio, overallAnalysis, IncomeStatement, BalanceSheet, CashFlow, FinanceData, Ratio,\
DividendCompanies,GrowthCompanies,ValueCompanies
from django.contrib.auth.models import User

class UserAdmin(admin.ModelAdmin):
    model = User
    # Only display the "username" field
    fields = ["username"]


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    fields = (
        "owner","symbol", "created_date", "updated_date"
    )
    list_display = (
        "id","owner","symbol", "created_date", "updated_date"
    )
    readonly_fields = (
        "created_date", "updated_date",
    )


@admin.register(Symbol)
class SymbolAdmin(admin.ModelAdmin):
    fields = (
        "symbolName", "companyName","sector", "created_date", "updated_date",
    )
    list_display = (
        "id","symbolName", "companyName","sector", "created_date", "updated_date",
    )
    readonly_fields = (
        "created_date", "updated_date",
    )

@admin.register(SymbolAnalysis)
class SymbolAnalysisAdmin(admin.ModelAdmin):
    fields = (
        "symbol", "AnalysisStatus", "created_date", "updated_date",
    )
    list_display = (
        "symbol", "AnalysisStatus", "created_date", "updated_date",
    )
    readonly_fields = (
        "created_date", "updated_date",
    )

@admin.register(IncomeStatement)
class IncomeStatementAdmin(admin.ModelAdmin):
    fields = (
        "financeInfo", "TaxEffectOfUnusualItems","TaxRateForCalcs","NormalizedEBITDA","NetIncomeFromContinuingOperationNetMinorityInterest","ReconciledDepreciation","ReconciledCostOfRevenue","EBITDA","EBIT","NetInterestIncome","InterestExpense","InterestIncome","NormalizedIncome","NetIncomeFromContinuingAndDiscontinuedOperation","TotalExpenses","TotalOperatingIncomeAsReported","DilutedAverageShares","BasicAverageShares","DilutedEPS","BasicEPS","DilutedNIAvailtoComStockholders","NetIncomeCommonStockholders","NetIncome","NetIncomeIncludingNoncontrollingInterests","NetIncomeContinuousOperations","TaxProvision","PretaxIncome","OtherIncomeExpense","OtherNonOperatingIncomeExpenses","NetNonOperatingInterestIncomeExpense","InterestExpenseNonOperating","InterestIncomeNonOperating","OperatingIncome","OperatingExpense","ResearchAndDevelopment","SellingGeneralAndAdministration","GrossProfit","CostOfRevenue","TotalRevenue","OperatingRevenue"
    )
    list_display = (
        "financeInfo", "TaxEffectOfUnusualItems","TaxRateForCalcs","NormalizedEBITDA","NetIncomeFromContinuingOperationNetMinorityInterest","ReconciledDepreciation","ReconciledCostOfRevenue","EBITDA","EBIT","NetInterestIncome","InterestExpense","InterestIncome","NormalizedIncome","NetIncomeFromContinuingAndDiscontinuedOperation","TotalExpenses","TotalOperatingIncomeAsReported","DilutedAverageShares","BasicAverageShares","DilutedEPS","BasicEPS","DilutedNIAvailtoComStockholders","NetIncomeCommonStockholders","NetIncome","NetIncomeIncludingNoncontrollingInterests","NetIncomeContinuousOperations","TaxProvision","PretaxIncome","OtherIncomeExpense","OtherNonOperatingIncomeExpenses","NetNonOperatingInterestIncomeExpense","InterestExpenseNonOperating","InterestIncomeNonOperating","OperatingIncome","OperatingExpense","ResearchAndDevelopment","SellingGeneralAndAdministration","GrossProfit","CostOfRevenue","TotalRevenue","OperatingRevenue"
    )

@admin.register(BalanceSheet)
class BalanceSheetAdmin(admin.ModelAdmin):
    fields = (
        "financeInfo","TreasurySharesNumber","OrdinarySharesNumber","ShareIssued","NetDebt","TotalDebt","TangibleBookValue","InvestedCapital","WorkingCapital","NetTangibleAssets","CapitalLeaseObligations","CommonStockEquity","TotalCapitalization","TotalEquityGrossMinorityInterest","StockholdersEquity","GainsLossesNotAffectingRetainedEarnings","OtherEquityAdjustments","RetainedEarnings","CapitalStock","CommonStock","TotalLiabilitiesNetMinorityInterest","TotalNonCurrentLiabilitiesNetMinorityInterest","OtherNonCurrentLiabilities","TradeandOtherPayablesNonCurrent","LongTermDebtAndCapitalLeaseObligation","LongTermCapitalLeaseObligation","LongTermDebt","CurrentLiabilities","OtherCurrentLiabilities","CurrentDeferredLiabilities","CurrentDeferredRevenue","CurrentDebtAndCapitalLeaseObligation","CurrentCapitalLeaseObligation","CurrentDebt","OtherCurrentBorrowings","CommercialPaper","PayablesAndAccruedExpenses","Payables","TotalTaxPayable","IncomeTaxPayable","AccountsPayable","TotalAssets","TotalNonCurrentAssets","OtherNonCurrentAssets","NonCurrentDeferredAssets","NonCurrentDeferredTaxesAssets","InvestmentsAndAdvances","OtherInvestments","InvestmentinFinancialAssets","AvailableForSaleSecurities","NetPPE","AccumulatedDepreciation","GrossPPE","Leases","OtherProperties","MachineryFurnitureEquipment","LandAndImprovements","Properties","CurrentAssets","OtherCurrentAssets","Inventory","FinishedGoods","RawMaterials","Receivables","OtherReceivables","AccountsReceivable","CashCashEquivalentsAndShortTermInvestments","OtherShortTermInvestments","CashAndCashEquivalents","CashEquivalents","CashFinancial"
    )
    list_display = (
        "financeInfo","TreasurySharesNumber","OrdinarySharesNumber","ShareIssued","NetDebt","TotalDebt","TangibleBookValue","InvestedCapital","WorkingCapital","NetTangibleAssets","CapitalLeaseObligations","CommonStockEquity","TotalCapitalization","TotalEquityGrossMinorityInterest","StockholdersEquity","GainsLossesNotAffectingRetainedEarnings","OtherEquityAdjustments","RetainedEarnings","CapitalStock","CommonStock","TotalLiabilitiesNetMinorityInterest","TotalNonCurrentLiabilitiesNetMinorityInterest","OtherNonCurrentLiabilities","TradeandOtherPayablesNonCurrent","LongTermDebtAndCapitalLeaseObligation","LongTermCapitalLeaseObligation","LongTermDebt","CurrentLiabilities","OtherCurrentLiabilities","CurrentDeferredLiabilities","CurrentDeferredRevenue","CurrentDebtAndCapitalLeaseObligation","CurrentCapitalLeaseObligation","CurrentDebt","OtherCurrentBorrowings","CommercialPaper","PayablesAndAccruedExpenses","Payables","TotalTaxPayable","IncomeTaxPayable","AccountsPayable","TotalAssets","TotalNonCurrentAssets","OtherNonCurrentAssets","NonCurrentDeferredAssets","NonCurrentDeferredTaxesAssets","InvestmentsAndAdvances","OtherInvestments","InvestmentinFinancialAssets","AvailableForSaleSecurities","NetPPE","AccumulatedDepreciation","GrossPPE","Leases","OtherProperties","MachineryFurnitureEquipment","LandAndImprovements","Properties","CurrentAssets","OtherCurrentAssets","Inventory","FinishedGoods","RawMaterials","Receivables","OtherReceivables","AccountsReceivable","CashCashEquivalentsAndShortTermInvestments","OtherShortTermInvestments","CashAndCashEquivalents","CashEquivalents","CashFinancial"
    )

@admin.register(CashFlow)
class CashFlowAdmin(admin.ModelAdmin):
    fields = (
        "financeInfo","FreeCashFlow","RepurchaseOfCapitalStock","RepaymentOfDebt","IssuanceOfDebt","CapitalExpenditure","InterestPaidSupplementalData","IncomeTaxPaidSupplementalData","EndCashPosition","BeginningCashPosition","ChangesInCash","FinancingCashFlow","CashFlowFromContinuingFinancingActivities","NetOtherFinancingCharges","CashDividendsPaid","CommonStockDividendPaid","NetCommonStockIssuance","CommonStockPayments","NetIssuancePaymentsOfDebt","NetShortTermDebtIssuance","ShortTermDebtPayments","NetLongTermDebtIssuance","LongTermDebtPayments","LongTermDebtIssuance","InvestingCashFlow","CashFlowFromContinuingInvestingActivities","NetOtherInvestingChanges","NetInvestmentPurchaseAndSale","SaleOfInvestment","PurchaseOfInvestment","NetPPEPurchaseAndSale","PurchaseOfPPE","OperatingCashFlow","CashFlowFromContinuingOperatingActivities","ChangeInWorkingCapital","ChangeInOtherWorkingCapital","ChangeInOtherCurrentLiabilities","ChangeInOtherCurrentAssets","ChangeInPayablesAndAccruedExpense","ChangeInPayable","ChangeInAccountPayable","ChangeInInventory","ChangeInReceivables","ChangesInAccountReceivables","OtherNonCashItems","StockBasedCompensation","DepreciationAmortizationDepletion","DepreciationAndAmortization","NetIncomeFromContinuingOperations"
    )
    list_display = (
        "financeInfo","FreeCashFlow","RepurchaseOfCapitalStock","RepaymentOfDebt","IssuanceOfDebt","CapitalExpenditure","InterestPaidSupplementalData","IncomeTaxPaidSupplementalData","EndCashPosition","BeginningCashPosition","ChangesInCash","FinancingCashFlow","CashFlowFromContinuingFinancingActivities","NetOtherFinancingCharges","CashDividendsPaid","CommonStockDividendPaid","NetCommonStockIssuance","CommonStockPayments","NetIssuancePaymentsOfDebt","NetShortTermDebtIssuance","ShortTermDebtPayments","NetLongTermDebtIssuance","LongTermDebtPayments","LongTermDebtIssuance","InvestingCashFlow","CashFlowFromContinuingInvestingActivities","NetOtherInvestingChanges","NetInvestmentPurchaseAndSale","SaleOfInvestment","PurchaseOfInvestment","NetPPEPurchaseAndSale","PurchaseOfPPE","OperatingCashFlow","CashFlowFromContinuingOperatingActivities","ChangeInWorkingCapital","ChangeInOtherWorkingCapital","ChangeInOtherCurrentLiabilities","ChangeInOtherCurrentAssets","ChangeInPayablesAndAccruedExpense","ChangeInPayable","ChangeInAccountPayable","ChangeInInventory","ChangeInReceivables","ChangesInAccountReceivables","OtherNonCashItems","StockBasedCompensation","DepreciationAmortizationDepletion","DepreciationAndAmortization","NetIncomeFromContinuingOperations"

    )

@admin.register(Ratio)
class RatioAdmin(admin.ModelAdmin):
    fields = (
        "financeInfo","GrossProfitMargin","NetProfitMargin","DEratio","TDTAratio","Currentratio","Quickratio","Cashratio"
    )
    list_display = (
        "financeInfo","GrossProfitMargin","NetProfitMargin","DEratio","TDTAratio","Currentratio","Quickratio","Cashratio"
    )

@admin.register(FinanceData)
class FinanceDataAdmin(admin.ModelAdmin):
    fields = (
        "dataType", "dataStatus", "dataFrequency", "dataYear","datePub"
    )
    list_display = (
        "dataType", "dataStatus", "dataFrequency", "dataYear","datePub"
    )

@admin.register(overallAnalysis)
class overallAnalysisAdmin(admin.ModelAdmin):
    fields = (
        "symbol", "metric", "rank","max_rank","analysisResult", "metricDisplay"
    )
    list_display = (
        "symbol", "metric", "rank","max_rank","analysisResult", "metricDisplay"

    )

@admin.register(ValueCompanies)
class ValueCompaniesAdmin(admin.ModelAdmin):
    fields = (
        "symbol", "rank",
    )
    list_display = (
        "symbol", "rank",
    )

@admin.register(GrowthCompanies)
class GrowthCompaniesAdmin(admin.ModelAdmin):
    fields = (
        "symbol", "rank",
    )
    list_display = (
        "symbol", "rank",
    )

@admin.register(DividendCompanies)
class DividendCompaniesAdmin(admin.ModelAdmin):
    fields = (
        "symbol", "rank",
    )
    list_display = (
        "symbol", "rank",
    )
