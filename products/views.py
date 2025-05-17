from rest_framework.response import Response
from rest_framework import viewsets, status
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.contrib.postgres.search import TrigramSimilarity

from .models import Product
from .serializers import ProductSerializer
from .utils import build_icontains_query

@method_decorator(cache_page(60 * 2), name='list')  # Cache for 2 minutes
class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing and searching products with efficient caching and rate limiting.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    # Search configuration
    SEARCH_FIELDS = ["name", "brand", "category"]
    NUTRITION_FIELD = "nutrition_facts"
    TRIGRAM_THRESHOLD = 0.3
    SHORT_QUERY_LENGTH = 5

    def _search_with_trigram(self, search_query: str) -> Q:
        """
        Search using trigram similarity on name, brand, and category fields.
        Returns a queryset with similarity scores and filtering.
        """
        return self.get_queryset().annotate(
            name_similarity=TrigramSimilarity('name', search_query),
            brand_similarity=TrigramSimilarity('brand', search_query),
            category_similarity=TrigramSimilarity('category', search_query)
        ).filter(
            Q(name_similarity__gt=self.TRIGRAM_THRESHOLD) |
            Q(brand_similarity__gt=self.TRIGRAM_THRESHOLD) |
            Q(category_similarity__gt=self.TRIGRAM_THRESHOLD)
        ).order_by(
            '-name_similarity',
            '-brand_similarity',
            '-category_similarity'
        )

    def _search_with_icontains(self, search_query: str) -> Q:
        """
        Search using case-insensitive contains on all fields including nutrition_facts.
        """
        fields = self.SEARCH_FIELDS + [self.NUTRITION_FIELD]
        return self.get_queryset().filter(build_icontains_query(fields, search_query))

    def _get_search_results(self, search_query: str) -> Q:
        """
        Get search results using appropriate search method based on query length.
        """
        if len(search_query) <= self.SHORT_QUERY_LENGTH:
            # For short queries, use icontains on all fields
            return self._search_with_icontains(search_query)
        
        # For longer queries, try trigram similarity first
        queryset = self._search_with_trigram(search_query)
        
        # If no results found with trigram, fallback to icontains
        if not queryset.exists():
            queryset = self._search_with_icontains(search_query)
        
        return queryset

    def list(self, request, *args, **kwargs):
        """
        List products with optional search functionality.
        Supports both trigram similarity and icontains search methods.
        """
        search_query = request.query_params.get('search')
        queryset = self.get_queryset()

        if search_query:
            queryset = self._get_search_results(search_query)

        # Handle pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Return unpaginated results
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



