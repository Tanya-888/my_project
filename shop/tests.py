from django.test import TestCase
from django.contrib.auth.models import User
from .models import Product, Cart, CartItem, Order, OrderItem


class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Test Product',
            description='A product for testing',
            price=99.99,
            stock=10
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), 'Test Product')


class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_str(self):
        self.assertEqual(str(self.cart), 'Cart of testuser')


class CartItemModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        cart = Cart.objects.create(user=user)
        product = Product.objects.create(
            name='Test Product',
            description='A product for testing',
            price=50,
            stock=5
        )
        self.cart_item = CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=2
        )

    def test_cart_item_str(self):
        expected_str = '2 x Test Product'
        self.assertEqual(str(self.cart_item), expected_str)


class OrderModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='orderuser', password='pass')
        product = Product.objects.create(
            name='Order Product',
            description='Test order product',
            price=20,
            stock=100
        )
        order = Order.objects.create(
            user=user,
            total_price=40,
            status='Pending'
        )
        self.order = order
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=2,
            price_at_purchase=20
        )

    def test_order_str(self):
        self.assertEqual(str(self.order), f'Order {self.order.id} of {self.order.user.username}')
