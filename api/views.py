from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Ingredient, Recipe
from recipes.sessions import CsrfExemptSessionAuthentication

from .filters import IngredientRangeFilter
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
    filter_backends = [filters.SearchFilter,]
    search_fields = ['title',]


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

#
# from django.shortcuts import get_object_or_404
# from rest_framework import filters, mixins, viewsets, status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
#
#
# from recipes.models import Ingredient
# from .models import Subscribe, Favorite
# from .serializers import (IngredientSerializer, SubscriptionSerializer,
#                           FavoriteSerializer, PurchaseSerializer)
#
#
# class CreateDestroyViewSet(mixins.CreateModelMixin,
#                            mixins.DestroyModelMixin,
#                            viewsets.GenericViewSet):
#     """
#     A viewset that provides `create` and `destroy` actions.
#     `destroy` action is overriden to return a json with a `success` flag.
#     """
#     def get_object(self, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#
#         lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
#         filter_kwargs = {
#             self.lookup_field: self.kwargs[lookup_url_kwarg],
#             **kwargs,
#         }
#
#         obj = get_object_or_404(queryset, **filter_kwargs)
#         self.check_object_permissions(self.request, obj)
#
#         return obj
#
#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object(user=self.request.user)
#         success = instance.delete()
#         return Response({'success': bool(success)}, status=status.HTTP_200_OK)
#
#
# class IngredientViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
#     """
#     Provide a search for ingredients in database.
#     """
#     queryset = Ingredient.objects.all()
#     serializer_class = IngredientSerializer
#     filter_backends = (filters.SearchFilter, )
#     search_fields = ('^title',)
#
#
# class SubscriptionViewSet(CreateDestroyViewSet):
#     """
#     A viewset that provides creation and deletion of
#     `api.Subscription` entries.
#     """
#     queryset = Subscribe.objects.all()
#     serializer_class = SubscriptionSerializer
#     permission_classes = (IsAuthenticated, )
#     lookup_field = 'author'
#
#
# class FavoriteViewSet(CreateDestroyViewSet):
#     """
#     A viewset that provides creation and deletion of
#     `api.Favorite` entries.
#     """
#     queryset = Favorite.objects.all()
#     serializer_class = FavoriteSerializer
#     permission_classes = (IsAuthenticated, )
#     lookup_field = 'recipe'
#
#
# class PurchaseViewSet(mixins.ListModelMixin, CreateDestroyViewSet):
#     """
#     A viewset that provides creation, deletion and listing of
#     `api.Purchase` entries for a given `auth.User`.
#     """
#     serializer_class = PurchaseSerializer
#     permission_classes = (IsAuthenticated, )
#     lookup_field = 'recipe'
#
#     def get_queryset(self):
#         return self.request.user.purchases.all()
