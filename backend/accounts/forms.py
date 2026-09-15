from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import Person


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'placeholder': 'email@gmail.com', 'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
    )
    firstname = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'})
    )
    lastname = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'})
    )
    
    # Profile/Person fields
    number = forms.CharField(
        max_length=15, 
        widget=forms.TextInput(attrs={'placeholder': 'Mobile Number', 'class': 'form-control'})
    )
    
    # Checkboxes for Hobbies
    HOBBIE_CHOICES = [  # noqa: RUF012
        ('Cricket', 'Cricket'),
        ('Football', 'Football'),
        ('Hockey', 'Hockey'),
        ('Bowling', 'Bowling'),
        ('Basketball', 'Basketball'),
    ]
    hobbies = forms.MultipleChoiceField(
        choices=HOBBIE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    # Radio buttons for Gender
    GENDER_CHOICES = [  # noqa: RUF012
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect
    )
    
    COUNTRY_CHOICES = [  # noqa: RUF012
        ('india', 'India'),          
        ('australia', 'Australia'),  
        ('usa', 'USA'),              
    ]
    country = forms.ChoiceField(
        choices=COUNTRY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'firstname', 'lastname']  # noqa: RUF012

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists(): 
            raise ValidationError("An account with this email already exists.")
        if Person.objects.filter(user__email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email
    
class PersonUpdateForm(forms.ModelForm):
    
    HOBBIE_CHOICES = [  # noqa: RUF012
            ('Cricket', 'Cricket'),
            ('Football', 'Football'),
            ('Hockey', 'Hockey'),
            ('Bowling', 'Bowling'),
            ('Basketball', 'Basketball'),
        ]
    
    hobbies = forms.MultipleChoiceField(
        choices=HOBBIE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = Person
        fields = ['number', 'hobbies', 'dob', 'gender', 'country']  # noqa: RUF012
        
        widgets = {  # noqa: RUF012
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.RadioSelect(),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
                    
        if self.instance and self.instance.hobbies:
            self.initial['hobbies'] = [h.strip() for h in self.instance.hobbies.split(',') if h.strip()]

    def clean_hobbies(self):
        hobbies_list = self.cleaned_data.get('hobbies')
        
        if hobbies_list:
            return ",".join(hobbies_list)
        
        return ""