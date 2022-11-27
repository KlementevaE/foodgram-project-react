from rest_framework.pagination import PageNumberPagination
# isort: skip
from foodgram.settings import REST_FRAMEWORK  # isort: skip


class CustomPagination(PageNumberPagination):
    page_size = REST_FRAMEWORK['PAGE_SIZE']
    page_size_query_param = 'limit'
