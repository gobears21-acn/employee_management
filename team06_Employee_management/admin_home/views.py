from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def admin_home(request):
    return render(request, 'admin_home/home.html')