from arenas.models import Arena

ARENAS = [
    {"name": "State Farm Arena", "team": "Atlanta Hawks", "latitude": 33.7573, "longitude": -84.3963},
    {"name": "TD Garden", "team": "Boston Celtics", "latitude": 42.3662, "longitude": -71.0621},
    {"name": "Barclays Center", "team": "Brooklyn Nets", "latitude": 40.6826, "longitude": -73.9754},
    {"name": "Spectrum Center", "team": "Charlotte Hornets", "latitude": 35.2251, "longitude": -80.8392},
    {"name": "United Center", "team": "Chicago Bulls", "latitude": 41.8807, "longitude": -87.6742},
    {"name": "Rocket Arena", "team": "Cleveland Cavaliers", "latitude": 41.4965, "longitude": -81.6882},
    {"name": "American Airlines Center", "team": "Dallas Mavericks", "latitude": 32.7905, "longitude": -96.8104},
    {"name": "Ball Arena", "team": "Denver Nuggets", "latitude": 39.7487, "longitude": -105.0077},
    {"name": "Little Caesars Arena", "team": "Detroit Pistons", "latitude": 42.3410, "longitude": -83.0552},
    {"name": "Chase Center", "team": "Golden State Warriors", "latitude": 37.7680, "longitude": -122.3877},
    {"name": "Toyota Center", "team": "Houston Rockets", "latitude": 29.7508, "longitude": -95.3621},
    {"name": "Gainbridge Fieldhouse", "team": "Indiana Pacers", "latitude": 39.7640, "longitude": -86.1555},
    {"name": "Intuit Dome", "team": "LA Clippers", "latitude": 33.9533, "longitude": -118.3391},
    {"name": "Crypto.com Arena", "team": "LA Lakers / LA Clippers", "latitude": 34.0430, "longitude": -118.2673},
    {"name": "FedExForum", "team": "Memphis Grizzlies", "latitude": 35.1382, "longitude": -90.0506},
    {"name": "Kaseya Center", "team": "Miami Heat", "latitude": 25.7814, "longitude": -80.1870},
    {"name": "Fiserv Forum", "team": "Milwaukee Bucks", "latitude": 43.0451, "longitude": -87.9172},
    {"name": "Target Center", "team": "Minnesota Timberwolves", "latitude": 44.9795, "longitude": -93.2760},
    {"name": "Smoothie King Center", "team": "New Orleans Pelicans", "latitude": 29.9490, "longitude": -90.0821},
    {"name": "Madison Square Garden", "team": "New York Knicks", "latitude": 40.7505, "longitude": -73.9934},
    {"name": "Paycom Center", "team": "Oklahoma City Thunder", "latitude": 35.4634, "longitude": -97.5151},
    {"name": "Kia Center", "team": "Orlando Magic", "latitude": 28.5392, "longitude": -81.3839},
    {"name": "Wells Fargo Center", "team": "Philadelphia 76ers", "latitude": 39.9012, "longitude": -75.1720},
    {"name": "PHX Arena", "team": "Phoenix Suns", "latitude": 33.4457, "longitude": -112.0712},
    {"name": "Moda Center", "team": "Portland Trail Blazers", "latitude": 45.5316, "longitude": -122.6668},
    {"name": "Golden 1 Center", "team": "Sacramento Kings", "latitude": 38.5802, "longitude": -121.4997},
    {"name": "Frost Bank Center", "team": "San Antonio Spurs", "latitude": 29.4269, "longitude": -98.4375},
    {"name": "Scotiabank Arena", "team": "Toronto Raptors", "latitude": 43.6435, "longitude": -79.3791},
    {"name": "Delta Center", "team": "Utah Jazz", "latitude": 40.7683, "longitude": -111.9011},
    {"name": "Capital One Arena", "team": "Washington Wizards", "latitude": 38.8981, "longitude": -77.0209},
]

for arena in ARENAS:
    Arena.objects.create(**arena)