from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from django.contrib.auth.models import User

from user_profile.models import UserProfile

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a
        social provider, but before the login is actually processed
        (and before the pre_social_login signal is emitted).

        We're trying to solve different use cases:
        - social account already exists, just go on
        - social account has no email or email is unknown, just go on
        - social account's email exists, link social account to existing user
        """

        # Ignore existing social accounts, just do this stuff for new ones
        if sociallogin.is_existing:
            return

        # some social logins don't have an email address, e.g. facebook accounts
        # with mobile numbers only, but allauth takes care of this case so just
        # ignore it
        if 'email' not in sociallogin.account.extra_data:
            return

        # check if given email address already exists.
        # Note: __iexact is used to ignore cases
        try:
            print 'print 1'
            email = sociallogin.account.extra_data['email'].lower()
            existing_user = User.objects.get(email__iexact=email)
            perfil = existing_user.userprofile
            email_address = existing_user.email
            #email_address = EmailAddress.objects.get(email__iexact=email)

        # if it does not, let allauth take care of this new social account
        except User.DoesNotExist:
            return
        
        '''
        # Populate user profile with social data:
        if sociallogin.account.provider == 'facebook':
            perfil.facebook = sociallogin.account.get_profile_url()
            perfil.save()
        
        if sociallogin.account.provider == 'twitter':
            perfil.twitter = sociallogin.account.get_profile_url()
            perfil.save()
            
        if sociallogin.account.provider == 'google':
            perfil.google = sociallogin.account.get_profile_url()
            perfil.save()
        '''

        # if it does, connect this new social login to the existing user
        user = existing_user
        sociallogin.connect(request, user)
        
        
        
        
        
        