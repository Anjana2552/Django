# Custom allauth adapter to integrate with your CustomUser model
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import perform_login
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    
    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a
        social provider, but before the login is actually processed.
        """
        # Check if user exists with this email
        if sociallogin.account.provider == 'google':
            email = sociallogin.account.extra_data.get('email')
            if email:
                try:
                    # Try to find existing user with this email
                    existing_user = User.objects.get(email=email)
                    # Connect this social account to existing user
                    sociallogin.connect(request, existing_user)
                except User.DoesNotExist:
                    pass
    
    def save_user(self, request, sociallogin, form=None):
        """
        Saves a newly signed up social login. 
        """
        user = sociallogin.user
        user.set_unusable_password()
        
        # Set user role as 'user' by default for social logins
        user.role = 'user'
        
        # Get additional info from Google
        if sociallogin.account.provider == 'google':
            extra_data = sociallogin.account.extra_data
            user.first_name = extra_data.get('given_name', '')
            user.last_name = extra_data.get('family_name', '')
            
        user.save()
        return user
        
    def get_login_redirect_url(self, request):
        """
        Returns the default URL to redirect to after logging in.
        """
        return '/dashboard/user/'