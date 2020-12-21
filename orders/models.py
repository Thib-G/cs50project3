from django.db import models

# Create your models here.


class Category(models.Model):
    """Food categories"""
    class Meta:
        verbose_name_plural = "categories"

    category_name = models.CharField(max_length=100)
    order_nr = models.IntegerField(default=0)

    def __str__(self):
        return self.category_name


class Item(models.Model):
    """Food items"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    max_toppings = models.IntegerField(null=True)

    def __str__(self):
        return self.item_name


class Pricing(models.Model):
    """Prices by item with multiple sizes"""
    PRICING_TYPES = (
        ('S', 'Small'),
        ('L', 'Large'),
        ('N', 'N/A'),
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    pricing_type = models.CharField(max_length=1, choices=PRICING_TYPES)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        if self.pricing_type != 'N':
            return f"{self.item.category} {self.item} {self.get_pricing_type_display()}: ${self.price}"
        return f"${self.price}"


class Topping(models.Model):
    """Toppings for pizzas"""
    topping_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.topping_name}"


class Cart(models.Model):
    """Cart containing pricing items"""
    is_completed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart nr {self.pk}"


class CartItem(models.Model):
    """Item added to the shopping cart"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    pricing_item = models.OneToOneField(Pricing, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cart}, item: {self.pricing_item}"
