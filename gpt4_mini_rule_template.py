import json

from openai import OpenAI
from key import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def init_boardgame(number_of_players, game_duration, description_of_background, game_category, game_mechanics):
    with open('rule_template_category.json') as json_data:
        rule_template_categories = json.load(json_data)
    category_features = json.dumps(rule_template_categories[game_category])

    with open('rule_template_mechanics.json') as json_data:
        rule_template_mechanics = json.load(json_data)
    filtered_mechanics = {}
    for game_mechanic in game_mechanics:
        filtered_mechanics[game_mechanic] = rule_template_mechanics[game_mechanic]
    game_mechanics_requirements = json.dumps(filtered_mechanics)

    system_context_init = f'''
    You are co-creativity assistant to help design a board game.
    
    The category of this game is: {game_category}. Fearures of this category of game are: {category_features}.
    
    The mechanics of this game are: {game_mechanics}. Elements and requirements for each mechanic are: {game_mechanics_requirements}.

    You will be provided with some settings: 
    1. number of players
    2. game duration
    3. description of background

    Based on these settings, generate a background story and detailed game rules. Category and mechanics must follow the requirement so that player can play the game directly according to the rules.

    Provide your output in json format with the keys:
    1. name
    2. background
    3. rules
    4. players
    '''
    print(f"*** system_context_init: \n {system_context_init}")

    assistant_context_init = '''
    1. name: 
    Pandemic Legacy

    2. background:
    Pandemic Legacy is a co-operative campaign game, with an overarching story arc played through 12-24 sessions, depending on how well your group does at the game. At the beginning, the game starts in a very similar fashion as basic Pandemic, in which your team of disease-fighting specialists races against the clock to travel around the world, treating disease hot spots while researching cures for each of four plagues before they get out of hand

    3. rules
    During a player's turn, they have four actions available, with which they may travel around in the world in various ways (sometimes needing to discard a card), build structures like research stations, treat diseases (removing one cube from the board; if all cubes of a color have been removed, the disease has been eradicated), trade cards with other players, or find a cure for a disease (requiring five cards of the same color to be discarded while at a research station). Each player has a unique role with special abilities to help them at these actions. After a player has taken their actions, they draw two cards. These cards can include epidemic cards, which will place new disease cubes on the board, and can lead to an outbreak, spreading disease cubes even further. Outbreaks additionally increase the panic level of a city, making that city more expensive to travel to. Each month in the game, you have two chances to achieve that month's objectives. If you succeed, you win and immediately move on to the next month. If you fail, you have a second chance, with more funding for beneficial event cards. During the campaign, new rules and components will be introduced. These will sometimes require you to permanently alter the components of the game; this includes writing on cards, ripping up cards, and placing permanent stickers on components. Your characters can gain new skills, or detrimental effects. A character can even be lost entirely, at which point it's no longer available for play. Part of the Pandemic serie.

    4. players:
    dispatcher, medic, scientist, researcher, operations expert, contingency planner, quarantine specialist
    '''

    user_context_init_json = {
        "number_of_players": number_of_players,
        "game_duration": game_duration,
        "description_of_background": description_of_background
    }
    user_context_init = json.dumps(user_context_init_json)
    print(f"*** user_context_init: \n {user_context_init}")

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
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
    )
    print(f"*** response: \n {completion.choices[0].message.content}")
    response_content = completion.choices[0].message.content

    file_path = "return/board_game_theme_fantacy.md"
    with open(file_path, "w") as file:
        file.write(response_content)

    return response_content


def follow_up(init_content):
    # Add the follow-up question
    follow_up_question = "Can you provide more detailed rules for combat mechanics, including dice usage, special abilities, and damage calculation?"

    # Build the conversation history
    conversation_history = [
        {
            "role": "system",
            "content": '''
            You are co-creativity assistant to help design a board game.

            You will be provided with some settings:
            [Settings description here as before.]
            Based on these settings, generate a background story and detailed game rules.

            Provide your output in JSON format with the keys:
            1. name
            2. background
            3. rules
            4. players
            '''
        },
        {
            "role": "user",
            "content": json.dumps({
                "number_of_players": 4,
                "game_duration": "1-2 hours",
                "description_of_background": "adventure happens on a mysterious island",
                "game_category": ["adventure"],
                "game_mechanics": ["Action and Turn Management", "Dice and Randomness", "Player Interaction"]
            })
        },
        {
            "role": "assistant",
            "content": '''
            {
              "background": "In the heart of the Forgotten Seas lies a mysterious island...",
              "rules": { /* Initial rules from the first output */ },
              "players": { /* Initial player roles and characters */ }
            }
            '''
        },
        {
            "role": "user",
            "content": follow_up_question
        }
    ]

    # Send the follow-up question to the API
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history
    )

    # Print and save the updated response
    response = completion.choices[0].message.content
    print(response)

    # Save to a markdown file
    with open("board_game_followup.md", "w") as file:
        file.write(response)


if __name__ == "__main__":
    number_of_players = 4
    game_duration = "1-2 hours"
    description_of_background = "adventure happen on a mysterious island"
    game_category = "adventure"
    game_mechanics = ["Action and Turn Management", "Dice and Randomness", "Player Interaction"]

    init_content = init_boardgame(number_of_players, game_duration, description_of_background, game_category, game_mechanics)
    # follow_up(init_content)

