from django.db import models
from django.urls import reverse
from CategoryApp.models import Category
# Create your models here.

class Product(models.Model):
    product_name    =      models.CharField(max_length=200,unique=True)
    slug            =      models.SlugField(max_length=200,unique=True)

    brief_description=     models.TextField(max_length=500,blank=True)    
    
    price           =      models.IntegerField()
    images          =      models.ImageField(upload_to='photos/products')
    stock           =      models.IntegerField()
    is_available    =      models.BooleanField(default=True)
    create_at       =      models.DateTimeField(auto_now_add=True)
    modified_date   =      models.DateTimeField(auto_now=True)

    category        =      models.ForeignKey(Category,on_delete=models.CASCADE)
    
    def get_url(self):
        return reverse('product_details',args=[self.category.slug,self.slug])

    def __str__(self):
        return self.product_name
    

# Variatation code start from here 
variation_category_choice = (
    ('color','color',),
    ('size','size',),
)

class VariationManager(models.Manager):
    def colors(self):
        return super (VariationManager, self).filter(variation_category = 'color', is_active=True)
    
    def sizes(self):
        return super (VariationManager, self).filter(variation_category = 'size', is_active=True)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    objects = VariationManager()

    class Meta:
        '''Meta definition for Variation.'''
  
        verbose_name = 'Variation'
        verbose_name_plural = 'Variations'

    def __str__(self):
        return self.variation_value
















