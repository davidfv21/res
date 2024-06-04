from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import *
from .serializers import *
from django.utils import timezone
from apps.shift.models import WaiterShift
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsManager,IsManagerOrAdminTables

class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated]



    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'waiter'):
            current_time = timezone.now()
            waiter_shifts = WaiterShift.objects.filter(waiter=user.waiter, start_date__lte=current_time, end_date__gte=current_time)
            print(waiter_shifts, current_time)
            if waiter_shifts.exists():
                # Get the restaurants from the current shifts
                restaurants = waiter_shifts.values_list('restaurant', flat=True)
                # Filter tables based on the restaurants in the current shifts
                tables_restaurants = TablesRestaurant.objects.filter(restaurant__in=restaurants)
                table_ids = tables_restaurants.values_list('table_id', flat=True)
                return Table.objects.filter(id__in=table_ids)
            else:
                return Table.objects.none()
        else:
            return Table.objects.all()


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = [IsManagerOrAdminTables]
        self.check_permissions(request)
        return super().destroy(request, *args, **kwargs)


class TablesRestaurantViewSet(viewsets.ModelViewSet):
    queryset = TablesRestaurant.objects.all()
    serializer_class = TablesRestaurantSerializer



class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = [IsManager]
        self.check_permissions(request)
        return super().destroy(request, *args, **kwargs)