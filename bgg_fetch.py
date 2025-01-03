import json

import requests
from xml.etree import ElementTree


def fetch_game_details(game_id):
    url = f"https://boardgamegeek.com/xmlapi2/thing?id={game_id}&stats=1"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch data for game ID {game_id}")
        return None

    # Parse XML response
    tree = ElementTree.fromstring(response.content)
    item = tree.find("item")

    if not item:
        print(f"No data found for game ID {game_id}")
        return None

    # Extract details
    title = item.find("name[@type='primary']").get("value", "Unknown")
    description = item.find("description").text.strip()
    min_players = item.find("minplayers").get("value")
    max_players = item.find("maxplayers").get("value")
    playing_time = item.find("playingtime").get("value")
    age = item.find("minage").get("value")
    weight = item.find(".//averageweight").get("value")

    categories = [
        link.get("value")
        for link in item.findall("link[@type='boardgamecategory']")
    ]
    mechanics = [
        link.get("value")
        for link in item.findall("link[@type='boardgamemechanic']")
    ]

    return {
        "title": title,
        "description": description,
        "players": f"{min_players}-{max_players}",
        "playing_time": playing_time,
        "age": age,
        "weight": weight,
        "categories": categories,
        "mechanics": mechanics,
    }


# Example usage
game_ids = {
    174430,  # Gloomhaven
    167791,  # Terraforming Mars
    224517,  # Brass: Birmingham
    12333,   # Twilight Struggle
    182028,  # Through the Ages: A New Story of Civilization
    187645,  # Star Wars: Rebellion
    169786,  # Scythe
    220308,  # Gaia Project
    162886,  # Spirit Island
    193738,  # Great Western Trail
    173346,  # 7 Wonders Duel
    161936,  # Pandemic Legacy: Season 1
    115746,  # War of the Ring (Second Edition)
    183394,  # Viticulture Essential Edition
    237182,  # Root
    124361,  # Concordia
    72125,   # Eclipse
    164928,  # Orléans
    84876,   # The Castles of Burgundy
    31260,   # Agricola
    201808,  # Clank!: A Deck-Building Adventure
    266192,  # Wingspan
    230802,  # Azul
    199792,  # Everdell
    244521,  # The Quacks of Quedlinburg
    170042,  # Raiders of the North Sea
    178900,  # Codenames
    148228,  # Splendor
    68448,   # 7 Wonders
    36218,   # Dominion
    9209,    # Ticket to Ride
    822,     # Carcassonne
    30549,   # Pandemic
    128882,  # The Resistance: Avalon
    204583,  # Kingdomino
    163412,  # Patchwork
    133473,  # Sushi Go!
    129622,  # Love Letter
    98778,   # Hanabi
    244992,  # The Mind
    39856,   # Dixit
    13,      # Catan
    3076,    # Puerto Rico
    2651,    # Power Grid
    40834,   # Dominion: Intrigue
    312484,  # Lost Ruins of Arnak
    284083,  # The Crew: The Quest for Planet Nine
    225694,  # Decrypto
    254640,  # Just One
    256043   # Terraforming Mars: Prelude
}

def dump_json():
    game_details = []
    for id in game_ids:  # Replace with a valid game ID (e.g., 13 for Catan)
        details = fetch_game_details(id)
        if details:
            game_detail = {
                "id": id,
                "title": details["title"],
                "description": details["description"],
                "players": details["players"],
                "playing_time": details["playing_time"],
                "age": details["age"],
                "weight": details["weight"],
                "categories": details["categories"],
                "mechanics": details["mechanics"],
            }
            game_details.append(game_detail)

    with open(f"game_geek.json", "w", encoding="utf-8") as json_file:
        json.dump(game_details, json_file, ensure_ascii=False, indent=4)

def normalize(text):
    return text.lower().replace(" ", "_")

def collect_game_details():
    all_categories = set()
    all_mechanics = set()

    for id in game_ids:
        details = fetch_game_details(id)
        if details:
            normalized_categories = [normalize(cat) for cat in details["categories"]]
            normalized_mechanics = [normalize(mech) for mech in details["mechanics"]]
            all_categories.update(normalized_categories)
            all_mechanics.update(normalized_mechanics)

    print("All Categories:", sorted(all_categories))
    print("All Mechanics:", sorted(all_mechanics))

collect_game_details()