from django.shortcuts import render
from django.views import View
from django.http.response import JsonResponse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from ads import serializers
import json
import os
from .models import User, Location, Category, Ad

class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = serializers.LocationSerializer

@method_decorator(csrf_exempt, name="dispatch")
class AdListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = serializers.AdListSerializer
    def get(self, request, *args, **kwargs):
        category=request.GET.get('cat',None)
        if category:
            self.queryset = self.queryset.filter(
                category_id__exact = category
            )

        text=request.GET.get('text',None)
        if text:
            self.queryset = self.queryset.filter(
                name__icontains = text
            )

        location=request.GET.get('location',None)
        if location:
            self.queryset = self.queryset.filter(
                author_id__location_id__name__iexact = location
            )
        
        priceFrom = request.GET.get('price_from', None)
        priceTo = request.GET.get('price_to', None)
        
        if priceTo and priceFrom:
            self.queryset = self.queryset.filter(
                price__range=(priceFrom,priceTo)
            )

        return super().get(request, *args, **kwargs)

class AdDetailView(DetailView):
    model = Ad
    def get(self, request, *args, **kwargs):
        super().get(request,*args,**kwargs)
        data = []
        obj = self.get_object()
        data.append({
                "id":obj.id,
                "name":obj.name,
                "author_id":obj.author_id.id if obj.author_id else None,
                "price":obj.price,
                "description":obj.description,
                "is_published":obj.is_published,
                "image":json.dumps(str(obj.image)) if obj.image else None,
                "category_id":obj.category_id.id if obj.category_id else None
            })
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateView(UpdateView):
    model = Ad
    fields = ["id","name","author_id","price","description","image","category_id","is_published"]
    def patch(self, request, *args, **kwargs):
        super().post(request,*args,**kwargs)
        res = []
        ad = self.get_object()
        data = json.loads(request.read())
        if "name" in data:
            ad.name = data["name"]
        if "author_id" in data:
            ad.author_id = data["author_id"]
        if data["price"]:
            ad.price = data["price"]
        if "description" in data:
            ad.description = data["description"]
        if "is_published" in data:
            ad.is_published = data["is_published"]
        if "image" in data:
            ad.image = data["image"]
        if "category_id" in data:
            ad.category_id = data["category_id"] 
        
        ad.save()
        res.append({
                "id":ad.id,
                "name":ad.name,
                "author_id":ad.author_id.id if ad.author_id else None,
                "price":ad.price,
                "description":ad.description,
                "is_published":ad.is_published,
                "image":json.dumps(str(ad.image)) if ad.image else None,
                "category_id":ad.category_id.id if ad.category_id else None
            })

        return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})

@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
    model = Ad
    fields = ["id","name","author_id","price","description","image","category_id","is_published"]
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.read())
        print(data)
        ad = Ad()
        ad.name = data["name"]
        ad.author_id = User.objects.get(pk=data["author_id"])
        ad.price = data["price"]
        ad.description = data["description"]
        ad.image = request.FILES.get("image", None)
        ad.category_id = Category.objects.get(pk=data["category_id"])

        ad.save()
        return JsonResponse({"status":"200"}, status=200)

@method_decorator(csrf_exempt, name="dispatch")
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/ads/"
    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status":"ok"}, status = 200)

@method_decorator(csrf_exempt, name="dispatch")
class ImageView(UpdateView):
    model = Ad
    fields = ["id","name","author_id","price","description","image","category_id","is_published"]
    def post(self, request, *args, **kwargs):
        super().post(request,*args,**kwargs)
        res = []
        ad = self.get_object()
        ad.image = request.FILES.get("image")

        
        ad.save()
        res.append({
                "id":ad.id,
                "name":ad.name,
                "author_id":ad.author_id.id if ad.author_id else None,
                "price":ad.price,
                "description":ad.description,
                "is_published":ad.is_published,
                "image":json.dumps(str(ad.image)) if ad.image else None,
                "category_id":ad.category_id.id if ad.category_id else None
            })

        return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})
        


class CategoryListView(ListView):
    model = Category
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = Category.objects.all().order_by('name')
        paginator = Paginator(self.object_list, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        data = []
        for i in page_obj:
            data.append({
                "id":i.id,
                "name":i.name
            })
        res = {
            "items":data,
            "total":paginator.count,
            "num_pages":paginator.num_pages
        }
        return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})

class CategoryDetailView(DetailView):
    model = Category
    def get(self, request, *args, **kwargs):
        super().get(request,*args,**kwargs)
        data = []
        obj = self.get_object()
        data.append({
                "id":obj.id,
                "name":obj.name
            })
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

@method_decorator(csrf_exempt, name="dispatch")
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ["id","name"]
    def patch(self, request, *args, **kwargs):
        super().post(request,*args,**kwargs)
        res = []
        category = self.get_object()
        data = json.loads(request.read())
        if "name" in data:
            category.name = data["name"]
        
        category.save()
        res.append({
                "id":category.id,
                "name":category.name
            })

        return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})

@method_decorator(csrf_exempt, name="dispatch")
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/categories/"
    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status":"ok"}, status = 200)



class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

@method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserCreateSerializer

@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserUpdateSerializer

@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserDestroySerializer


