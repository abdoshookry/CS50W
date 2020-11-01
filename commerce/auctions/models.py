from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    AbstractUser



class comments(models.Model):
    text=models.CharField(max_length=500)
    commenter = models.CharField(max_length=64)
    def __str__(self):
        return f"text : {self.text} , commenter : {self.commenter}"



class bid(models.Model):
    price = models.IntegerField()
    highestBid = models.CharField(max_length=64)
    def __str__(self):
        return f"price : {self.price} , highestBid : {self.highestBid}"


class watchlists(models.Model):
    is_watching = models.BooleanField()
    user =  models.CharField(max_length=64)

    def __str__(self):
        return f"is watching : {self.is_watching} , user : {self.user}"
   

class  auction_listings(models.Model):
    name = models.CharField(max_length=64)
    descreption = models.CharField(max_length=500)
    image = models.URLField()
    category = models.CharField(max_length=64, default="no category")
    author = models.CharField(max_length=64, default = "none")
    closed =models.BooleanField(default=False)
    bid = models.ForeignKey( bid, on_delete=models.CASCADE, related_name="bid")
    comments = models.ManyToManyField(comments, blank = True, related_name="comments")
    watchlists = models.ForeignKey( watchlists, on_delete=models.CASCADE, related_name="watchlists")
    def __str__(self):
        return f"\n name : {self.name}, \n category : {self.category}, \n author :{self.author}, \n closed : {self.closed}, \n bid : ({self.bid}), \n watchlists : ({self.watchlists}) \n"

    
