class Continued:
    def investigate(inventoryList:list, printed:list, key=""):
                    if key in inventoryList:
                        match inventoryList[key]:
                            case 'Apple':
                                printed.append("It appears to be a red, spherical object.")
                            case 'Chicken Nugget':
                                printed.append("It is a yellow food made from chicken. You wonder who put it here.")
                            case 'Golden Blåhaj Statue':
                                printed.append("It is a golden statue representing Blåhaj.")
                            case 'Red Amulet':
                                printed.append("It appears to have many symbols engraved onto it, and is made out of red stone.")
                            case 'Fire Resistance Amulet':
                                printed.append("It appears to have many symbols engraved onto it, and is made out of red stone.")
                            case 'Carrot':
                                printed.append("It is orange and conical.")
                            case 'Lantern':
                                printed.append("It appears to be a battery powered lantern. You wonder how they got the batteries.")
                            case 'Arnav Statue':
                                printed.append("It is a statue of a familiar figure.")
                            case 'Water Walking Boots':
                                printed.append("It is blue, and is very comfortable.")
                            case 'Blue Boots':
                                printed.append("It is blue, and is very comfortable.")
                            case 'Water Bottle':
                                printed.append("It is certaintly water.")
                            case 'Cloak':
                                printed.append("It's just some thin fabric, and it's not very strong.")
                            case _:
                                if "Potion" in inventoryList[key]:
                                    printed.append("It is some sort of liquid.")
                    return printed
    def wear(inventoryList:list, inventory:list, printed:list, equipped:list, items_list:list, turn:int, key):
        try:
        #if 1==1:
            if (inventoryList[key] in items_list['equippable']) or (inventoryList[key] in items_list['amulet']):
                    for i in range(len(inventory)):
                        if inventory[i][0] == inventoryList[key]:
                            inventory[i][4][3] = 1 - inventory[i][4][3]
                            if inventoryList[key] not in equipped:
                                equipped.append(inventoryList[key])
                            else:
                                equipped.pop(equipped.index(inventoryList[key]))
            else:
                printed.append("You cannot equip that.")
                turn -= 5
        except Exception:
            turn -= 5
        return inventory, printed, equipped, turn
    def eat(inventory:list, ALPHABET:str, items_hunger:dict, hunger_points:int, printed:list, turn:int, key):
        try:
        #if 1==1:
            idx = 0
            items_list = {}
            for item in inventory:
                items_list[ALPHABET[idx]] = item
                idx += 1
            match items_list[key][2]:
                case -1:
                    x = 0.8
                case 0:
                    x = 1
                case 1:
                    x = 1.2
                case _:
                    x = 0.1
            hunger_points += round(x * items_hunger[items_list[key][0]])
            idx = inventory.index(items_list[key])
            if inventory[idx][1] == 1:
                inventory.pop(idx)
            else: inventory[idx][1] -= 1
        except Exception:
            printed.append("You cannot eat that.")
            turn -= 1
        return inventory, hunger_points, turn
    def drink(inventory:list, ALPHABET:str, printed:list, hunger_points:int, turn:int, items_info:dict, key):
        try:
        #if 1==1:
            idx = 0
            items_list = {}
            for item in inventory:
                items_list[ALPHABET[idx]] = item
                idx += 1
            if item[0] not in items_info["potions"]:
                    printed.append("You cannot drink that.")
            else:
                match items_list[key][2]:
                    case -1:
                        x = 0.8
                    case 0:
                        x = 1
                    case 1:
                        x = 1.2
                    case _:
                        x = 0.1
                match items_list[key][0]:
                    case "Water Bottle":
                        thirst = 20
                    case "Fruit Juice":
                        thirst = 15
                    case _:
                        thirst = 5
                hunger_points += round(x * thirst)
                idx = inventory.index(items_list[key])
                if inventory[idx][1] == 1:
                    inventory.pop(idx)
                else: inventory[idx][1] -= 1
        except:
            printed.append("You cannot drink that.")
            turn -= 1
        return inventory, printed, hunger_points, turn
    def floor_one(printed:list, location:list, kb, key:str = "") -> None:
                            if type(key) != kb.Key:
                                if key.strip().lower() == "y":
                                    location = [99999, 99999]
                                    return False, printed, location
                                else:
                                    printed.append("You decide that would be a bad idea.")
                                    return True, printed, location