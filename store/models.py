from django.db import models
from django.contrib.auth.models import User



# Define a model for a Customer
class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)

	# Define the string representation of a Customer.
	def __str__(self):
		return self.name

# Define a model for a Product
class Product(models.Model):
	name = models.CharField(max_length=200)
	price = models.FloatField()
	digital = models.BooleanField(default=False,null=True, blank=True)
	image = models.ImageField(null=True, blank=True)
	description = models.TextField(null=True, blank=True)

	# Define the string representation of a Product.
	def __str__(self):
		return self.name

	# Define a property method that returns the URL of the image associated with the Product.
	# If the Product has no image, return an empty string.
	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

# Define a model for an Order

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	# Define the string representation of an Order.
	def __str__(self):
		return str(self.id)

	# Define a property method that returns the total price of all items in the cart.
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product is not None and i.product.digital == False:
				shipping = True
		return shipping

	# Define a property method that returns the total number of items in the cart.
	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	# Define a property method that returns the total number of items in the cart.
	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

# Define a model for an OrderItem
class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	# Define a property method that returns the total price for this OrderItem
	# (price of the associated Product times the quantity of the OrderItem).
	@property
	def get_total(self):
		if self.product is None:
			return 0
		total = self.product.price * self.quantity
		return total

# Define a model for a ShippingAddress
class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	# Define the string representation of a ShippingAddress.
	def __str__(self):
		return self.address