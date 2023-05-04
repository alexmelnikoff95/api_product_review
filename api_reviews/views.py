from django.db import models
from rest_framework import status
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from api_reviews.exaption import APIReviewException, MyException
from api_reviews.models import Product, Manufacturer
from api_reviews.serializers import ProductSerializer, ProductDetailSerializer, ReviewCreateSerializer, \
    RatingSerializer, ManufacturerSerializer, ManufacturerDetailSerializer
from api_reviews.utils import get_client_ip


class ProductListView(APIView):

    def get(self, request):

        try:
            qs = Product.objects.filter(published=True).annotate(
                rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(request)))
            ).annotate(
                middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
            )
            sr = ProductSerializer(qs, many=True)
        except APIReviewException as e:
            raise MyException(str(e))
        return Response(sr.data)


class ProductDetailView(APIView):

    def get(self, request, pk):
        try:
            sr = ProductDetailSerializer(get_object_or_404(Product, id=pk))
        except APIReviewException as e:
            raise MyException(str(e))
        return Response(sr.data)


class ReviewCreateView(APIView):

    def post(self, request):
        try:
            sr = ReviewCreateSerializer(data=request.data)
        except APIReviewException as e:
            raise MyException(str(e))
        if sr.is_valid(raise_exception=True):
            sr.save()
        return Response(status=status.HTTP_201_CREATED)


class AddStarRatingView(APIView):

    def post(self, request):
        try:
            sr = RatingSerializer(data=request.data)
        except APIReviewException as e:
            raise MyException(str(e))

        if sr.is_valid(raise_exception=True):
            sr.save(ip=get_client_ip(request))
            return Response(status=201)
        return Response(status=400)


class ManufacturerListView(generics.ListAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer


class ManufacturerDetailView(generics.RetrieveAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerDetailSerializer
