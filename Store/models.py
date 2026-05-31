from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_category_url(self):
        return reverse('Store:products_by_category', args=[self.slug])
    


class Product(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'AV', 'Available'
        DREFT     = 'DF', 'Dreft'
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    image= models.ImageField(upload_to='products/images')
    description = models.TextField(max_length=1500 , default='Lorem ipsum dolor sit amet consectetur, adipisicing elit. Repudiandae neque perferendis excepturi')
    price= models.DecimalField(max_digits=6, decimal_places=2)
    status= models.CharField(max_length=2, choices=Status.choices)
    creat_at = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    def save(self):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save()

    def __str__(self):
        return self.name
    
    def get_product_url(self):
        return reverse('Store:product_detail', args=[self.slug])
    

    class Meta:
        ordering = ['name']
        indexes  = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-creat_at'])
        ]

