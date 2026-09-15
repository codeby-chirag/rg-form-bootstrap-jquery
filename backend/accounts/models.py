from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Person(models.Model):
    GENDER_CHOICES = [  # noqa: RUF012
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    def calculate_age(self):
        if not self.dob:
            return "-"
                
        today = date.today()  # noqa: DTZ011

        age = today.year - self.dob.year - (
            (today.month, today.day) < (self.dob.month, self.dob.day)
        )
        return age
   
   
    def full_name(self):
        return self.user.first_name + " " + self.user.last_name
    
    def email(self):
        return self.user.email if self.user else "-"

    def fullname(self):
        if self.user:
            name = f"{self.user.first_name} {self.user.last_name}".strip()
            return name if name else self.user.username
        return "-"    

    
    COUNTRY_CHOICES = [  # noqa: RUF012
        ('india', 'India'),
        ('australia', 'Australia'),
        ('usa', 'USA'),
    ]   
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    number = models.CharField(max_length=15)      
    hobbies = models.CharField(max_length=255, blank=True) 
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    country = models.CharField(max_length=50, choices=COUNTRY_CHOICES, default='india')
    


    def __str__(self):
        if self.user:
            return self.user.username
        return f"Profile {self.id}"
    
    
@receiver(post_delete, sender=Person)
def delete_related_user(sender, instance, **kwargs):
    """Deletes the associated User object when a Person instance is deleted."""
    if instance.user:
        instance.user.delete()
        






