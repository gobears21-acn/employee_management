from django.shortcuts import render, get_object_or_404
from .models import Team, TeamMember

def team_page(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    team_members = TeamMember.objects.filter(team=team).order_by('-is_leader')
    context = {
        'team': team,
        'team_members': team_members,
    }
    return render(request, 'team_page.html', context)