

from django.contrib.auth import authenticate
# from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status
from rest_framework.decorators import APIView, api_view, permission_classes
from .serializers import SignUpSerializer,ProductSerializer,CartSerializer,OrderSerializer,UserSerializer
from .tokens import create_jwt_pair_for_user
from .models import Product,Cart,Order,User
import datetime
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)

# Create your views here.


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = []

    def post(self, request: Request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            response = {"message": "User Created Successfully", "data": serializer.data}

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([AllowAny])  
class LoginView(APIView):
    permission_classes = []

    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)
        print(user)
        if user is not None:

            tokens = create_jwt_pair_for_user(user)

            response = {"message": "Login Successfull", "tokens": tokens}
            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data={"message": "Invalid email or password"})

    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}

        return Response(data=content, status=status.HTTP_200_OK)
    
@permission_classes([AllowAny])  
class ProductAllView(APIView):
    
    def get(self,request):
        detailsObj  = Product.objects.all()
        serialize = ProductSerializer(detailsObj,many=True)
        return Response(data=serialize.data,status=status.HTTP_200_OK)
    
@permission_classes([IsAuthenticated])
class UserView(APIView):
    def get(self,request):
        obj =  User.objects.filter(username=self.request.user).first()
        serialize = UserSerializer(obj)
        return Response(data=serialize.data,status=status.HTTP_200_OK)
    

@permission_classes([IsAuthenticated])
class ProductView(APIView):
    def get(self,request,Pid):
        obj = Product.objects.filter(Pid=Pid)
        print(obj)
        serialize = ProductSerializer(obj,many=True)
        print(serialize)
        return Response(data=serialize.data,status=status.HTTP_200_OK)
    @permission_classes([IsAdminUser])
    def post(self,request):
        obj = ProductSerializer(data = request.data)
        if obj.is_valid():
            obj.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            result = {"result":"product has invalid fields"}
            return Response(data=result,status=status.HTTP_406_NOT_ACCEPTABLE)
        
    
@permission_classes([IsAuthenticated])
class CartView(APIView):
    def get(self,request):
        obj = Cart.objects.filter(Cid=self.request.user)
        print(obj)
        serialize = CartSerializer(obj,many=True)
        print(serialize)
        return Response(data=serialize.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        obj = Cart()
        obj.Cid = self.request.user
        obj.Pid = Product.objects.filter(Pid=request.data.get("Pid")).first()
        obj.count = request.data.get("count")
        obj.save()
        return Response(status=status.HTTP_201_CREATED)
        
    def put(self,request):
        cid = self.request.user
        pid = Product.objects.filter(Pid=request.data.get("Pid")).first()
        obj = Cart.objects.filter(Cid=cid,Pid=pid).first()
        obj.count = request.data.get("count")
        print(obj)
        obj.save()
        return Response(status=status.HTTP_202_ACCEPTED)
       
        
    def delete(self,request):
        cid = self.request.user
        pid = Product.objects.filter(Pid=request.data.get("Pid")).first()
        obj = Cart.objects.filter(Cid=cid,Pid=pid).first()
        obj.delete()
        return Response(status = status.HTTP_200_OK)
    
    
@permission_classes([IsAuthenticated])
class OrderView(APIView):
    
    def post(self,request):
        obj = Order()
        obj.Cid = self.request.user 
        
        for each in request.data.get("products"):
            prod = Product.objects.filter(Pid=each["Pid"]).first()
            serializeprod = ProductSerializer(prod)
            if(serializeprod.data["count"]<each["count"]):
                result={"result":"this product :"+serializeprod.data["name"]+" is only available "+str(serializeprod.data["count"])+" times"}
                return Response(data=result,status=status.HTTP_400_BAD_REQUEST)
            
        for each in request.data.get("products"):
            obj.add_product(each["Pid"],each["count"])
        
        # obj.total_price = request.data.get("total_price")
        obj.date = datetime.datetime.now()
        obj.address = request.data.get("address")
        
        obj.save()
        
        #making cart empty of the user
        list_cart = Cart.objects.filter(Cid=self.request.user)
        for each in list_cart:
            each.delete()
        return Response(status= status.HTTP_201_CREATED)
    
    def get(self,request):
        obj = Order.objects.filter(Cid=self.request.user)
        serialize = OrderSerializer(obj,many=True)
        return Response(data = serialize.data,status = status.HTTP_200_OK)
        