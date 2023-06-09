from django.db import models
from django.utils import timezone
from account.models import Profile, Account
from PIL import Image

# Create your models here.

class PostSell(models.Model):

    """
    Model representing a post for selling an item.
    """
    
    post_type =         models.CharField(default='Sell', max_length=150)  # Type of the post (e.g. sell,rent,garage sale)
    poster =            models.ForeignKey(Profile, on_delete=models.CASCADE)  
    title =             models.CharField(max_length=150)  
    latitude =          models.CharField(max_length=160)  
    longitude =         models.CharField(max_length=150)  
    price =             models.IntegerField()  
    size =              models.CharField(max_length=100)  
    show_to_verified =  models.BooleanField(default=True)  
    description =       models.TextField(max_length=300, blank=True)  
    time =              models.DateTimeField(default=timezone.now)
    flat_no =           models.CharField(max_length=100, blank=True)
    street_no =         models.CharField(max_length=100) 
    street =            models.CharField(max_length=100) 
    neighborhood =      models.CharField(max_length=100) 
    city =              models.CharField(max_length=100) 
    country =           models.CharField(max_length=100) 
    postal_code =       models.CharField(max_length=100)  
    condition =         models.CharField(max_length=100)  # Condition of the item (e.g. like new, good, fair)
    age =               models.IntegerField()  # Age of the item (how old the item is)
    age_unit =          models.CharField(max_length=100)  # Unit of the age (e.g., years, months)



class PostSellPictures(models.Model):

    """
    Model representing pictures associated with a post for selling an item.
    """
    
    post =            models.ForeignKey(PostSell, on_delete=models.CASCADE)  # Post to which the picture belongs
    image =           models.ImageField(upload_to='post_sell_pics', blank=False)  # Image file of the picture



class PostSellLikes(models.Model):

    """
    Model representing likes on a post for selling an item.
    """
    
    post =            models.ForeignKey(PostSell, on_delete=models.CASCADE)  # Post that received the like
    user =            models.ForeignKey(Account, on_delete=models.CASCADE)  # User who liked the post
    time =            models.DateTimeField(default=timezone.now)  # Time when the like was made

    class Meta:
        unique_together = ['post', 'user']  # Ensure uniqueness of post-user combination



class PostSellDeletes(models.Model):
    
    """
    Model representing deletion actions on a post for selling an item.
    """
    
    post =            models.ForeignKey(PostSell, on_delete=models.CASCADE)  # Post that was deleted
    user =            models.ForeignKey(Account, on_delete=models.CASCADE)  # User who deleted the post
    time =            models.DateTimeField(default=timezone.now)  # Time when the deletion action was performed

    class Meta:
        unique_together = ['post', 'user']  # Ensure uniqueness of post-user combination



class PostSellReceivedInterest(models.Model):
    
    """
    Model representing received interest on a post for selling an item.
    """
    
    buyer =         models.ForeignKey(Profile, on_delete=models.CASCADE)  # User who showed interest
    item =          models.ForeignKey(PostSell, on_delete=models.CASCADE)  # Post for which interest was shown
    time =          models.DateTimeField(default=timezone.now)  # Time when the interest was shown
    # class Meta:
    #     # Add a unique together constraint for 'buyer' and 'item'
    #     unique_together = ('buyer', 'item')
