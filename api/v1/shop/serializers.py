from drf_yasg import openapifrom rest_framework import serializersclass FilterDateSerializer(serializers.Serializer):    month = serializers.IntegerField()    year = serializers.IntegerField()    def validate_month(self, value):        if not 13 > value > 0:            raise serializers.ValidationError("Invalid month")        return valueclass ResponseEmployeesStatisticsSerializer(serializers.Serializer):    id = serializers.IntegerField()    fullname = serializers.CharField()    unique_clients = serializers.IntegerField()    clients = serializers.IntegerField()    products_count = serializers.IntegerField()    prices_sum = serializers.IntegerField()class ResponseEmployeeStatisticsWithPk(serializers.Serializer):    employee_name = serializers.CharField()    clients_count = serializers.IntegerField()    unique_client = serializers.IntegerField()    prices_sum = serializers.IntegerField()    products_count = serializers.IntegerField()class ResponseClientStatisticsSerializer(serializers.Serializer):    id = serializers.IntegerField()    fullname = serializers.CharField()    products_count = serializers.IntegerField()    prices_sum = serializers.IntegerField()date_params = [    openapi.Parameter(        name='month',        in_=openapi.IN_QUERY,        type=openapi.TYPE_INTEGER,        description='месяц',        required=True    ),    openapi.Parameter(        name='year',        in_=openapi.IN_QUERY,        type=openapi.TYPE_INTEGER,        description='год',        required=True    )]