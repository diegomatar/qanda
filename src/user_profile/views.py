from django.contrib.auth.models import User
from django.shortcuts import render

from .forms import EditProfileForm
from .models import UserProfile

# Create your views here.

def user_profile(request):
    
    user_data = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user_data)
        if form.is_valid:
            form_add = form.save()
    else:
        form = EditProfileForm(instance=user_data)
    
    context ={
        'user': user_data,
        'form': form,
    }
    return render(request, 'user_profile/profile.html', context)

