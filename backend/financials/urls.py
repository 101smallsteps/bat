from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from .views import SymbolAnalysisList, PortfolioList, SymbolList, overallAnalysisDet,FinanceDataList,\
    IncomeStatementList, RatioList,ValueCompanisList,GrowthCompaniesList,DividendCompaniesList
from rest_framework.urlpatterns import format_suffix_patterns
from financials import views


# Create a router and register our viewsets with it.
#router = DefaultRouter()
#router.register(r'folio', PortfolioList,basename='portfolio')

urlpatterns = [
    path("api/symanalysis/", SymbolAnalysisList.as_view(),name="symanaly"),
    path("api/symbols/",SymbolList.as_view(),name="syms"),
    path("api/portfolio/", PortfolioList.as_view(),name="portfolio-list"),
    path("api/portfolio/<int:pk>/", PortfolioList.as_view(),name="portfolio-detail"),
    path("api/overall/<int:pk>/",overallAnalysisDet.as_view(),name="overallAnaly-detail"),
    path("api/findata/<str:datatype>/<str:datafrequency>/<int:year>/<int:id>/",FinanceDataList.as_view(),name="findata-detail"),
    path("api/incstmt/<str:metricname>/<int:id>/<int:n>/",IncomeStatementList.as_view(),name="income-detail"),
    path("api/ratio/<str:rationame>/<int:id>/<int:n>/",RatioList.as_view(),name="ratio-detail"),
    path("api/rankvc/<int:n>/",ValueCompanisList.as_view(),name="rvc-detail"),
    path("api/rankgc/<int:n>/",GrowthCompaniesList.as_view(),name="rgc-detail"),
    path("api/rankdc/<int:n>/",DividendCompaniesList.as_view(),name="rdc-detail"),
    path("", views.api_root),
]

urlpatterns = format_suffix_patterns(urlpatterns)


