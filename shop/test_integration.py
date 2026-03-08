from django.test import TestCase
from django.contrib.auth.models import User
from .models import Product, Cart, CartItem, Order, OrderItem

class OrderFlowTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=10.00,
            stock=10
        )

    def test_create_order_from_cart(self):
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, product=self.product, quantity=2)

        total_price = cart_item.quantity * cart_item.product.price

        order = Order.objects.create(
            user=self.user,
            total_price=total_price,
            status='Pending'
        )

        order_item = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=cart_item.quantity,
            price_at_purchase=self.product.price
        )

        # Проверки
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().product.name, 'Test Product')
        self.assertEqual(order.total_price, 20.00)
        self.assertEqual(order.items.first().quantity, 2)
        self.assertEqual(order.items.first().price_at_purchase, 10.00)

        print("Интеграционный тест успешно выполнен!")