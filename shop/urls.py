from django.urls import path
from django.http import HttpResponse
from .views import ProductListAPIView, ProductDetailAPIView, CartAPIView, CheckoutAPIView

def api_root(request):
    html = """
    <html>
        <head><title>Интернет магазин</title></head>
        <body>
            <h1>Интернет магазин</h1>
            <p>Добро пожаловать в Интернет магазин.</p>
            <ul>
                <li><a href="/api/products/">Товары</a></li>
                <li><a href="/api/cart/">Корзина</a></li>
                <li><a href="/api/checkout/">Оформление заказа</a></li>
            </ul>
        </body>
    </html>
    """
    return HttpResponse(html)

urlpatterns = [
    path('', api_root),
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('cart/', CartAPIView.as_view(), name='cart'),
    path('checkout/', CheckoutAPIView.as_view(), name='checkout'),
]
