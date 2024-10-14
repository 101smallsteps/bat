# Generated by Django 4.2 on 2024-10-11 23:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FinanceData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataType', models.CharField(choices=[('Q', 'Quarterly'), ('A', 'Annual')], max_length=1)),
                ('dataStatus', models.CharField(choices=[('CREATE', 'Work Created'), ('START', 'Work Started'), ('DONE', 'Work Done'), ('VERIFY', 'Work Verification In Progress'), ('APPR', 'Work APPROVED')], max_length=6)),
                ('dataFrequency', models.CharField(choices=[('Q_1', 'Q_1'), ('Q_2', 'Q_2'), ('Q_3', 'Q_3'), ('Q_4', 'Q_4'), ('A', 'Annual')], max_length=6)),
                ('dataYear', models.IntegerField(choices=[(1950, 1950), (1951, 1951), (1952, 1952), (1953, 1953), (1954, 1954), (1955, 1955), (1956, 1956), (1957, 1957), (1958, 1958), (1959, 1959), (1960, 1960), (1961, 1961), (1962, 1962), (1963, 1963), (1964, 1964), (1965, 1965), (1966, 1966), (1967, 1967), (1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024)], default=2024, verbose_name='year')),
                ('datePub', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Symbol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbolName', models.CharField(max_length=255)),
                ('companyName', models.CharField(max_length=255)),
                ('sector', models.CharField(choices=[('CSE', 'ConsumerElectronics'), ('ROB', 'ROBOTICS'), ('SEMI', 'Semiconductor'), ('SEMIDESIGN', 'SemiconductorDesign'), ('SEMIFAB', 'SemiconductorFab'), ('CTRAN', 'ConsumerTransportation')], max_length=50)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ValueCompanies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField()),
                ('symbol', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vc_symbol', to='financials.symbol')),
            ],
        ),
        migrations.CreateModel(
            name='SymbolAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AnalysisStatus', models.CharField(choices=[('VGOOD', 'vgood'), ('GOOD', 'good'), ('BAD', 'bad'), ('OK', 'ok')], max_length=6)),
                ('rank', models.IntegerField(default=0.0)),
                ('max_rank', models.IntegerField(default=0.0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('symbol', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='symbols_all', to='financials.symbol')),
            ],
        ),
        migrations.CreateModel(
            name='Ratio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GrossProfitMargin', models.FloatField(default=0.0, null=True)),
                ('NetProfitMargin', models.FloatField(default=0.0, null=True)),
                ('DEratio', models.FloatField(default=0.0, null=True)),
                ('TDTAratio', models.FloatField(default=0.0, null=True)),
                ('Currentratio', models.FloatField(default=0.0, null=True)),
                ('Quickratio', models.FloatField(default=0.0, null=True)),
                ('Cashratio', models.FloatField(default=0.0, null=True)),
                ('financeInfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financials.financedata')),
                ('symbol', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='financials.symbol')),
            ],
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='portfolio_owner', to=settings.AUTH_USER_MODEL)),
                ('symbol', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_symbol', to='financials.symbol')),
            ],
        ),
        migrations.CreateModel(
            name='overallAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metric', models.CharField(choices=[('Cashratio', 'Cashratio'), ('Quickratio', 'Quickratio'), ('Currentratio', 'Currentratio'), ('TDTAratio', 'TDTAratio'), ('DEratio', 'DEratio'), ('NetProfitMargin', 'NetProfitMargin'), ('GrossProfitMargin', 'GrossProfitMargin'), ('RevenueGrowthConsecutive', 'RevenueGrowthConsecutive'), ('RevenueVsCoR', 'RevenueVsCoR'), ('Revenue', 'Revenue')], max_length=40)),
                ('rank', models.IntegerField(default=0.0)),
                ('max_rank', models.IntegerField(default=0.0)),
                ('analysisResult', models.CharField(choices=[('VGOOD', 'verygood'), ('GOOD', 'good'), ('BAD', 'bad'), ('OK', 'ok'), ('NAVL', 'navl')], default='NAVL', max_length=6)),
                ('metricDisplay', models.CharField(max_length=36)),
                ('symbol', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='symbols_all_overall', to='financials.symbol')),
            ],
        ),
        migrations.CreateModel(
            name='IncomeStatement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TaxEffectOfUnusualItems', models.FloatField(default=0.0, null=True)),
                ('TaxRateForCalcs', models.FloatField(default=0.0, null=True)),
                ('NormalizedEBITDA', models.FloatField(default=0.0, null=True)),
                ('NetIncomeFromContinuingOperationNetMinorityInterest', models.FloatField(default=0.0, null=True)),
                ('ReconciledDepreciation', models.FloatField(default=0.0, null=True)),
                ('ReconciledCostOfRevenue', models.FloatField(default=0.0, null=True)),
                ('EBITDA', models.FloatField(default=0.0, null=True)),
                ('EBIT', models.FloatField(default=0.0, null=True)),
                ('NetInterestIncome', models.FloatField(default=0.0, null=True)),
                ('InterestExpense', models.FloatField(default=0.0, null=True)),
                ('InterestIncome', models.FloatField(default=0.0, null=True)),
                ('NormalizedIncome', models.FloatField(default=0.0, null=True)),
                ('NetIncomeFromContinuingAndDiscontinuedOperation', models.FloatField(default=0.0, null=True)),
                ('TotalExpenses', models.FloatField(default=0.0, null=True)),
                ('TotalOperatingIncomeAsReported', models.FloatField(default=0.0, null=True)),
                ('DilutedAverageShares', models.FloatField(default=0.0, null=True)),
                ('BasicAverageShares', models.FloatField(default=0.0, null=True)),
                ('DilutedEPS', models.FloatField(default=0.0, null=True)),
                ('BasicEPS', models.FloatField(default=0.0, null=True)),
                ('DilutedNIAvailtoComStockholders', models.FloatField(default=0.0, null=True)),
                ('NetIncomeCommonStockholders', models.FloatField(default=0.0, null=True)),
                ('NetIncome', models.FloatField(default=0.0, null=True)),
                ('NetIncomeIncludingNoncontrollingInterests', models.FloatField(default=0.0, null=True)),
                ('NetIncomeContinuousOperations', models.FloatField(default=0.0, null=True)),
                ('TaxProvision', models.FloatField(default=0.0, null=True)),
                ('PretaxIncome', models.FloatField(default=0.0, null=True)),
                ('OtherIncomeExpense', models.FloatField(default=0.0, null=True)),
                ('OtherNonOperatingIncomeExpenses', models.FloatField(default=0.0, null=True)),
                ('NetNonOperatingInterestIncomeExpense', models.FloatField(default=0.0, null=True)),
                ('InterestExpenseNonOperating', models.FloatField(default=0.0, null=True)),
                ('InterestIncomeNonOperating', models.FloatField(default=0.0, null=True)),
                ('OperatingIncome', models.FloatField(default=0.0, null=True)),
                ('OperatingExpense', models.FloatField(default=0.0, null=True)),
                ('ResearchAndDevelopment', models.FloatField(default=0.0, null=True)),
                ('SellingGeneralAndAdministration', models.FloatField(default=0.0, null=True)),
                ('GrossProfit', models.FloatField(default=0.0, null=True)),
                ('CostOfRevenue', models.FloatField(default=0.0, null=True)),
                ('TotalRevenue', models.FloatField(default=0.0, null=True)),
                ('OperatingRevenue', models.FloatField(default=0.0, null=True)),
                ('financeInfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financials.financedata')),
                ('symbol', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='financials.symbol')),
            ],
        ),
        migrations.CreateModel(
            name='GrowthCompanies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField()),
                ('symbol', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gc_symbol', to='financials.symbol')),
            ],
        ),
        migrations.CreateModel(
            name='DividendCompanies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField()),
                ('symbol', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dc_symbol', to='financials.symbol')),
            ],
        ),
        migrations.CreateModel(
            name='CashFlow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FreeCashFlow', models.FloatField(default=0.0, null=True)),
                ('RepurchaseOfCapitalStock', models.FloatField(default=0.0, null=True)),
                ('RepaymentOfDebt', models.FloatField(default=0.0, null=True)),
                ('IssuanceOfDebt', models.FloatField(default=0.0, null=True)),
                ('CapitalExpenditure', models.FloatField(default=0.0, null=True)),
                ('InterestPaidSupplementalData', models.FloatField(default=0.0, null=True)),
                ('IncomeTaxPaidSupplementalData', models.FloatField(default=0.0, null=True)),
                ('EndCashPosition', models.FloatField(default=0.0, null=True)),
                ('BeginningCashPosition', models.FloatField(default=0.0, null=True)),
                ('ChangesInCash', models.FloatField(default=0.0, null=True)),
                ('FinancingCashFlow', models.FloatField(default=0.0, null=True)),
                ('CashFlowFromContinuingFinancingActivities', models.FloatField(default=0.0, null=True)),
                ('NetOtherFinancingCharges', models.FloatField(default=0.0, null=True)),
                ('CashDividendsPaid', models.FloatField(default=0.0, null=True)),
                ('CommonStockDividendPaid', models.FloatField(default=0.0, null=True)),
                ('NetCommonStockIssuance', models.FloatField(default=0.0, null=True)),
                ('CommonStockPayments', models.FloatField(default=0.0, null=True)),
                ('NetIssuancePaymentsOfDebt', models.FloatField(default=0.0, null=True)),
                ('NetShortTermDebtIssuance', models.FloatField(default=0.0, null=True)),
                ('ShortTermDebtPayments', models.FloatField(default=0.0, null=True)),
                ('NetLongTermDebtIssuance', models.FloatField(default=0.0, null=True)),
                ('LongTermDebtPayments', models.FloatField(default=0.0, null=True)),
                ('LongTermDebtIssuance', models.FloatField(default=0.0, null=True)),
                ('InvestingCashFlow', models.FloatField(default=0.0, null=True)),
                ('CashFlowFromContinuingInvestingActivities', models.FloatField(default=0.0, null=True)),
                ('NetOtherInvestingChanges', models.FloatField(default=0.0, null=True)),
                ('NetInvestmentPurchaseAndSale', models.FloatField(default=0.0, null=True)),
                ('SaleOfInvestment', models.FloatField(default=0.0, null=True)),
                ('PurchaseOfInvestment', models.FloatField(default=0.0, null=True)),
                ('NetPPEPurchaseAndSale', models.FloatField(default=0.0, null=True)),
                ('PurchaseOfPPE', models.FloatField(default=0.0, null=True)),
                ('OperatingCashFlow', models.FloatField(default=0.0, null=True)),
                ('CashFlowFromContinuingOperatingActivities', models.FloatField(default=0.0, null=True)),
                ('ChangeInWorkingCapital', models.FloatField(default=0.0, null=True)),
                ('ChangeInOtherWorkingCapital', models.FloatField(default=0.0, null=True)),
                ('ChangeInOtherCurrentLiabilities', models.FloatField(default=0.0, null=True)),
                ('ChangeInOtherCurrentAssets', models.FloatField(default=0.0, null=True)),
                ('ChangeInPayablesAndAccruedExpense', models.FloatField(default=0.0, null=True)),
                ('ChangeInPayable', models.FloatField(default=0.0, null=True)),
                ('ChangeInAccountPayable', models.FloatField(default=0.0, null=True)),
                ('ChangeInInventory', models.FloatField(default=0.0, null=True)),
                ('ChangeInReceivables', models.FloatField(default=0.0, null=True)),
                ('ChangesInAccountReceivables', models.FloatField(default=0.0, null=True)),
                ('OtherNonCashItems', models.FloatField(default=0.0, null=True)),
                ('StockBasedCompensation', models.FloatField(default=0.0, null=True)),
                ('DepreciationAmortizationDepletion', models.FloatField(default=0.0, null=True)),
                ('DepreciationAndAmortization', models.FloatField(default=0.0, null=True)),
                ('NetIncomeFromContinuingOperations', models.FloatField(default=0.0, null=True)),
                ('financeInfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financials.financedata')),
                ('symbol', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='financials.symbol')),
            ],
        ),
        migrations.CreateModel(
            name='BalanceSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TreasurySharesNumber', models.FloatField(default=0.0, null=True)),
                ('OrdinarySharesNumber', models.FloatField(default=0.0, null=True)),
                ('ShareIssued', models.FloatField(default=0.0, null=True)),
                ('NetDebt', models.FloatField(default=0.0, null=True)),
                ('TotalDebt', models.FloatField(default=0.0, null=True)),
                ('TangibleBookValue', models.FloatField(default=0.0, null=True)),
                ('InvestedCapital', models.FloatField(default=0.0, null=True)),
                ('WorkingCapital', models.FloatField(default=0.0, null=True)),
                ('NetTangibleAssets', models.FloatField(default=0.0, null=True)),
                ('CapitalLeaseObligations', models.FloatField(default=0.0, null=True)),
                ('CommonStockEquity', models.FloatField(default=0.0, null=True)),
                ('TotalCapitalization', models.FloatField(default=0.0, null=True)),
                ('TotalEquityGrossMinorityInterest', models.FloatField(default=0.0, null=True)),
                ('StockholdersEquity', models.FloatField(default=0.0, null=True)),
                ('GainsLossesNotAffectingRetainedEarnings', models.FloatField(default=0.0, null=True)),
                ('OtherEquityAdjustments', models.FloatField(default=0.0, null=True)),
                ('RetainedEarnings', models.FloatField(default=0.0, null=True)),
                ('CapitalStock', models.FloatField(default=0.0, null=True)),
                ('CommonStock', models.FloatField(default=0.0, null=True)),
                ('TotalLiabilitiesNetMinorityInterest', models.FloatField(default=0.0, null=True)),
                ('TotalNonCurrentLiabilitiesNetMinorityInterest', models.FloatField(default=0.0, null=True)),
                ('OtherNonCurrentLiabilities', models.FloatField(default=0.0, null=True)),
                ('TradeandOtherPayablesNonCurrent', models.FloatField(default=0.0, null=True)),
                ('LongTermDebtAndCapitalLeaseObligation', models.FloatField(default=0.0, null=True)),
                ('LongTermCapitalLeaseObligation', models.FloatField(default=0.0, null=True)),
                ('LongTermDebt', models.FloatField(default=0.0, null=True)),
                ('CurrentLiabilities', models.FloatField(default=0.0, null=True)),
                ('OtherCurrentLiabilities', models.FloatField(default=0.0, null=True)),
                ('CurrentDeferredLiabilities', models.FloatField(default=0.0, null=True)),
                ('CurrentDeferredRevenue', models.FloatField(default=0.0, null=True)),
                ('CurrentDebtAndCapitalLeaseObligation', models.FloatField(default=0.0, null=True)),
                ('CurrentCapitalLeaseObligation', models.FloatField(default=0.0, null=True)),
                ('CurrentDebt', models.FloatField(default=0.0, null=True)),
                ('OtherCurrentBorrowings', models.FloatField(default=0.0, null=True)),
                ('CommercialPaper', models.FloatField(default=0.0, null=True)),
                ('PayablesAndAccruedExpenses', models.FloatField(default=0.0, null=True)),
                ('Payables', models.FloatField(default=0.0, null=True)),
                ('TotalTaxPayable', models.FloatField(default=0.0, null=True)),
                ('IncomeTaxPayable', models.FloatField(default=0.0, null=True)),
                ('AccountsPayable', models.FloatField(default=0.0, null=True)),
                ('TotalAssets', models.FloatField(default=0.0, null=True)),
                ('TotalNonCurrentAssets', models.FloatField(default=0.0, null=True)),
                ('OtherNonCurrentAssets', models.FloatField(default=0.0, null=True)),
                ('NonCurrentDeferredAssets', models.FloatField(default=0.0, null=True)),
                ('NonCurrentDeferredTaxesAssets', models.FloatField(default=0.0, null=True)),
                ('InvestmentsAndAdvances', models.FloatField(default=0.0, null=True)),
                ('OtherInvestments', models.FloatField(default=0.0, null=True)),
                ('InvestmentinFinancialAssets', models.FloatField(default=0.0, null=True)),
                ('AvailableForSaleSecurities', models.FloatField(default=0.0, null=True)),
                ('NetPPE', models.FloatField(default=0.0, null=True)),
                ('AccumulatedDepreciation', models.FloatField(default=0.0, null=True)),
                ('GrossPPE', models.FloatField(default=0.0, null=True)),
                ('Leases', models.FloatField(default=0.0, null=True)),
                ('OtherProperties', models.FloatField(default=0.0, null=True)),
                ('MachineryFurnitureEquipment', models.FloatField(default=0.0, null=True)),
                ('LandAndImprovements', models.FloatField(default=0.0, null=True)),
                ('Properties', models.FloatField(default=0.0, null=True)),
                ('CurrentAssets', models.FloatField(default=0.0, null=True)),
                ('OtherCurrentAssets', models.FloatField(default=0.0, null=True)),
                ('Inventory', models.FloatField(default=0.0, null=True)),
                ('FinishedGoods', models.FloatField(default=0.0, null=True)),
                ('RawMaterials', models.FloatField(default=0.0, null=True)),
                ('Receivables', models.FloatField(default=0.0, null=True)),
                ('OtherReceivables', models.FloatField(default=0.0, null=True)),
                ('AccountsReceivable', models.FloatField(default=0.0, null=True)),
                ('CashCashEquivalentsAndShortTermInvestments', models.FloatField(default=0.0, null=True)),
                ('OtherShortTermInvestments', models.FloatField(default=0.0, null=True)),
                ('CashAndCashEquivalents', models.FloatField(default=0.0, null=True)),
                ('CashEquivalents', models.FloatField(default=0.0, null=True)),
                ('CashFinancial', models.FloatField(default=0.0, null=True)),
                ('financeInfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financials.financedata')),
                ('symbol', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='financials.symbol')),
            ],
        ),
    ]
