from django.shortcuts import render
from admin_search.models import CustomUser

def user_search(request):
    query = request.GET.get('q')
    if query:
        users = CustomUser.objects.filter(username__icontains=query)[:20]
    else:
        users = CustomUser.objects.all()[:20]
    return render(request, 'user_search/user_search.html', {'users': users})

def welcome(request):
    return render(request, '/welcome.html')

def team(request):
    return render(request, 'team.html')