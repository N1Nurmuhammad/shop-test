from django.core.cache import cache
from django.db.models import Count
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.v1.shop.serializers import ResponseEmployeesStatisticsSerializer, FilterDateSerializer, date_params, \
    ResponseEmployeeStatisticsWithPk, ResponseClientStatisticsSerializer
from api.v1.shop.utils import filter_fields, check_to_cache
from apps.shop.models import *


@swagger_auto_schema(tags=['statistics'], method='get', manual_parameters=date_params,
                     responses={200: ResponseEmployeeStatisticsWithPk})
@api_view(['GET'])
def employee_statistics(request, pk: int):
    context = {}
    serializer = FilterDateSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    data = serializer.data
    filter_kwargs = filter_fields(data)
    cache_date = cache.get(f"stat_empl_{pk}_{filter_kwargs}")
    if cache_date:
        return Response(cache_date)
    employee_obj = get_object_or_404(EmployeeModel, pk=pk)
    filtered_orders = employee_obj.orders.filter(**filter_kwargs).select_related("client").prefetch_related(
        "products")
    clients_count = filtered_orders.count()
    unique_client = filtered_orders.distinct("client").count()
    prices_sum = filtered_orders.aggregate(order_price_sum=Sum("price"))["order_price_sum"]
    products_count = filtered_orders.annotate(products_count=Count("products")).aggregate(
        products_sum=Sum("products_count"))["products_sum"]
    context["employee_name"] = employee_obj.full_name
    context["clients_count"] = clients_count
    context["unique_client"] = unique_client
    context["prices_sum"] = prices_sum or 0
    context["products_count"] = products_count or 0
    if check_to_cache(filter_kwargs):
        cache.set(f"stat_empl_{pk}_{filter_kwargs}", context)
    else:
        cache.set(f"stat_empl_{pk}_{filter_kwargs}", context, 60)
    return Response(context, status=status.HTTP_200_OK)


@swagger_auto_schema(tags=['statistics'], method='get', manual_parameters=date_params,
                     responses={200: ResponseEmployeesStatisticsSerializer(many=True)})
@api_view(['GET'])
def all_employees_stat(request):
    serializer = FilterDateSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    data = serializer.data
    filter_kwargs = filter_fields(data)
    cache_date = cache.get(f"stat_all_empl_{filter_kwargs}")
    if cache_date:
        return Response(cache_date)
    filtered_orders = OrderModel.objects.filter(**filter_kwargs).select_related("employee", "client").prefetch_related(
        "products")
    order_stats = filtered_orders.values("employee__id").annotate(
        unique_clients=Count("client", distinct=True),
        clients=Count("client"),
        products_sum=Sum("products"),
        prices_sum=Sum("price")
    ).values("employee__id", "employee__full_name", "unique_clients", "clients", "products_sum", "prices_sum")
    response = [
        {
            "id": stat["employee__id"],
            "fullname": stat["employee__full_name"],
            "unique_clients": stat["unique_clients"],
            "clients": stat["clients"],
            "products_count": stat["products_sum"] or 0,
            "prices_sum": stat["prices_sum"] or 0
        }
        for stat in order_stats
    ]
    if check_to_cache(filter_kwargs):
        cache.set(f"stat_all_empl_{filter_kwargs}", response)
    else:
        cache.set(f"stat_all_empl_{filter_kwargs}", response, 60)
    return Response(response, status=status.HTTP_200_OK)


@swagger_auto_schema(tags=['statistics'], method='get', manual_parameters=date_params,
                     responses={200: ResponseClientStatisticsSerializer})
@api_view(['GET'])
def client_stat(request, pk: int):
    serializer = FilterDateSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    data = serializer.data
    context = {}
    filter_kwargs = filter_fields(data)
    cache_date = cache.get(f"stat_client_{pk}_{filter_kwargs}")
    if cache_date:
        return Response(cache_date)
    client = get_object_or_404(ClientModel, pk=pk)
    filtered_orders = client.orders.filter(**filter_kwargs).prefetch_related("products")
    context["id"] = client.id
    context["fullname"] = client.full_name
    context["products_count"] = filtered_orders.annotate(products_count=Count("products")).aggregate(
        products_sum=Sum("products_count")).get("products_sum", 0)
    context["prices_sum"] = filtered_orders.aggregate(order_price_sum=Sum("price")).get("order_price_sum", 0)
    if check_to_cache(filter_kwargs):
        cache.set(f"stat_client_{pk}_{filter_kwargs}", context)
    else:
        cache.set(f"stat_client_{pk}_{filter_kwargs}", context, 60)
    return Response(context, status=status.HTTP_200_OK)
