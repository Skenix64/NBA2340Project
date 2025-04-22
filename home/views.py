from django.shortcuts import render

def homepage(request):
    return render(request, 'home/index.html')

def player_search_view(request):
    query = request.GET.get('q', '')
    players = Player.objects.filter(name__icontains=query) if query else []

    context = {
        'query': query,
        'players': players,
    }
    return render(request, 'home/player_search.html', context)

def team_search_view(request):
    query = request.GET.get('q', '')
    teams = Team.objects.filter(name__icontains=query) if query else []

    context = {
        'query': query,
        'teams': teams,
    }
    return render(request, 'home/team_search.html', context)