from django.db.models import Sum, Count
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.v1.shop.serializers import ResponseEmployeesStatisticsSerializer, FilterDateSerializer
from apps.shop.models import *


@swagger_auto_schema(tags=['statistics'], method='get', manual_parameters=[
    openapi.Parameter(
        name='month',
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_INTEGER,
        description='месяц',
        required=True
    ),
    openapi.Parameter(
        name='year',
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_INTEGER,
        description='год',
        required=True
    )
])
@api_view(['GET'])
def employee_statistics(request, pk: int):
    serializer = FilterDateSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    data = serializer.data
    filter_kwargs = {"date__year": data["year"], "date__month": data["month"]}
    context = {}
    employee_obj = get_object_or_404(EmployeeModel, pk=pk)
    filtered_orders = employee_obj.orders.filter(**filter_kwargs)
    clients_count = filtered_orders.count()
    unique_client = filtered_orders.distinct("client").count()
    prices_sum = filtered_orders.aggregate(order_price_sum=Sum("price"))["order_price_sum"]
    products_count = filtered_orders.annotate(products_count=Count("products")).aggregate(
        products_sum=Sum("products_count"))["products_sum"]
    context["employee_name"] = employee_obj.full_name
    context["clients_count"] = clients_count
    context["unique_client"] = unique_client
    context["prices_sum"] = prices_sum
    context["products_count"] = products_count

    return Response(context)


@swagger_auto_schema(tags=['statistics'], method='get', manual_parameters=[
    openapi.Parameter(
        name='month',
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_INTEGER,
        description='месяц',
        required=True
    ),
    openapi.Parameter(
        name='year',
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_INTEGER,
        description='год',
        required=True
    )
], responses={200: ResponseEmployeesStatisticsSerializer(many=True)})
@api_view(['GET'])
def all_employees_stat(request):
    serializer = FilterDateSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    data = serializer.data
    filter_kwargs = {"date__year": data["year"], "date__month": data["month"]}
    response = []
    employees = EmployeeModel.objects.all()
    filtered_orders = OrderModel.objects.filter(**filter_kwargs)
    for employee in employees:
        context = {}
        context["id"] = employee.id
        context["fullname"] = employee.full_name
        context["unique_clients"] = filtered_orders.distinct("client").count()
        context["clients"] = filtered_orders.count()
        context["products_count"] = filtered_orders.annotate(products_count=Count("products")).aggregate(
            products_sum=Sum("products_count"))["products_sum"]
        context["prices_sum"] = filtered_orders.aggregate(order_price_sum=Sum("price"))["order_price_sum"]
        response.append(context)
    return Response(response)


@swagger_auto_schema(tags=['statistics'], method='get', manual_parameters=[
    openapi.Parameter(
        name='month',
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_INTEGER,
        description='месяц',
        required=True
    ),
    openapi.Parameter(
        name='year',
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_INTEGER,
        description='год',
        required=True
    )
])
@api_view(['GET'])
def client_stat(request, pk):
    serializer = FilterDateSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    data = serializer.data
    context = {}
    filter_kwargs = {"date__year": data["year"], "date__month": data["month"]}
    client = get_object_or_404(ClientModel, pk=pk)
    filtered_orders = client.orders.filter(**filter_kwargs)
    context["id"] = client.id
    context["fullname"] = client.full_name
    context["products_count"] = filtered_orders.annotate(products_count=Count("products")).aggregate(
        products_sum=Sum("products_count")).get("products_sum", 0)
    context["prices_sum"] = filtered_orders.aggregate(order_price_sum=Sum("price"))["order_price_sum"]
    return Response(context)
