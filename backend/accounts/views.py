from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth.tokens import default_token_generator


from .forms import PersonUpdateForm, UserRegistrationForm
from .models import Person


class HomePage(TemplateView):
    template_name = 'home.html'
    
class LoginView(TemplateView):
    template_name = 'login'
    
class ProfileDetailView(LoginRequiredMixin, DetailView):
    template_name = 'profile_detail.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        """Fetches the Person profile belonging to the logged-in user dynamically."""
        return self.request.user.person
    
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PersonUpdateForm
    template_name = 'profile_edit.html'
    success_url = reverse_lazy('profile_edit_success')

    def get_object(self, queryset=None):
        """Fetches the Person profile belonging to the logged-in user dynamically."""
        return self.request.user.person
    
class UserRegistrationView(FormView):
    template_name = 'register_form.html'  
    form_class = UserRegistrationForm
    success_url = reverse_lazy('register_success')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = form.cleaned_data['email'] 
        user.first_name = form.cleaned_data['firstname']
        user.last_name = form.cleaned_data['lastname']
        user.set_password(form.cleaned_data['password'])
        user.is_active = False 
        user.save()

        hobbies_list = form.cleaned_data.get('hobbies', [])

        Person.objects.create(
            user=user,
            number=form.cleaned_data['number'],
            hobbies=",".join(hobbies_list), 
            dob=form.cleaned_data['dob'],
            gender=form.cleaned_data['gender'],
            country=form.cleaned_data['country']
        )
        
        token = default_token_generator.make_token(user)

     
        user_email = form.cleaned_data['email']
        domain = "http://127.0.0.1:8000"
        
        path = reverse('activate_user', kwargs={'user_id': user.pk, 'token': token}) 
        activation_link = domain + path
        
        print("\n" + "="*80)
        print(f"ACTIVATION LINK: {activation_link}")
        print("="*80 + "\n")
        
        email_message = f"Click here to verify your account: {activation_link}"

        email = EmailMessage(
            subject="Verify Your Account",
            body=email_message,
            from_email="your-email@gmail.com",
            to=[user_email],
        )
        email.send(fail_silently=False)
                
        return super().form_valid(form)

class VerifyUser(TemplateView):
    template_name = 'success.html' 
    
    def get(self, request, *args, **kwargs):
        User = get_user_model()
        user_id = self.kwargs.get('user_id') 
        token = self.kwargs.get('token') 
    
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return HttpResponse("User not found.", status=404)
            
        if not default_token_generator.check_token(user, token):
            return HttpResponse("This activation link is invalid or has expired.", status=400)
        
                    
        user.is_active = True
        user.save()
            
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verified_message'] = "Your Email is VERIFIED, Now User is able to LOGIN!"
        return context


class RegistrationSuccessView(TemplateView):
    template_name = 'success.html' 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['custom_message'] = """Your account was successfully created! Now, Verify the account and Login. Link sended to your mail."""
        
        return context
    

class ProfileUpdateSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['custom_message'] = "Your profile details have been updated successfully!"
        return context
    

@login_required
def profile_redirect(request):
    return redirect('profile_detail', pk=request.user.person.pk)




