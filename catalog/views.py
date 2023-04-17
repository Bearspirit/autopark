from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Managers, Vehicles, Enterprise
from .serializers import ManagerSerializer, EnterpriseSerializer, VehiclesSerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

'''
Этот класс позволяет отображать данные по всем менеджерам, без авторизации пользователя
в, то есть передает данные любому запросившему. Ниже класс переписан с учетом авторизации пользователя.
Данные будут отдаваться только по тому менеджеру и тому менеджеру, котрый авторизован
class ManagerListView(APIView):
    def get(self, request):
        managers = Managers.objects.all()
        serializer = ManagerSerializer(managers, many=True)
        return Response(serializer.data)
'''

class ManagerListView(ListAPIView):
    serializer_class = ManagerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        manager = self.request.user
        return Managers.objects.filter(id=manager.id)
    

class EnterpriseListView(APIView):
    def get(self, request):
        enterprises = Enterprise.objects.all()
        serializer = EnterpriseSerializer(enterprises, many=True)
        return Response(serializer.data)
'''    
class VehicleListView(APIView):
    def get(self, request):
        vehicles = Vehicles.objects.all()
        serializer = VehiclesSerializer(vehicles, many=True)
        return Response(serializer.data)
'''    
class VehicleListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vehicles = Vehicles.objects.filter(enterprise__manager_enterprise=request.user)
        serializer = VehiclesSerializer(vehicles, many=True)
        return Response(serializer.data)
    
@csrf_protect
def my_view(request):
    context = {
        'heading': 'Hello, world!',
        'content': 'This is Django view.',
    }
    return render(request, 'test.html', context)