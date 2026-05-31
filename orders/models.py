from django.db import models
from django.utils import timezone
from Store.models import Product
import random
import string

def generate_order_id(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


class Order(models.Model):
    order_id       = models.CharField(max_length=8 ,default=generate_order_id, unique=True)
    frist_name     = models.CharField(max_length=100)
    last_name      = models.CharField(max_length=100)
    email          = models.EmailField()
    address        = models.CharField(max_length=100)
    postal_code    = models.CharField(max_length=100)
    city           = models.CharField(max_length=100)
    create_at      = models.DateTimeField(default=timezone.now)
    update_at      = models.DateTimeField( auto_now_add=True)
    paid           = models.BooleanField(default=False)


    class Meta:
        ordering = ['-create_at']
        indexes  = [
            models.Index(fields=['-create_at'])
        ]


    def __str__(self):
        return f'Order ID:{self.order_id}'
    
    def get_full_name(self):
        return f"{self.frist_name} {self.last_name}"    

    def save(self, *args, **kwargs):
        if not self.order_id:
            unique_id = generate_order_id()
            while Order.objects.filter(order_id=unique_id).exists():
                unique_id = generate_order_id()
            self.order_id = unique_id

        super().save(*args, **kwargs)


    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items' , on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='order_item' , on_delete=models.CASCADE)
    price   = models.DecimalField(max_digits=6, decimal_places=2)
    quantity= models.PositiveIntegerField(default=1)

    def get_cost(self):
        return self.price * self.quantity
    
    def __str__(self):
        return str(self.id)
    


class OrderPay(models.Model):
    order  = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    pay_phone = models.CharField(max_length=9)
    creat_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creat_at']

    def __str__(self):
        return f'Pyment for Order [ID: {self.order.order_id} ]'