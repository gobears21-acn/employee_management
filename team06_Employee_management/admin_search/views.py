from django.shortcuts import render, get_object_or_404, redirect
from .forms import CustomUserCreationForm
from .models import CustomUser
from team.models import Team, TeamMember

def admin_search(request):
    query = request.GET.get('q')
    if query:
        users = CustomUser.objects.filter(username__icontains=query)
    else:
        users = CustomUser.objects.all()[:20]
    return render(request, 'admin_search/admin_search.html', {'users': users})

def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    user.delete()
    return redirect('admin_search')


def add_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_search')
    else:
        form = CustomUserCreationForm()
    return render(request, 'admin_search/add_user.html', {'form': form})