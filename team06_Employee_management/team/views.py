from django.shortcuts import render, get_object_or_404
from .models import CustomUser, Team, TeamMember

def team(request):
    query = request.GET.get('team_identifier')
    if query:
        team = get_object_or_404(Team, team_identifier=query)
        members = TeamMember.objects.filter(team=team).select_related('user')
    else:
        members = []
    return render(request, 'team/team.html', {'members': members, 'query': query})