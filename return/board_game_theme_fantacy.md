```json
{
  "background": "In the heart of the Forgotten Seas lies a mysterious island, shrouded in fog and legends of ancient treasures. Adventurers from across the realms gather at the shores, lured by tales of enchanted relics said to grant unimaginable power. However, the island harbors dark secrets and hidden dangers. The explorers must navigate through treacherous landscapes, fend off fierce creatures, and outsmart each other as they embark on perilous quests. But beware! Among the adventurers, there are those with secret agendas – traitors who seek to sabotage their efforts for their own gain. Only through cunning strategy and teamwork can the true treasure be unearthed. Will you survive the island’s trials and emerge as the champion of legends or will you fall victim to the shadows lurking within?",
  "rules": {
    "setup": {
      "players": "Each player selects a character with unique abilities.",
      "island_map": "Create the island map with unexplored areas and point of interest markers.",
      "treasure_tokens": "Place treasure tokens randomly across the map.",
      "role_card": "Shuffle the hidden role cards and distribute one to each player face down."
    },
    "turn_structure": {
      "action_phase": {
        "each_turn": {
          "players": "Take turns in clockwise order.",
          "actions": [
            "Move: Players may move to an adjacent area.",
            "Explore: Players can explore their current location for treasure or encounter events.",
            "Fight: Engage in combat with creatures or other players.",
            "Strategize: Use hand management to execute special abilities."
          ]
        }
      },
      "reveal_phase": {
        "end_of_turn": "Players can choose to reveal or hide their roles, creaing tension and strategy."
      }
    },
    "victory_conditions": {
      "treasure_collection": "The first player to collect a set amount of treasure tokens is declared the winner.",
      "elimination": "Alternatively, players can win by eliminating all other adventurers."
    },
    "hidden_roles": {
      "sabotage": "Traitors have special abilities that allow them to hinder other players' progress.",
      "victory_for_traitors": "If all loyal adventurers are eliminated, the traitors win."
    }
  },
  "players": {
    "player_characters": [
      "Warrior: Strong in battle, excels at combat tasks.",
      "Rogue: Quick and stealthy, can sneak past enemies or players.",
      "Mage: Uses magic for powerful spells, useful in combat and exploration.",
      "Ranger: Expert tracker, can identify creature weaknesses and gain advantages."
    ],
    "player_roles": [
      "Loyal Adventurer: Work to collect treasure and aid allies.",
      "Traitor: Deceive and sabotage the adventurers while appearing innocent."
    ]
  }
}
```