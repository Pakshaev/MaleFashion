from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
            verbose_name = 'бренд'
            verbose_name_plural = 'Бренды' 
          
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
                verbose_name = 'категория'
                verbose_name_plural = 'Категории' 

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
                verbose_name = 'цвет'
                verbose_name_plural = 'Цвета' 

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    gender = models.CharField(max_length=10)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image1 = models.ImageField()
    image2 = models.ImageField()
    image3 = models.ImageField()
    image4 = models.ImageField(blank=True, null=True)
    image5 = models.ImageField(blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'продукт'
        verbose_name_plural = 'Продукты'    

    def __str__(self):
        return self.name
    
    def discounted_price(self):
        return self.price * (1 - self.discount / 100)