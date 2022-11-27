from rest_framework.pagination import PageNumberPagination  # isort: off

from foodgram.settings import REST_FRAMEWORK


class CustomPagination(PageNumberPagination):
    page_size = REST_FRAMEWORK['PAGE_SIZE']
    page_size_query_param = 'limit'
