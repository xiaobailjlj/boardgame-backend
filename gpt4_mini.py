import json

from openai import OpenAI
from key import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def init_boardgame():
    system_context_init = '''
    You are co-creativity assistant to help design a board game.

    You will be provided with some settings: 
    1. number of players
    2. game duration
    3. description of background
    4. game categories
    5. game mechanics
    categories and mechanics can be combination of:
    All Categories: ['abstract_strategy', 'adventure', 'age_of_reason', 'american_west', 'ancient', 'animals', 'bluffing', 'card_game', 'city_building', 'civilization', 'deduction', 'dice', 'economic', 'educational', 'environmental', 'exploration', 'fantasy', 'farming', 'fighting', 'humor', 'industry_/_manufacturing', 'medical', 'medieval', 'miniatures', 'modern_warfare', 'mythology', 'nautical', 'negotiation', 'novel-based', 'number', 'party_game', 'political', 'post-napoleonic', 'puzzle', 'religious', 'renaissance', 'science_fiction', 'space_exploration', 'spies_/_secret_agents', 'territory_building', 'trains', 'transportation', 'travel', 'wargame', 'word_game']
    All Mechanics: ['action_/_event', 'action_drafting', 'action_points', 'action_queue', 'action_retrieval', 'advantage_token', 'area_majority_/_influence', 'area_movement', 'auction:_dutch', 'auction_/_bidding', 'automatic_resource_growth', 'campaign_/_battle_card_driven', 'card_play_conflict_resolution', 'catch_the_leader', 'chaining', 'closed_drafting', 'communication_limits', 'contracts', 'cooperative_game', 'deck,_bag,_and_pool_building', 'deduction', 'delayed_purchase', 'dice_rolling', 'enclosure', 'end_game_bonuses', 'events', 'finale_ending', 'follow', 'force_commitment', 'grid_coverage', 'grid_movement', 'hand_management', 'hexagon_grid', 'hidden_roles', 'hidden_victory_points', 'income', 'increase_value_of_unchosen_resources', 'investment', 'kill_steal', 'king_of_the_hill', 'layering', 'legacy_game', 'loans', 'map_addition', 'market', 'modular_board', 'movement_points', 'multi-use_cards', 'narrative_choice_/_paragraph', 'negotiation', 'network_and_route_building', 'once-per-game_abilities', 'open_drafting', 'ownership', 'paper-and-pencil', 'pattern_building', 'player_elimination', 'point_to_point_movement', 'push_your_luck', 'race', 'random_production', 'resource_to_move', 'roles_with_asymmetric_information', 'rondel', 'scenario_/_mission_/_campaign_game', 'score-and-reset_game', 'set_collection', 'simulation', 'simultaneous_action_selection', 'solo_/_solitaire_game', 'square_grid', 'storytelling', 'sudden_death_ending', 'tags', 'take_that', 'targeted_clues', 'team-based_game', 'tech_trees_/_tech_tracks', 'tile_placement', 'track_movement', 'trading', 'traitor_game', 'trick-taking', 'tug_of_war', 'turn_order:_claim_action', 'turn_order:_pass_order', 'turn_order:_progressive', 'turn_order:_stat-based', 'turn_order:_time_track', 'variable_phase_order', 'variable_player_powers', 'variable_set-up', 'victory_points_as_a_resource', 'voting', 'worker_placement', 'worker_placement,_different_worker_types', 'zone_of_control']

    Based on these settings, generate a background story and detailed game rules.

    Provide your output in json format with the keys:
    1. name
    2. background
    3. rules
    4. players
    '''

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
        "number_of_players": 4,
        "game_duration": "1-2 hours",
        "description_of_background": "adventure happen on a mysterious island",
        "game_categories": ["adventure", "fantasy", "fighting"],
        "game_mechanics": ["catch_the_leader", "hand_management", "hidden_roles"]
    }
    user_context_init = json.dumps(user_context_init_json)

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
    # print(completion.choices[0].message)
    print(completion.choices[0].message.content)
    response_content = completion.choices[0].message.content

    file_path = "return/example.md"
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
                "game_categories": ["adventure", "fantasy", "fighting"],
                "game_mechanics": ["catch_the_leader", "hand_management", "hidden_roles"]
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
    init_content = init_boardgame()
    follow_up(init_content)

