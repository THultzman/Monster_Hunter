import sys
import ItemClass
import PlayerClass as PC
from MonsterClass import gen_ran_pos


class Npc:
    def __init__(self, name, symbol, npc_type, position, hidden, found):
        self.name = name
        self.symbol = symbol
        self.npc_type = npc_type
        self.position = position
        self.hidden = hidden
        self.found = found

        self.inventory = []
        self.gold = 1000


def tradeItem():
    sell_buy = input("Would you like to [sell] or [buy]? else just [leave]! > ").lower()

    if sell_buy == "exit":
        sys.exit()
    elif sell_buy == "leave":
        pass

    elif sell_buy == "buy":

        print("\nExcellent! Here's what I have:\n")

        for attr in sorted(the_trader.inventory, key=lambda obj: obj.rarity):

            if attr.rarity in ["Normal", "Rare", "Unique"]:
                print(f"{attr.name}:")

                print("-------------")

                print(f"Damage: {attr.damage} \n"

                      f"Defence: {attr.defence} \n"

                      f"HP: {attr.health} \n"

                      f"Rarity: {attr.rarity} \n"

                      f"Price: {attr.value}\n")

        buy_item = input("Which item would you like to buy? > ")
        for i in the_trader.inventory:
            if i.name == buy_item:
                if PC.char.gold >= i.value:
                    PC.char.gold -= i.value
                    PC.char.inventory.append(i)
                    print("\nItem added to your inventory.")
                else:
                    print("\nYou don't have enough gold for that item.")

            elif i.name != buy_item:
                pass
            else:
                print("\nI don't know what you're saying")

    elif sell_buy == "sell":
        sell_item = input("\nWhat is it that you would like to sell? > ")
        for i in PC.char.inventory:
            try:
                if i.name == sell_item:
                    the_trader.inventory.append(i)
                    PC.char.inventory.remove(i)
                    PC.char.gold += i.value
                    print("Pleasure to do business with you.")
                    print(f"{i.value} gold added to your sack")
                elif i.name != sell_item:
                    print("\nYou don't have that item in your backpack.")
                else:
                    print("\nI don't understand.")
            except AttributeError:
                pass


def healing():
    heal = input("Welcome to my shack, I can heal you for a small price if you want. [y/n] > ")
    if heal == "y":
        if PC.char.hp >= 100:
            print("You're in a great shape, I can't heal you.")
        else:
            bonus_hp = 0
            for i in PC.char.equipped_items:
                try:
                    item = PC.char.equipped_items[i]
                    bonus_hp += item.health
                except AttributeError:
                    bonus_hp += 0
            healing_need = (100 - PC.char.hp) + bonus_hp

            healing_cost = healing_need / 5
            rounded_cost = round(healing_cost, 2)
            get_healed = input(f"It will cost you {rounded_cost} gold. Deal? [y/n] > ")
            if get_healed == "y":
                if PC.char.gold >= rounded_cost:
                    PC.char.gold -= rounded_cost
                    PC.char.hp += healing_need
                    print("All of your wounds magically disappear...")
                else:
                    print("You don't have enough gold for that.")
            else:
                print("Stop wasting my time!")
    else:
        print("Stop wasting my time!")


def sellSpell():
    buy_spell = input('"Do not meddle in the affairs of Wizards, for they are subtle and quick to anger"\n'
                      'So... Wanna buy some spells? [y/n] > ')
    if buy_spell == "exit":
        sys.exit()

    elif buy_spell == "y":
        print("----------------")
        print("Wizard Inventory")
        for spell in the_wizard.inventory:
            print(f"Spell:       {spell.name}\n"
                  f"Description: {spell.description}\n"
                  f"Price:       {spell.value}")
        print("----------------")

        buy_item = input("Which spell would you like to buy? > ")
        for i in the_wizard.inventory:
            if i.name == buy_item:
                if PC.char.gold >= i.value:
                    PC.char.gold -= i.value
                    PC.char.inventory.append(i)
                    print("\nItem added to your inventory.")
                else:
                    print("\nYou don't have enough gold for that item.")

            elif i.name != buy_item:
                pass
            else:
                print("\nI don't know what you're saying")

    else:
        print("What a waste of time...")


def upgradeItem():
    upgradeMultiplier = 5
    print("Welcome to my blacksmith shop traveller. We can upgrade most items!"
          " For a cost of course..(Lvl 1 upgrades are free)")
    print("")
    print("Your gold: " + str(PC.char.gold))
    print("")
    print("Items in Inventory")
    print("---------------------")

    it = False
    slit = None
    invlist = []
    for obj in PC.char.inventory:  # Looping through player inventory and inserting into a new table
        if obj.name != "Fire Ball": #YOU REALLY NEED TO MAKE SPELLS A SEPERATE DICT AND NOT IN INVENTORY DICT
            invlist.append(obj)
            print(obj.name + " Lvl: " + str(obj.u_times))  # Displaying inventory choices
    selitem = input("Selected Item >")
    print("")
    for k in invlist:
        if selitem == str.lower(k.name):  # Finding selected item in inventory
            it = True
            slit = k  # Putting the specific object from inventory into slit (selected item)
    if it:  # If the item they input matches a item in their inventory continue
        if PC.char.gold >= slit.u_times * upgradeMultiplier:  # Checking if they have enough gold
            if slit.i_type == "Weapon":
                if slit.u_times >= 10:  # If the item is already at max return
                    print("Your item is already maxed out!")
                else:
                    PC.char.gold = PC.char.gold - (slit.u_times * upgradeMultiplier)
                    slit.u_times += 1  # Adding to multiplier
                    slit.damage = slit.u_times * slit.defdamage  # Damage of weapon is default damage times multiplier
                    slit.damage = ((slit.defdamage * .5) * 2) + slit.damage  # Adding .5 times default damage for Defense and Magic
                    print("Here is your upgraded item!")
            elif slit.i_type == ("Shield" or "Helmet") or "Chest":
                if slit.u_times >= 10:
                    print("Your item is already maxed out!")
                else:
                    PC.char.gold = PC.char.gold - (slit.u_times * upgradeMultiplier)
                    slit.u_times += 1
                    slit.defence = slit.u_times * slit.defdefence
                    slit.defence = ((slit.defdefence * .5) * 2) + slit.defence
                    print("Here is your upgraded item!")
            else:
                print("Can't upgrade magic items!")  # Unless you want the blacksmith to be able to
        else:
            print("You don't have enough gold!")
    else:
        print("Can't find that item!")


# Create an NPC
the_trader = Npc("The Mystical Trader", "T", "Trader", gen_ran_pos(), " ", False)
the_trader.gold = 1000

the_healer = Npc("The Healer", "H", "Healer", gen_ran_pos(), " ", False)

the_wizard = Npc("The Wizard", "W", "Wizard", gen_ran_pos(), " ", False)

the_blacksmith = Npc("The Blacksmith", "B", "Blacksmith", 1, " ", False)

# Give items to an NPC
# Normal
the_trader.inventory.append(ItemClass.leather_cap)
the_trader.inventory.append(ItemClass.leather_armour)
the_trader.inventory.append(ItemClass.iron_helmet)
the_trader.inventory.append(ItemClass.iron_shield)
the_trader.inventory.append(ItemClass.iron_armour)
the_trader.inventory.append(ItemClass.iron_sword)
# Rare
the_trader.inventory.append(ItemClass.dragon_plate)
the_trader.inventory.append(ItemClass.half_moon_katana)
# Unique
the_trader.inventory.append(ItemClass.one_hit_wonder)

# Wizard/Spells
the_wizard.inventory.append(ItemClass.fire_ball)

# Dictionary holding NPC functions
npc_func_dict = {
    the_trader: tradeItem,
    the_healer: healing,
    the_wizard: sellSpell,
    the_blacksmith: upgradeItem,
}
