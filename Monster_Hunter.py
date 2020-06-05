# Monster_Hunter Development Ver 1.8.2
import sys
import pickle

# Game imports
import GameBoard
import CombatSystem
import PlayerClass
import MonsterClass
import ItemClass
import NPCClass
from MonsterClass import gen_ran_pos


def startGame():
    # player_info is a tuple -> ([char stats], player_name)
    player_info = PlayerClass.createCharacter()
    PlayerClass.char.player = player_info[1]
    PlayerClass.char.strength = player_info[0][0]
    PlayerClass.char.defence = player_info[0][1]
    PlayerClass.char.dexterity = player_info[0][2]
    PlayerClass.char.intelligence = player_info[0][3]
    PlayerClass.char.magic = player_info[0][4]

    GameBoard.draw_board(GameBoard.theBoard)
    gameAction()


def printHelp():
    print("\nAvailable Menu Commands:\n"
          "help         Display help menu\n"
          "start        Start the game\n"
          "exit         Exit the game\n\n"
          "\nAvailable Game Commands:\n"
          "help         Display help menu\n"
          "exit         Exit the game\n"
          "item stats   View stats of an item\n"
          "player stats View player statistics\n"
          "equip        Allows to equip an item\n"
          "unequip      Allows to unequip an item\n"
          "save         Saves the game\n"
          "load         Loads the save\n"
          "inventory    Check your inventory\n\n"
          "up           Move up\n"
          "down         Move down\n"
          "left         Move left\n"
          "right        Move right\n")


def menuAction():
    """
    Hold a dictionary with available commands in the menu of the game
    """
    menu_action_dict = {
        "help": printHelp, "start": startGame, "exit": sys.exit, "load": loadSave,
    }
    menu = True
    while menu:
        menu_action = input("What would you like to do? > ")
        if menu_action in menu_action_dict:
            menu_action_dict[menu_action]()
            if menu_action == 'load':
                gameAction()

        else:
            print("Unknown command...")


def gameAction():
    """
    This function holds a game action dictionary, which maps valid user inputs to either other functions
    or converts player movement to equivalent integers. For example: If the player wants to move up the board,
    it has to add 10 to the current position of the player, if the player wants to move left it has to minus 1
    from the current position.
    """
    game_action_dict = {
        "help": printHelp, "exit": sys.exit, "inventory": PlayerClass.char.show_inventory,
        "item stats": ItemClass.showStats, "save": makeSave, "load": loadSave,
        "equip": ItemClass.equip, "unequip": ItemClass.unequip, "player stats": PlayerClass.char.showStats,
        "up": 10, "down": -10, "left": -1, "right": 1
    }
    valid_move = False
    while not valid_move:
        game_action = input("\n> ")
        if game_action in game_action_dict:
            # Try calling a function, if the action is not a function, catch the exception and pass it to makeMove()
            try:
                game_action_dict[game_action]()
            except TypeError:
                makeMove(game_action_dict[game_action])
                valid_move = True
        else:
            print("Unknown command...")


def makeMove(move):
    """
    This function defines movement on the board. When a player makes a move, it first moves the player to the new
    position, because now there are two instances of the player on board, it erases the previous position with
    an empty string -> ' '.

    Once the movements are complete, it updates the player object.player_position with the new pos. It then draws the
    board and loops back to take the gameAction() function to take the player input again.
    """
    try:
        # Place the player in a new position
        GameBoard.theBoard[PlayerClass.char.position + move] = PlayerClass.char.name
        # Reset the current position to empty
        GameBoard.theBoard[PlayerClass.char.position] = " "
        # Update player position to the new position
        PlayerClass.char.position = PlayerClass.char.position + move
    except IndexError:
        print("Out of bounds.")

    checkEncounters()
    GameBoard.draw_board(GameBoard.theBoard)
    gameAction()


def npcEncounter():
    for npc in NPCClass.npc_func_dict:
        if PlayerClass.char.position == npc.position:
            print("--------------------------------------")
            print(f"\nYou found an NPC! {npc.name}\n")
            npc.found = True
            NPCClass.npc_func_dict[npc]()
        if npc.found:
            GameBoard.theBoard[npc.position] = npc.symbol
        else:
            GameBoard.theBoard[npc.position] = npc.hidden


def checkEncounters():
    # This function checks for any encounters on the board between the player/monster/item.

    npcEncounter()
    # All items that are on the board are in the on_board_items list. If player pos == item pos -> find item.
    for i in ItemClass.on_board_items:
        if not i.found:
            if PlayerClass.char.position == i.position:
                i.found = True
                print("You found something!")
                PlayerClass.char.add_item(i)
                print(f"{i.name} was added to your inventory")
        else:
            pass

    # For every orc in the army, if the orc pos is same as player pos, but not defeated, discover the monster
    for orc in MonsterClass.army_of_orcs:
        if orc.defeated:
            pass
        else:
            if orc.position == PlayerClass.char.position:
                print("\nYou found the monster!")
                print(f"The {orc.name}")
                orc.found = True

                fight_flee = input("\nDo you want to fight? [y/n] > ")
                if fight_flee == "y":
                    GameBoard.theBoard[orc.position] = orc.symbol
                    CombatSystem.battle(orc)

                elif fight_flee == "n":
                    pass
                else:
                    print("You stutter something as you run away in fear...")
    # If an orc is found, leave a symbol on the board
    for orc in MonsterClass.army_of_orcs:
        if orc.found:
            GameBoard.theBoard[orc.position] = orc.symbol
        if orc.defeated:
            if PlayerClass.char.position == orc.position:
                GameBoard.theBoard[orc.position] = PlayerClass.char.name
            else:
                GameBoard.theBoard[orc.position] = " "

    if MonsterClass.orc_boss.defeated:
        print("You killed the boss, you win!")
        sys.exit()
    else:
        if MonsterClass.orc_boss.position == PlayerClass.char.position:
            print("\nYou found the Destroyer Orc!")
            print("Be careful, he's not like the other Orcs!")
            MonsterClass.orc_boss.found = True

            boss_fight = input("\nDo you want to fight the boss? [y/n] > ")
            if boss_fight == "y":
                GameBoard.theBoard[MonsterClass.orc_boss.position] = MonsterClass.orc_boss.symbol
                CombatSystem.battle(MonsterClass.orc_boss)

            elif boss_fight == "n":
                pass
            else:
                print("You stutter something as you run away in fear...")
    if MonsterClass.orc_boss.found:
        GameBoard.theBoard[MonsterClass.orc_boss.position] = MonsterClass.orc_boss.symbol


def makeSave():
    inventory_list = []
    for obj in PlayerClass.char.inventory:
        inventory_list.append(obj)

    save_dict = {
        # --- Player --- #
        "player_pos": PlayerClass.char.position,
        "player_inventory": inventory_list,
        "player_spellbag": PlayerClass.char.spellbag,
        "player_eq": PlayerClass.char.equipped_items,
        "player_hp": PlayerClass.char.hp,
        "player_gold": PlayerClass.char.gold,
        "player_xp": PlayerClass.char.xp,
        "player_lvl": PlayerClass.char.level,
        "player_def": PlayerClass.char.defence,
        "player_str": PlayerClass.char.strength,
        "player_dex": PlayerClass.char.dexterity,
        "player_int": PlayerClass.char.intelligence,
        "player_mag": PlayerClass.char.magic,
        # --- NPC --- #
        "trader_pos": NPCClass.the_trader.position,
        "trader_found": NPCClass.the_trader.found,
        "healer_pos": NPCClass.the_healer.position,
        "healer_found": NPCClass.the_healer.found,
        "wizard_pos": NPCClass.the_wizard.position,
        "wizard_found": NPCClass.the_wizard.found,
        "blacksmith_pos": NPCClass.the_blacksmith.position,
        "blacksmith_found": NPCClass.the_blacksmith.found,
        # --- Items --- #
        "board_items": ItemClass.on_board_items
    }
    # --- Monsters (1 - 9) --- #
    for i in range(0, 9):
        save_dict[f'monster{i + 1}'] = MonsterClass.army_of_orcs[i]

    pickle.dump(save_dict, open("save.p", "wb"))


def loadSave():
    load_dict = pickle.load(open("save.p", "rb"))

    # --- Player --- #
    # First reset old position to -> " "
    GameBoard.theBoard[PlayerClass.char.position] = " "
    # Now the position is updated
    PlayerClass.char.position = load_dict['player_pos']
    # Now place the player
    GameBoard.theBoard[PlayerClass.char.position] = PlayerClass.char.name

    PlayerClass.char.spellbag = load_dict['player_spellbag']
    PlayerClass.char.inventory = load_dict['player_inventory']
    PlayerClass.char.equipped_items = load_dict['player_eq']
    PlayerClass.char.hp = load_dict['player_hp']
    PlayerClass.char.gold = load_dict['player_gold']
    PlayerClass.char.xp = load_dict['player_xp']
    PlayerClass.char.lvl = load_dict['player_lvl']
    PlayerClass.char.defence = load_dict['player_def']
    PlayerClass.char.strength = load_dict['player_str']

    # --- NPC --- #
    # Set Found
    NPCClass.the_trader.found = load_dict['trader_found']
    NPCClass.the_healer.found = load_dict['healer_found']
    NPCClass.the_blacksmith.found = load_dict['blacksmith_found']
    NPCClass.the_wizard.found = load_dict['wizard_found']
    # Now the position is updated
    NPCClass.the_trader.position = load_dict['trader_pos']
    NPCClass.the_wizard.position = load_dict['wizard_pos']
    NPCClass.the_blacksmith.position = load_dict['blacksmith_pos']
    NPCClass.the_healer.position = load_dict['healer_pos']

    # --- Monsters --- #
    MonsterClass.army_of_orcs = []

    # Separate all monsters
    for i in range(1, 10):
        loaded = load_dict[f'monster{i}']
        MonsterClass.army_of_orcs += [MonsterClass.Monster("Bald Orc", "m", loaded.position, " ", loaded.found, loaded.hp, 32, 2, loaded.defeated, MonsterClass.gen_orc_gold(), 49)]

    # Place saved monsters on the board
    for monster in MonsterClass.army_of_orcs:
        if monster.found:
            GameBoard.theBoard[monster.position] = monster.symbol
        else:
            GameBoard.theBoard[monster.position] = monster.hidden

    # --- Items --- #
    # First reset on_board_items
    ItemClass.on_board_items = []
    GameBoard.theBoard[ItemClass.leather_cap.position] = " "
    # If item is already found, pass, else add the item to on_board_items, replace on the board and make hidden
    for i in load_dict['board_items']:
        if not i.found:
            ItemClass.on_board_items.append(i)
            GameBoard.theBoard[i.position] = i.hidden

    # First check encounters, then draw the board accordingly and finally run gameAction for the player to start.
    checkEncounters()
    GameBoard.draw_board(GameBoard.theBoard)
    gameAction()


def main():
    # Place player on position 0
    GameBoard.theBoard[PlayerClass.char.position] = PlayerClass.char.name

    # Place orcs in random positions
    for orc in MonsterClass.army_of_orcs:
        GameBoard.theBoard[orc.position] = orc.hidden

    # Boss
    GameBoard.theBoard[99] = MonsterClass.orc_boss.symbol

    # Place NPC
    for orc in MonsterClass.army_of_orcs:
        for npc in NPCClass.npc_func_dict:
            GameBoard.theBoard[npc.position] = npc.hidden
            while npc.position == orc.position:
                npc.position = gen_ran_pos()

    # Give player a wooden stick and a wooden shield ( + Spell for testing )
    PlayerClass.char.equipped_items["Weapon"] = ItemClass.wooden_stick
    PlayerClass.char.inventory.append(ItemClass.wooden_shield)

    # Temporary spell added to inventory for testing
    PlayerClass.char.inventory.append(ItemClass.fire_ball)

    # Place some normal items around the board
    GameBoard.theBoard[ItemClass.leather_armour.position] = ItemClass.leather_armour.hidden
    GameBoard.theBoard[ItemClass.leather_cap.position] = ItemClass.leather_cap.hidden

    print("\nWelcome to Monster_Hunter.\n\n"
          "Kill monsters, gather gold, buy better\n"
          "equipment and battle with the boss.\n\n"
          "Available Commands:\n\n"
          "help     Display help menu\n"
          "start    Start the game\n"
          "load     Load last save\n"
          "exit     Exit the game\n")
    menuAction()


if __name__ == '__main__':
    main()

# Contributions to project:
# Co-authored-by: torbray <66016078+torbray@users.noreply.github.com>
