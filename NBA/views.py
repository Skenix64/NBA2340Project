from django.shortcuts import render
from NBA.services.NBAStatsService import NBAStatsService
from NBA.services.player import Player  # if you use it

def player_search_view(request):
    if request.method == "POST":
        name = request.POST.get("player_name")
        stats_service = NBAStatsService()
        try:
            response = stats_service.get_player_info(name)
            # You can also parse it here using json.loads(response)
            return render(request, "player_result.html", {"data": response})
        except Exception as e:
            return render(request, "player_result.html", {"error": str(e)})

    return render(request, "player_form.html")
