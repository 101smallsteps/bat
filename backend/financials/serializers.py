from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Symbol, SymbolAnalysis, Portfolio,overallAnalysis,FinanceData,IncomeStatement,\
    Ratio,ValueCompanies,GrowthCompanies,DividendCompanies
from django.shortcuts import get_object_or_404



class SymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symbol
        fields = ['id', 'symbolName','companyName','created_date', 'updated_date']
        read_only_fields = ('id', 'created_date', 'updated_date',)



class SymbolAnalysisSerializer(serializers.ModelSerializer):
    symbol = SymbolSerializer()
    class Meta:
        model = SymbolAnalysis
        fields = ('id', 'symbol','AnalysisStatus','created_date', 'updated_date',)
        read_only_fields = ('id', 'created_date', 'updated_date',)

#https://testdriven.io/blog/drf-serializers/#serializer-save
#https://www.django-rest-framework.org/api-guide/relations/#nested-relationships
#django code to get nested with related_name read and write
class PortfolioReadSerializer(serializers.ModelSerializer):
    user_symbol = SymbolSerializer(many=True, read_only=True)
    symbol = SymbolSerializer(many=True, required=False)

    class Meta:
        model = Portfolio
        fields =['owner','symbol','user_symbol']

    def to_representation(self, obj):
        print("entering to_representation")
        print(obj)
        self.fields['symbol'] = SymbolSerializer()
        #self.fields['user_symbol'] = obj.symbol
        return super(PortfolioReadSerializer, self).to_representation(obj)


class PortfolioWriteSerializer(serializers.ModelSerializer):
    user_symbol = SymbolSerializer(many=True, required=False)
    class Meta:
        model = Portfolio
        fields =['owner','user_symbol']


    def to_representation(self, obj):
        print("entering to_representation")
        print(obj)
        self.fields['symbol'] = SymbolSerializer()
        #self.fields['user_symbol'] = obj.symbol
        return super(PortfolioWriteSerializer, self).to_representation(obj)

    def create(self, validated_data):
        user_symbol_data=validated_data.pop('user_symbol')
        print(user_symbol_data)
        try:
            port_item = Portfolio.objects.create(**validated_data)
            for sym in user_symbol_data:
                sym_1 = get_object_or_404(Symbol, symbolName=sym['symbolName'])
                port_item.symbol=sym_1
                port_item.save()
        except Symbol.DoesNotExist:
            pass
        return port_item

class overallAnalysisReadSerializer(serializers.ModelSerializer):
    symbols_all_overall = SymbolSerializer(many=True, read_only=True)
    symbol = SymbolSerializer(many=True, required=False)

    class Meta:
        model = overallAnalysis
        fields =['metric','analysisResult','metricDisplay','symbol','symbols_all_overall']

    def to_representation(self, obj):
        print("entering to_representation")
        print(obj)
        self.fields['symbol'] = SymbolSerializer()
        #self.fields['user_symbol'] = obj.symbol
        return super(overallAnalysisReadSerializer, self).to_representation(obj)


#class UserSerializer(serializers.HyperlinkedModelSerializer):
#    portfolio = serializers.HyperlinkedRelatedField(
#        many=True, view_name="portfolio-detail",read_only=True)
#    class Meta:
#        model = User
#        fields = [ 'username', 'portfolio']

class FinanceDataReadSerializer(serializers.ModelSerializer):
    findata_symbol = SymbolSerializer(many=True, read_only=True)
    symbol = SymbolSerializer(many=True, required=False)

    class Meta:
        model = FinanceData
        fields =['symbol','findata_symbol','dataType','dataStatus','dataFrequency','dataYear']

    def to_representation(self, obj):
        print("entering to_representation")
        print(obj)
        self.fields['symbol'] = SymbolSerializer()
        #self.fields['user_symbol'] = obj.symbol
        return super(FinanceDataReadSerializer, self).to_representation(obj)


class FinanceDataWriteSerializer(serializers.ModelSerializer):
    user_symbol = SymbolSerializer(many=True, required=False)
    class Meta:
        model = Portfolio
        fields =['owner','user_symbol']


    def to_representation(self, obj):
        print("entering to_representation")
        print(obj)
        self.fields['symbol'] = SymbolSerializer()
        #self.fields['user_symbol'] = obj.symbol
        return super(PortfolioWriteSerializer, self).to_representation(obj)

    def create(self, validated_data):
        user_symbol_data=validated_data.pop('user_symbol')
        print(user_symbol_data)
        try:
            port_item = Portfolio.objects.create(**validated_data)
            for sym in user_symbol_data:
                sym_1 = get_object_or_404(Symbol, symbolName=sym['symbolName'])
                port_item.symbol=sym_1
                port_item.save()
        except Symbol.DoesNotExist:
            pass
        return port_item

class IncomeStatementReadSerializer(serializers.ModelSerializer):
    income_financeInfo = FinanceDataReadSerializer(many=True, read_only=True)
    financeInfo = FinanceDataReadSerializer(many=True, required=False)

    class Meta:
        model = IncomeStatement
        fields =['financeInfo','income_financeInfo','totalRevenue','totalRevenue_operatingRevenue']

    def to_representation(self, obj):
        print("entering to_representation")
        print(obj)
        self.fields['financeInfo'] = FinanceDataReadSerializer()
        #self.fields['user_symbol'] = obj.symbol
        return super(IncomeStatementReadSerializer, self).to_representation(obj)

class RatioReadSerializer(serializers.ModelSerializer):
    ratios_financeInfo = FinanceDataReadSerializer(many=True, read_only=True)
    financeInfo = FinanceDataReadSerializer(many=True, required=False)

    class Meta:
        model = Ratio
        fields =['financeInfo','DEratio']

    def to_representation(self, obj):
        print("entering to_representation")
        print(obj)
        self.fields['financeInfo'] = FinanceDataReadSerializer()
        #self.fields['user_symbol'] = obj.symbol
        return super(RatioReadSerializer, self).to_representation(obj)

class ValueCompaniesReadSerializer(serializers.ModelSerializer):
    vc_symbol = SymbolSerializer(many=True, read_only=True)
    symbol = SymbolSerializer(many=True, required=False)

    class Meta:
        model = ValueCompanies
        fields =['symbol','vc_symbol','rank']

    def to_representation(self, obj):
        print("entering to_representation")
        print(obj)
        self.fields['symbol'] = SymbolSerializer()
        #self.fields['user_symbol'] = obj.symbol
        return super(ValueCompaniesReadSerializer, self).to_representation(obj)

class GrowthCompaniesReadSerializer(serializers.ModelSerializer):
    gc_symbol = SymbolSerializer(many=True, read_only=True)
    symbol = SymbolSerializer(many=True, required=False)

    class Meta:
        model = GrowthCompanies
        fields =['symbol','gc_symbol','rank']

    def to_representation(self, obj):
        print("entering to_representation")
        print(obj)
        self.fields['symbol'] = SymbolSerializer()
        #self.fields['user_symbol'] = obj.symbol
        return super(GrowthCompaniesReadSerializer, self).to_representation(obj)

class DividendCompaniesReadSerializer(serializers.ModelSerializer):
    dc_symbol = SymbolSerializer(many=True, read_only=True)
    symbol = SymbolSerializer(many=True, required=False)

    class Meta:
        model = DividendCompanies
        fields =['symbol','dc_symbol','rank']

    def to_representation(self, obj):
        print("entering to_representation")
        print(obj)
        self.fields['symbol'] = SymbolSerializer()
        #self.fields['user_symbol'] = obj.symbol
        return super(DividendCompaniesReadSerializer, self).to_representation(obj)
