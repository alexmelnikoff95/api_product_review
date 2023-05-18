from django.urls import path

from api_reviews.views import ProductListView, ProductDetailView, ReviewCreateView, AddStarRatingView, \
    ManufacturerListView, ManufacturerDetailView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('review-create/', ReviewCreateView.as_view(), name='review_create'),
    path('rating/', AddStarRatingView.as_view(), name='add_rating'),
    path('manufacturer/', ManufacturerListView.as_view(), name='manufacturer_list'),
    path('manufacturer/<int:pk>/', ManufacturerDetailView.as_view(), name='manufacturer_detail'),
]
