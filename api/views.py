from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import filters, generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Ingredient, Recipe
from recipes.sessions import CsrfExemptSessionAuthentication

from .models import Favorite, Purchase, Subscribe
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          PurchaseSerializer, SubscribeSerializer)

User = get_user_model()


class CreateResponseView:
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"success": True})
        return Response({"success": False})


class IngredientAPIView(generics.ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^title', ]


@method_decorator(csrf_exempt, name='dispatch')
class FavoriteCreateView(CreateResponseView, generics.CreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


@method_decorator(csrf_exempt, name='dispatch')
class FavoriteDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def delete(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        favorite = recipe.favored_by.filter(user=request.user)
        return Response({"success": bool(favorite.delete())})


@method_decorator(csrf_exempt, name='dispatch')
class PurchaseCreateView(CreateResponseView, generics.CreateAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


@method_decorator(csrf_exempt, name='dispatch')
class PurchaseDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def delete(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        purchase = recipe.in_purchases.filter(user=request.user)
        return Response({"success": bool(purchase.delete())})


@method_decorator(csrf_exempt, name='dispatch')
class SubscribeCreateView(CreateResponseView, generics.CreateAPIView):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


@method_decorator(csrf_exempt, name='dispatch')
class SubscribeDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def delete(self, request, id):
        author = get_object_or_404(User, id=id)
        subscribe = author.following.filter(user=request.user)
        return Response({"success": bool(subscribe.delete())})
