from django.test import TestCase, Client
from accounts.models import Account
from category.models import Category
from products.models import Product
from carts.models import CartItem
from django.urls import reverse


class OrdersIntegrationTests(TestCase):
	def setUp(self):
		# Create test user
		self.user = Account.objects.create_user(first_name='Test', last_name='User', username='testuser', email='test@example.com', password='testpass123')
		self.user.is_active = True
		self.user.save()

		# Create category and product
		self.cat = Category.objects.create(category_name='TestCat', slug='testcat')
		self.product = Product.objects.create(product_name='Test Product', slug='test-product', price=100, stock=50, category=self.cat)

		# Add a cart item for user
		self.cart_item = CartItem.objects.create(user=self.user, product=self.product, quantity=1)

		self.client = Client()

	def test_cod_flow_creates_order_and_invoice(self):
		# Login
		logged = self.client.login(email='test@example.com', password='testpass123')
		self.assertTrue(logged)

		# Post place_order with COD
		url = reverse('place_order')
		data = {
			'first_name': 'Test',
			'last_name': 'User',
			'email': 'test@example.com',
			'phone': '1234567890',
			'address_line_1': 'Addr1',
			'address_line_2': '',
			'city': 'City',
			'state': 'State',
			'country': 'Country',
			'order_note': 'note',
			'payment_method': 'COD',
		}
		response = self.client.post(url, data, follow=True)
		# After COD we end up on order_complete
		self.assertEqual(response.status_code, 200)
		self.assertIn('/orders/order_complete/', response.request['PATH_INFO'])

		# Download invoice
		order = response.context.get('order')
		payment = response.context.get('payment')
		self.assertIsNotNone(order)
		self.assertIsNotNone(payment)
		invoice_url = reverse('download_invoice') + f"?order_number={order.order_number}&payment_id={payment.payment_id}"
		invoice_resp = self.client.get(invoice_url)
		self.assertEqual(invoice_resp.status_code, 200)
		self.assertTrue(invoice_resp['Content-Disposition'].startswith('attachment;'))

	def test_online_flow_renders_payments(self):
		# Login
		self.client.login(email='test@example.com', password='testpass123')
		url = reverse('place_order')
		data = {
			'first_name': 'Test',
			'last_name': 'User',
			'email': 'test@example.com',
			'phone': '1234567890',
			'address_line_1': 'Addr1',
			'address_line_2': '',
			'city': 'City',
			'state': 'State',
			'country': 'Country',
			'order_note': 'note',
		}
		response = self.client.post(url, data)
		# Should render payments page
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'orders/payments.html')
