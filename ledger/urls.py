from django.urls import path
from .views import block_list, chain_status

urlpatterns = [
    path("blocks/", block_list, name="block_list"),
    path("verify/", chain_status, name="chain_status"),
]