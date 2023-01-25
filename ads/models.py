from django.db import models



# Create your models here.

class Location(models.Model):
    id = models.BigIntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=200)  
    lat = models.DecimalField(max_digits=10, decimal_places=7)
    lng = models.DecimalField(max_digits=10, decimal_places=7)
    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self):
        return self.name

class User(models.Model):
    id = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, null=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=120)
    role = models.CharField(max_length=10)
    age = models.IntegerField()
    location_id = models.ManyToManyField(Location)
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['username']

    def __str__(self):
        return self.username

class Category(models.Model):
    id = models.BigIntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=50)
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Ad(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)    
    price = models.DecimalField(max_digits=18 ,decimal_places=2)
    description = models.TextField(max_length=2000, blank=True)
    is_published = models.BooleanField(default= True)
    image = models.ImageField(upload_to='images/', null = True)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.name