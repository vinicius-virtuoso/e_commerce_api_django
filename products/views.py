from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from products.models import ImageProduct, Product
from products.serializers import ProductSerializer
from users.permissions import IsAdmin
from rest_framework.views import APIView,Request,Response,status
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q

from utils.upload_images import destroy_cloud_image


class ProductCreateListView(APIView):
    permission_classes = [IsAdmin]
    parser_classes = [MultiPartParser, FormParser]
    
    def get(self, request: Request) -> Response:
        products = Product.objects.all().order_by('price')
        serializer = ProductSerializer(instance=products,many=True)
        return Response(serializer.data,status.HTTP_200_OK)
    
    def post(self, request: Request) -> Response:
        data_request = self.request.data
        products_exists = Product.objects.filter(slug__iexact=data_request.get('slug',None)).exists()
        if products_exists:
            return Response({"detail": "Product already exists."},status.HTTP_409_CONFLICT)
        
        categories = [value for key,value in data_request.items() if key.startswith('category_')]
        serializer = ProductSerializer(data=data_request)
        serializer.is_valid(raise_exception=True)
        serializer.save(categories=categories,image=request.FILES.get('image'))
        return Response(serializer.data, status.HTTP_201_CREATED)    
        

class ProductDetailView(APIView):
    permission_classes = [IsAdmin]
    parser_classes = [MultiPartParser, FormParser]
    
    def get(self, request:Request, slug:str):
        product = get_object_or_404(Product, slug=slug)
        serializer = ProductSerializer(instance=product)
        return Response(serializer.data,status.HTTP_200_OK)
    
    def patch(self, request:Request, slug:str):
        data_request = self.request.data
        product = get_object_or_404(Product, slug=slug) 
        serializer = ProductSerializer(product,data_request,partial=True)
        serializer.is_valid(raise_exception=True)
        categories = [value for key,value in data_request.items() if key.startswith('category_')]
        serializer.save(categories=categories,image=request.FILES.get('image',None))
        return Response(serializer.data, status.HTTP_200_OK)   
        
    def delete(self, request:Request, slug:str):
        product = get_object_or_404(Product, slug=slug) 
        image_product = get_object_or_404(ImageProduct, product=product)
        
        if destroy_cloud_image(image_product.image_url):
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"Error": "Internal Server Error"}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
        
        
