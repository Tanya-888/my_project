# Create your views here.

from rest_framework import generics, permissions
from .models import Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer, OrderItemSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # корзина хранится во временной сессии (не идеально для API, но для примера)
        cart = request.session.get('cart', {})
        products = []
        total = 0
        for pk, qty in cart.items():
            try:
                product = Product.objects.get(pk=int(pk))
                product_data = ProductSerializer(product).data
                product_data['quantity'] = qty
                products.append(product_data)
                total += product.price * qty
            except Product.DoesNotExist:
                continue
        return Response({'products': products, 'total': total})

    def post(self, request):
        # Добавить товар в корзину: ожидается JSON {"product_id": int, "quantity": int}
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        if not product_id:
            return Response({'error': 'product_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
        request.session['cart'] = cart
        return Response({'message': 'Добавлено в корзину'}, status=status.HTTP_200_OK)

    def delete(self, request):
        # Очистить корзину
        request.session['cart'] = {}
        return Response({'message': 'Корзина очищена'}, status=status.HTTP_200_OK)

class CheckoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart = request.session.get('cart', {})
        if not cart:
            return Response({'error': 'Корзина пуста'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=request.user)
        for pk, qty in cart.items():
            try:
                product = Product.objects.get(pk=int(pk))
                OrderItem.objects.create(order=order, product=product, quantity=qty)
            except Product.DoesNotExist:
                continue
        # Очистим корзину после оформления заказа
        request.session['cart'] = {}

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)