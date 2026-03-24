from django.db import models

from django.contrib.auth.models import User


class Register(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    year = models.IntegerField()
    email = models.EmailField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=28)

    class Meta:
        ordering = ['username']


    def __str__(self):
        return self.username
    






class Book(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    about = models.TextField()
    author = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    janr = models.CharField(max_length=100)
    nashriyot = models.CharField(max_length=100)
    year = models.DateField()
    sale = models.IntegerField(default=0)
    count = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

    @property
    

    def old_price(self):
       if self.sale > 0:
        
        return int(self.price / (1 - self.sale / 100))
       return self.price

    class Meta:
        ordering = ['-created_at']

class Bookimage(models.Model):
    image = models.ImageField(upload_to='bookimage/')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='images')

    
    def __str__(self):
       return self.book.name
    
class Comment(models.Model):
   text = models.TextField()
   full_name = models.CharField(max_length=100)
   created_at = models.DateTimeField(auto_now_add=True)
   book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comment_list')





    