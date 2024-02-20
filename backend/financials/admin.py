from django.contrib import admin

# Register your models here.
from .models import Symbol, SymbolAnalysis, Portfolio, overallAnalysis, IncomeStatement, FinanceData, Ratio,\
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
        "financeInfo", "TotalRevenue", "OperatingRevenue"
    )
    list_display = (
        "financeInfo", "TotalRevenue", "OperatingRevenue"
    )

@admin.register(Ratio)
class RatioAdmin(admin.ModelAdmin):
    fields = (
        "financeInfo","GrossMargin", "DEratio"
    )
    list_display = (
        "financeInfo","GrossMargin", "DEratio"
    )

@admin.register(FinanceData)
class FinanceDataAdmin(admin.ModelAdmin):
    fields = (
        "dataType", "dataStatus", "symbol", "dataFrequency", "dataYear","datePub"
    )
    list_display = (
        "dataType", "dataStatus", "symbol", "dataFrequency", "dataYear","datePub"
    )

@admin.register(overallAnalysis)
class overallAnalysisAdmin(admin.ModelAdmin):
    fields = (
        "symbol", "metric", "analysisResult", "metricDisplay",
    )
    list_display = (
        "symbol", "metric", "analysisResult", "metricDisplay",
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
