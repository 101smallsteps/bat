from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required

from .models import SymbolAnalysis, Portfolio, Symbol, overallAnalysis, IncomeStatement, FinanceData, Ratio,\
    ValueCompanies,GrowthCompanies,DividendCompanies
from django.contrib.auth.models import User
from rest_framework import  renderers, viewsets
from rest_framework.decorators import action
from rest_framework import generics, permissions

from .serializers import SymbolAnalysisSerializer,PortfolioWriteSerializer,PortfolioReadSerializer, SymbolSerializer,\
    overallAnalysisReadSerializer,FinanceDataReadSerializer,IncomeStatementReadSerializer,\
ValueCompaniesReadSerializer,GrowthCompaniesReadSerializer,DividendCompaniesReadSerializer
import json
from rest_framework import mixins
from rest_framework import generics
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from django.shortcuts import get_object_or_404

@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "users": reverse("user-list", request=request, format=format),
            "portfolio": reverse("portfolio-list", request=request, format=format),
        }
    )

class SymbolList(APIView):
    http_method_names = ['get', 'head']
    permission_classes = (permissions.IsAuthenticated,)


    def post(self, request, format=None):
        serializer = SymbolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, format=None):
        symbols = Symbol.objects.all()
        serializer = SymbolSerializer(symbols,many=True)
        return Response(serializer.data)



class SymbolAnalysisList(APIView):
    http_method_names = ['get', 'head']
    permission_classes = (permissions.IsAuthenticated,)


    def post(self, request, format=None):
        serializer = SymbolAnalysisSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, format=None):
        symbol_analysis = SymbolAnalysis.objects.all()
        serializer = SymbolAnalysisSerializer(symbol_analysis,many=True)
        return Response(serializer.data)

class PortfolioList(APIView):
    http_method_names = ['get','post','head','delete']
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        portfolio = Portfolio.objects.filter(owner=request.user.id)
        serializer = PortfolioReadSerializer(portfolio, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def delete(self, request, pk,format=None):
        port_iem=Portfolio.objects.filter(owner=request.user.id,symbol=pk)
        port_iem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    def post(self, request, *args, **kwargs):
        data = {
            'user_symbol': request.data.get('user_symbol'),
            'owner': request.user.id
        }
        serializer = PortfolioWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response("", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FinanceDataList(APIView):
    http_method_names = ['get','post','head','delete']
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request,datatype,datafrequency,year,id, format=None):
        print("I am in get "+datatype+" "+datafrequency+" "+str(year)+" "+str(id))
        #dataType=datatype,dataFrequency=datafrequency,dataYear=year,
        #fData = FinanceData.objects.filter(symbol=id)[:5]
        fData = FinanceData.objects.filter(dataType=datatype,dataFrequency=datafrequency,dataYear=year,symbol=id)[:5]
        serializer = FinanceDataReadSerializer(fData, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def delete(self, request, pk,format=None):
        fin_item=FinanceData.objects.filter(owner=request.user.id,symbol=pk)
        fin_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    def post(self, request, *args, **kwargs):
        data = {
            'user_symbol': request.data.get('user_symbol'),
            'owner': request.user.id
        }
        serializer = FinanceDataWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response("", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IncomeStatementList(APIView):
    http_method_names = ['get','post','head','delete']
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request,metricname , id,n, format=None):
        for field in IncomeStatement._meta.get_fields():
            print(field.name)
        if metricname not in [field.name for field in IncomeStatement._meta.get_fields()]:
            return Response({'error': 'Invalid field name'}, status=400)

        data = IncomeStatement.objects.filter(symbol=id).order_by('-financeInfo__datePub').values_list(metricname,'financeInfo__dataFrequency','financeInfo__dataYear')[:int(n)]
        print(data)
        #serializer = IncomeStatementReadSerializer(data, many=True)
        #return Response(serializer.data,status=status.HTTP_200_OK)
        incstmt_list_of_dicts = [{'metricValue':metricname,'dataFrequency':dataFrequency,'dataYear':dataYear } for metricname,dataFrequency,dataYear in data]

        if (len(incstmt_list_of_dicts)>1):
            data_final={
                 'last_metric_value':incstmt_list_of_dicts[0]['metricValue']/1000000,
                 'percentChange':round(((incstmt_list_of_dicts[0]['metricValue'] - incstmt_list_of_dicts[1]['metricValue'])/incstmt_list_of_dicts[1]['metricValue'])*100,2),
                 'chartData':incstmt_list_of_dicts

            }
        elif (len(incstmt_list_of_dicts)>0):
            data_final = {
                'last_metric_value': incstmt_list_of_dicts[0]['metricValue'],
                'percentChange': 0,
                'chartData': incstmt_list_of_dicts

            }
        else:
            data_final = {
                'last_metric_value': 0,
                'percentChange': 0,
                'chartData': []

            }
        return Response([data_final],status=status.HTTP_200_OK)

    def delete(self, request, pk,format=None):
        port_iem=Portfolio.objects.filter(owner=request.user.id,symbol=pk)
        port_iem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    def post(self, request, *args, **kwargs):
        data = {
            'user_symbol': request.data.get('user_symbol'),
            'owner': request.user.id
        }
        serializer = PortfolioWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response("", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RatioList(APIView):
    http_method_names = ['get','post','head','delete']
    permission_classes = [permissions.IsAuthenticated]

    def get_old(self, request,rationame , id,n, format=None):

        if rationame not in [field.name for field in Ratio._meta.get_fields()]:
            return Response({'error': 'Invalid field name'}, status=400)

        data = Ratio.objects.filter(financeInfo__symbol=id).values_list(rationame, flat=True)[:int(n)]
        #print(data)
        #serializer = IncomeStatementReadSerializer(data, many=True)
        #return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(data,status=status.HTTP_200_OK)

    def get(self, request,rationame , id,n, format=None):
        for field in Ratio._meta.get_fields():
            print(field.name)
        if rationame not in [field.name for field in Ratio._meta.get_fields()]:
            return Response({'error': 'Invalid field name'}, status=400)

        data = Ratio.objects.filter(symbol=id).order_by('-financeInfo__datePub').values_list(rationame,'financeInfo__dataFrequency','financeInfo__dataYear')[:int(n)]
        print(data)
        #serializer = IncomeStatementReadSerializer(data, many=True)
        #return Response(serializer.data,status=status.HTTP_200_OK)
        ratio_list_of_dicts = [{'metricValue':rationame,'dataFrequency':dataFrequency,'dataYear':dataYear } for rationame,dataFrequency,dataYear in data]

        if (len(ratio_list_of_dicts)>1):
            data_final={
                 'last_metric_value':ratio_list_of_dicts[0]['metricValue'],
                 'percentChange':round(((ratio_list_of_dicts[0]['metricValue'] - ratio_list_of_dicts[1]['metricValue'])/ratio_list_of_dicts[1]['metricValue'])*100,2),
                 'chartData':ratio_list_of_dicts

            }
        elif (len(ratio_list_of_dicts)>0):
            data_final = {
                'last_metric_value': ratio_list_of_dicts[0]['metricValue'],
                'percentChange': 0,
                'chartData': ratio_list_of_dicts

            }
        else:
            data_final = {
                'last_metric_value': 0,
                'percentChange': 0,
                'chartData': []

            }
        return Response([data_final],status=status.HTTP_200_OK)


    def delete(self, request, pk,format=None):
        port_iem=Portfolio.objects.filter(owner=request.user.id,symbol=pk)
        port_iem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    def post(self, request, *args, **kwargs):
        data = {
            'user_symbol': request.data.get('user_symbol'),
            'owner': request.user.id
        }
        serializer = PortfolioWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response("", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PortfolioList_old(generics.ListCreateAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioReadSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):  # new
        serializer.save(owner=self.request.user)

class PortfolioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioReadSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )

class overallAnalysisDet(APIView):
    http_method_names = ['get','post','head','delete']
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk,format=None):
        obj = overallAnalysis.objects.filter(symbol=pk)
        serializer = overallAnalysisReadSerializer(obj, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

#class UserList(generics.ListAPIView):  # new
#    queryset = User.objects.all()
#    serializer_class = UserSerializer
#
#
#class UserDetail(generics.RetrieveAPIView):  # new
#    queryset = User.objects.all()
#    serializer_class = UserSerializer

class ValueCompanisList(APIView):
    http_method_namees = ['get']
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, n,format=None):
        obj = ValueCompanies.objects.all().order_by('rank')[:int(n)]
        serializer = ValueCompaniesReadSerializer(obj, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class GrowthCompaniesList(APIView):
    http_method_namees = ['get']
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, n,format=None):
        obj = GrowthCompanies.objects.all().order_by('rank')[:int(n)]
        serializer = GrowthCompaniesReadSerializer(obj, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class DividendCompaniesList(APIView):
    http_method_namees = ['get']
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, n,format=None):
        obj = DividendCompanies.objects.all().order_by('rank')[:int(n)]
        serializer = DividendCompaniesReadSerializer(obj, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)