import copy
import json

from openai import OpenAI
from key import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def init_boardgame(rule_id, number_of_players, game_duration, description_of_background, game_category, game_mechanics):
    print("********** init_boardgame **********")
    with open('rule_template_category.json') as json_data:
        rule_template_categories = json.load(json_data)
    category_features = json.dumps(rule_template_categories[game_category])

    with open('rule_template_mechanics.json') as json_data:
        rule_template_mechanics = json.load(json_data)
    filtered_mechanics = {}
    for game_mechanic in game_mechanics:
        filtered_mechanics[game_mechanic] = rule_template_mechanics[game_mechanic]
    game_mechanics_requirements = json.dumps(filtered_mechanics)

    player_format = json.dumps({"number_of_players": 4, "roles": [
        {"name": "The Medic", "ability": "Negotiate for additional healing resources."},
        {"name": "The Strategist", "ability": "Plan ambushes against rival factions."},
        {"name": "The Diplomat", "ability": "Negotiate more favorable trades during alliances."}]})

    system_context_init = f'''
    You are co-creativity assistant to help design a board game.

    The category of this game is: {game_category}. Fearures of this category of game are: {category_features}.

    The mechanics of this game are: {game_mechanics}. Elements and requirements for each mechanic are: {game_mechanics_requirements}.

    You will be provided with some settings: 
    1. number of players
    2. game duration
    3. description of background

    Based on these settings, generate a background story and detailed game rules. Category and mechanics must follow the requirement so that player can play the game directly according to the rules.

    Provide your output in json format with the keys, all keys in the json should be lowercase:
    1. name
    2. background
    3. rules
    4. players, format: {player_format}
    
    After generating the output, evaluate and validate for self-check, but don't return the evaluate and validate result:
    1. Does the game follow the category features?
    2. Are the mechanics fully utilized with unique player actions?
    3. Does the background match the theme?
    4. Is the output json format aligned with the provided example?
    '''


    assistant_context_init = f'''
    1. name:
    Pandemic Legacy

    2. background:
    Pandemic Legacy is a co-operative campaign game, with an overarching story arc played through 12-24 sessions, depending on how well your group does at the game. At the beginning, the game starts in a very similar fashion as basic Pandemic, in which your team of disease-fighting specialists races against the clock to travel around the world, treating disease hot spots while researching cures for each of four plagues before they get out of hand

    3. rules
    During a player's turn, they have four actions available, with which they may travel around in the world in various ways (sometimes needing to discard a card), build structures like research stations, treat diseases (removing one cube from the board; if all cubes of a color have been removed, the disease has been eradicated), trade cards with other players, or find a cure for a disease (requiring five cards of the same color to be discarded while at a research station). Each player has a unique role with special abilities to help them at these actions. After a player has taken their actions, they draw two cards. These cards can include epidemic cards, which will place new disease cubes on the board, and can lead to an outbreak, spreading disease cubes even further. Outbreaks additionally increase the panic level of a city, making that city more expensive to travel to. Each month in the game, you have two chances to achieve that month's objectives. If you succeed, you win and immediately move on to the next month. If you fail, you have a second chance, with more funding for beneficial event cards. During the campaign, new rules and components will be introduced. These will sometimes require you to permanently alter the components of the game; this includes writing on cards, ripping up cards, and placing permanent stickers on components. Your characters can gain new skills, or detrimental effects. A character can even be lost entirely, at which point it's no longer available for play. Part of the Pandemic serie.

    4. players:
    {player_format}
    '''

    user_context_init_json = {
        "number_of_players": number_of_players,
        "game_duration": game_duration,
        "description_of_background": description_of_background
    }
    user_context_init = json.dumps(user_context_init_json)

    message = [
        {
            "role": "system",
            "content": system_context_init,
        },
        {
            "role": "assistant",
            "content": assistant_context_init,
        },
        {
            "role": "user",
            "content": user_context_init
        }
    ]

    print(f"*** message_init: \n {message}")

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=message
    )
    response_content_raw = completion.choices[0].message.content
    print(f"*** response: \n {response_content_raw}")
    cleaned_content = response_content_raw.strip('```json').strip('```').strip()
    response_content = json.loads(cleaned_content)

    print(f"*** saving rule_id: {rule_id}")
    file_path_init = "return/board_game_id_" + str(rule_id) + "_init.json"
    with open(file_path_init, 'w') as f:
        json.dump(response_content, f)
    file_path_follow = "return/board_game_id_" + str(rule_id) + "_follow.json"
    with open(file_path_follow, 'w') as f:
        json.dump(response_content, f)
    print(f"*** saving rule_id: {rule_id}, success")

    return response_content


def follow_up(rule_id, file_path_follow, follow_instructions):
    print("********** updating_boardgame **********")
    with open(file_path_follow) as json_data:
        init_content = json.load(json_data)

    player_format = json.dumps({"number_of_players": 4, "roles": [
        {"name": "The Medic", "ability": "Negotiate for additional healing resources."},
        {"name": "The Strategist", "ability": "Plan ambushes against rival factions."},
        {"name": "The Diplomat", "ability": "Negotiate more favorable trades during alliances."}]})

    system_context_follow = f'''
    You are co-creativity assistant to help design a board game.
    You have been provided with the initial game rules. You are now required to provide more details for the game.

    The initial game is:
    {json.dumps(init_content)}

    Combine the initial game and the details, provide your output in json format with the keys, all keys in the json should be lowercase:
    1. name
    2. background
    3. rules
    4. players, format: {player_format}
    
    After generating the output, evaluate and validate for self-check, but don't return the evaluate and validate result:
    1. Is the output json format aligned with the provided example?
    '''

    assistant_context_follow = f'''
    1. name:
    Pandemic Legacy

    2. background:
    Pandemic Legacy is a co-operative campaign game, with an overarching story arc played through 12-24 sessions, depending on how well your group does at the game. At the beginning, the game starts in a very similar fashion as basic Pandemic, in which your team of disease-fighting specialists races against the clock to travel around the world, treating disease hot spots while researching cures for each of four plagues before they get out of hand

    3. rules
    During a player's turn, they have four actions available, with which they may travel around in the world in various ways (sometimes needing to discard a card), build structures like research stations, treat diseases (removing one cube from the board; if all cubes of a color have been removed, the disease has been eradicated), trade cards with other players, or find a cure for a disease (requiring five cards of the same color to be discarded while at a research station). Each player has a unique role with special abilities to help them at these actions. After a player has taken their actions, they draw two cards. These cards can include epidemic cards, which will place new disease cubes on the board, and can lead to an outbreak, spreading disease cubes even further. Outbreaks additionally increase the panic level of a city, making that city more expensive to travel to. Each month in the game, you have two chances to achieve that month's objectives. If you succeed, you win and immediately move on to the next month. If you fail, you have a second chance, with more funding for beneficial event cards. During the campaign, new rules and components will be introduced. These will sometimes require you to permanently alter the components of the game; this includes writing on cards, ripping up cards, and placing permanent stickers on components. Your characters can gain new skills, or detrimental effects. A character can even be lost entirely, at which point it's no longer available for play. Part of the Pandemic serie.

    4. players:
    {player_format}
    '''

    message = [
        {
            "role": "system",
            "content": system_context_follow
        },
        {
            "role": "user",
            "content": follow_instructions
        },
        {
            "role": "assistant",
            "content": assistant_context_follow
        }
    ]
    print(f"*** message_follow: \n {message}")

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=message
    )

    response_content_raw = completion.choices[0].message.content
    print(f"*** response: \n {response_content_raw}")
    cleaned_content = response_content_raw.strip('```json').strip('```').strip()
    response_content = json.loads(cleaned_content)

    print(f"*** saving rule_id: {rule_id}")
    with open(file_path_follow, 'w') as f:
        json.dump(response_content, f)
    print(f"*** saving rule_id: {rule_id}, success")

    return response_content


def start_game(rule_id, file_path_rule, player_role):

    print("********** start game **********")
    with open(file_path_rule) as json_data:
        game_context = json.load(json_data)

    system_context = f'''
    You are co-creativity assistant to help design a board game.
    You have been provided with the game rules. Now you have to accompany the players to try out this game.
    Player will choose a role to start the game.
    You are required to a guide to the player's first action.

    The game is:
    {json.dumps(game_context)}

    Provide your output in json format with the keys, all keys in the json should be lowercase:
    1. name
    2. player_role
    3. history (now it's empty)
    4. next_action (a guide to the player's first action)
        for instance:
        choice 1: Roll a D20 dice to determine the starting food resource of the player.
        choice 2: Move forward to the nearest food resource.
        choose: roll a D20 dice or move forward
        
    After generating the output, evaluate and validate for self-check, but don't return the evaluate and validate result:
    1. Is the output json format aligned with the provided example?
    '''

    # assistant_context = '''
    # 1. name
    #
    # 2. player_role
    #
    # 3. history: []
    #
    # 4. next_action: (just an example)
    # choice 1: Roll a dice to determine the starting food resource of the player.
    # choice 2: Move forward to the nearest food resource.
    # choose: roll a dice or move forward
    # '''

    message = [
        {
            "role": "system",
            "content": system_context
        },
        {
            "role": "user",
            "content": player_role
        },
        # {
        #     "role": "assistant",
        #     "content": assistant_context
        # }
    ]
    print(f"*** message: \n {message}")

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=message
    )

    response_content_raw = completion.choices[0].message.content
    print(f"*** response: \n {response_content_raw}")
    cleaned_content = response_content_raw.strip('```json').strip('```').strip()
    response_content = json.loads(cleaned_content)

    file_path_follow = "return/board_game_id_" + str(rule_id) + "_history.json"
    with open(file_path_follow, 'w') as f:
        json.dump(response_content, f)

    return response_content


def game_round(rule_id, file_path_rule, file_path_history, round_id, action):
    with open(file_path_rule) as json_data:
        game_context = json.load(json_data)

    with open(file_path_history) as json_data:
        game_history = json.load(json_data)

    pure_history_all = game_history['history']
    print(f"*** pure_history_all: {pure_history_all}")
    pure_history_previous = []
    for history in pure_history_all:
        print (f"*** history: {history}")
        if history['round'] == round_id-1:
            pure_history_previous.append(history)

    game_history_only_previous = copy.deepcopy(game_history)
    game_history_only_previous['history'] = pure_history_previous

    print("********** next round **********")

    history_example = json.dumps([{"round": 1, "actions": [
        {"player": "Warrior", "action": "Move", "description": "Alice moved to the Jungle Clearing.", "cost": 1,
         "result": "Fail"}, {"player": "Explorer", "action": "Explore",
                                "description": "Bob explored an Ancient Ruin and found a treasure map.", "cost": 2,
                                "result": "Success - Treasure Map acquired."},
        {"player": "Scholar", "action": "Rest", "description": "Carol rested to recover 2 health points.", "cost": 1,
         "result": "Success - Health restored to 8."},
        {"player": "Trader", "action": "Engage", "description": "Dave engaged an enemy lurking in the Forest Trail.",
         "cost": 3, "result": "Failure - Took 3 damage."}], "events": [{"type": "Environment Change",
                                                                        "description": "A storm begins, reducing visibility for all players in open areas."}]},
                                  {"round": 2, "actions": [{"player": "Warrior", "action": "Explore",
                                                            "description": "Alice explored a cave and discovered a hidden passage.",
                                                            "cost": 2,
                                                            "result": "Critical Success - Hidden passage revealed!"},
                                                           {"player": "Explorer", "action": "Trade",
                                                            "description": "Bob traded the treasure map with Carol for a health potion.",
                                                            "cost": 1, "result": "Fail"},
                                                           {"player": "Scholar", "action": "Engage",
                                                            "description": "Carol fought a Giant Spider in the cave.",
                                                            "cost": 3,
                                                            "result": "Success - Spider defeated, gained 3 XP."},
                                                           {"player": "Trader", "action": "Strategize",
                                                            "description": "Dave used his ability to grant Bob an extra action.",
                                                            "cost": 2,
                                                            "result": "Success - Bob gains 1 additional action."}],
                                   "events": [{"type": "Quest Triggered",
                                               "description": "The group unlocked the 'Lost Artifact' quest by finding the hidden passage."}]}])

    system_context = f'''
    You are co-creativity assistant to help design a board game.
    Now you have to accompany the players to try out this game. The game is in the middle, you have been provided with the game rules, the role of the player, and game history. The current round is {round_id}.
    The action of player is for this round. You are required to :
    1. generate other player's action in this round, write to history of this round, other players are in the game context.
    2. provide a guide to the player's next action for next round.

    The game context is:
    {json.dumps(game_context)}

    The game history is:
    {json.dumps(game_history_only_previous)}

    Provide your output in json format with the keys, all keys in the json should be lowercase:
    1. name
    2. player_role
    3. history, for instance: {history_example}, you can only return the history of this round
    4. next_action (a guide to the player's next action)
    
    After generating the output, evaluate and validate for self-check, but don't return the evaluate and validate result:
    1. Is the output json format aligned with the provided example?
    '''

    assistant_context = json.dumps(game_history_only_previous)

    message = [
        {
            "role": "system",
            "content": system_context
        },
        {
            "role": "user",
            "content": action
        },
        {
            "role": "assistant",
            "content": assistant_context
        }
    ]
    print(f"*** message: \n {message}")

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=message
    )

    response_content_raw = completion.choices[0].message.content
    print(f"*** response: \n {response_content_raw}")
    cleaned_content = response_content_raw.strip('```json').strip('```').strip()
    response_content = json.loads(cleaned_content)
    pure_history_current = response_content['history']
    for history in game_history['history']:
        if history['round'] == round_id:
            game_history['history'].remove(history)
    for history in pure_history_current:
        if history['round'] == round_id:
            game_history['history'].append(history)


    with open(file_path_history, 'w') as f:
        json.dump(game_history, f)

    return response_content


if __name__ == "__main__":
    # number_of_players = 3
    # game_duration = "3-4 hours"
    # description_of_background = "Fight for medical resources in plague cities"
    # game_category = "bluffing"
    # game_mechanics = ["Dice and Randomness", "Player Interaction"]
    #
    # init_content = init_boardgame(number_of_players, game_duration, description_of_background, game_category, game_mechanics)

    # with open('return/board_game_name_Resource Wars: Plague Survivors_follow.json') as json_data:
    #     init_content = json.load(json_data)
    #
    # follow_instructions = 'Provide more detailed rules for dice.'
    # follow_content = follow_up(init_content, follow_instructions)

    # with open('return/board_game_name_Resource Wars: Plague Survivors_follow.json') as json_data:
    #     game_context = json.load(json_data)

    # player_role = "The Medic"
    # history = start_game(player_role, game_context)

    # with open('return/board_game_name_Resource Wars: Plague Survivors_history.json') as json_data:
    #     game_history = json.load(json_data)
    rule_id = 1736115427
    action = "influence"
    round_id = 3
    file_path_rule = "return/board_game_id_1736115427_follow.json"
    file_path_history = "return/board_game_id_1736115427_history.json"
    history = game_round(rule_id, file_path_rule, file_path_history, round_id, action)








