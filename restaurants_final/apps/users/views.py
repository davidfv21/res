# views.py
from rest_framework import viewsets
from .models import Waiter
from .serializers import WaiterSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import action
from apps.restaurant.models import Restaurant,Order
from apps.restaurant.serializers import OrderSerializer
from apps.shift.models import WaiterShift
from apps.restaurant.models import Bill
from apps.shift.serializers import WaiterShiftSerializer
from rest_framework.response import Response
from django.utils.timezone import now


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class WaiterViewSet(viewsets.ModelViewSet):
    queryset = Waiter.objects.all()
    serializer_class = WaiterSerializer


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        extra = request.query_params.get('extra', None)
        if extra is not None:
            today = now().date()
            upcoming_shifts = WaiterShift.objects.filter(
                waiter=instance, start_date__gte=today
            ).order_by('start_date')[:5]
            shift_serializer = WaiterShiftSerializer(upcoming_shifts, many=True)
            data['upcoming_shifts'] = shift_serializer.data

        return Response(data)

    @action(detail=True, methods=['get'])
    def get_tips(self, request, pk=None):
        waiter = self.get_object()
        tips_payed = Bill.objects.filter(order__waiter=waiter).exclude(final_cost=None).aggregate(Sum('tip_percent'))['tip_percent__sum'] or 0
        current_tips = Bill.objects.filter(order__waiter=waiter, final_cost=None).aggregate(Sum('tip_percent'))['tip_percent__sum'] or 0
        
        return Response({
            "tips_payed": tips_payed,
            "current_tips": current_tips
        })

    @action(detail=True, methods=['post'])
    def add_shift(self, request, pk=None):
            waiter = self.get_object()
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')
            restaurant_id = request.data.get('restaurant')
            restaurant = Restaurant.objects.get(id=restaurant_id)
            shift = WaiterShift.objects.create(waiter=waiter, start_date=start_date, end_date=end_date, restaurant=restaurant)
            return Response({'status': 'shift added'})



    @action(detail=True, methods=['get'], url_path='orders')
    def orders(self, request, pk=None):
        waiter = self.get_object()
        orders = Order.objects.filter(waiter=waiter)

        # Filtrar órdenes activas si el parámetro 'active' está presente y es igual a '1'
        active = request.query_params.get('active')
        if active == '1':
            orders = orders.filter(bill__isnull=True) | orders.filter(bill__final_cost__isnull=True)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=200)
