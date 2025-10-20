from enum import Enum

class Constants(Enum):
    # Ingredients
    Nightrose = 0
    Whisperthorn = 1
    Frostblossom = 2
    Sunfire_Lily = 3
    Powdered_Moonstone = 4
    Obsidian_Ash = 5
    Phoenix_Feather_Dust = 6
    Whispleaf = 7
    Bottled_Echos = 8
    Glowing_Mushroom = 9
    # Potions
    Water = {"id":1,"color":"ice", "sell":5}
    Garbage = {"id":2,"color":"gargreen"}
    Remove_Rust = {"id":3,"color":"grey"}
    Create_Flowers = {"id":4, "color":"lgreen"}
    Heating = {"id":5,"color":"orange"}
    Cooling = {"id":6,"color":"ice"}
    Levitation = {"id":7,"color":"purple"}
    Light_Poison = {"id":8,"color":"green"}
    Heavy_Poison = {"id":9,"color":"dgreen"}
    Spicy = {"id":10,"color":"red"}
    Sleep = {"id":11,"color":"dpurple"}
    Acid = {"id":12,"color":"red"}
    Indigestion = {"id":13,"color":"dgreen"}
    Digestion = {"id":14,"color":"green"}
    Energy = {"id":15,"color":"yellow"}
    Teleportation = {"id":16,"color":"purple"}
    Electricity = {"id":17,"color":"yellow"}
    Enlargement = {"id":18,"color":"lgreen"}
    Shrinking = {"id":19,"color":"pink"}
    Mold_Removal = {"id":20,"color":"dgreen"}
    Rusting = {"id":21,"color":"dred"}
    Stickiness = {"id":22,"color":"dgreen"}
    Slight_Invisibility = {"id":23,"color":"grey"}
    Invisibility = {"id":24,"color":"white"}
    Second_Thoughts = {"id":25,"color":"blue"}
    Insect_Fighting_Bravery = {"id":26,"color":"dgreen"}
    Memory_Enhancement = {"id":27,"color":"purple"}
    Speed = {"id":28,"color":"lblue"}
    Slowness = {"id":29,"color":"black"}
    Hearing = {"id":30,"color":"yellow"}
    Instant_Freezing = {"id":31,"color":"ice"}
    Fire = {"id":32,"color":"orange"}
    Fire_Resistance = {"id":33,"color":"orange"}
    Regeneration = {"id":34,"color":"pink"}
    Power_Amplification = {"id":35,"color":"red"}
    Shadow = {"id":36,"color":"black"}
    Silencing = {"id":37,"color":"yellow"}
    Echoing = {"id":38,"color":"yellow"}
    Whispering = {"id":39,"color":"blue"}
    Frostburn = {"id":40,"color":'green'}
    Glowing = {"id":41,"color":'yellow'}
    # Effects
    Fire_Resisting = {"id":1, "length":3, "outcome":None}
    Poisoned = {"id":2, "length":5, "outcome":"death"}
    #!PLACEHOLDER = {"id":3, "length":2, "outcome":"death"}
    Silenced = {"id":3, "length":4, "outcome":None}
    Regenerating = {"id":4, "length":2, "outcome":None}
    Slowed = {"id":5, "length":4, "outcome":None}
    Quickened = {"id":6, "length":3, "outcome":None}
    Invisible = {"id":7, "length":3, "outcome":None}
class Combinations():
    combinations = {
        'Nightrose':{
            'Bottled Echos':None,
            'Nightrose':Constants.Shadow,
            'Whisperthorn':Constants.Silencing,
            'Frostblossom':None,
            'Sunfire_Lily':Constants.Fire,
            'Powdered_Moonstone':None,
            'Obsidian_Ash':Constants.Second_Thoughts,
            'Phoenix_Feather_Dust':Constants.Rusting,
            'Whispleaf':Constants.Slowness,
            'Glowing_Mushroom':None},
        'Bottled_Echos':{
            'Bottled Echos':Constants.Hearing,
            'Nightrose':None,
            'Whisperthorn':Constants.Sleep,
            'Frostblossom':None,
            'Sunfire_Lily':None,
            'Powdered_Moonstone':Constants.Echoing,
            'Obsidian_Ash':Constants.Teleportation,
            'Phoenix_Feather_Dust':Constants.Energy,
            'Whispleaf':None,
            'Glowing_Mushroom':Constants.Speed},
        'Whisperthorn':{
            'Bottled Echos':Constants.Sleep,
            'Nightrose':Constants.Silencing,
            'Whisperthorn':Constants.Whispering,
            'Frostblossom':None,
            'Sunfire_Lily':Constants.Heating,
            'Powdered_Moonstone':None,
            'Obsidian_Ash':Constants.Heavy_Poison,
            'Phoenix_Feather_Dust':None,
            'Whispleaf':Constants.Light_Poison,
            'Glowing_Mushroom':Constants.Shrinking},
        'Frostblossom':{
            'Bottled Echos':None,
            'Nightrose':None,
            'Whisperthorn':None,
            'Frostblossom':Constants.Instant_Freezing,
            'Sunfire_Lily':Constants.Frostburn,
            'Powdered_Moonstone':Constants.Cooling,
            'Obsidian_Ash':None,
            'Phoenix_Feather_Dust':None,
            'Whispleaf':Constants.Electricity,
            'Glowing_Mushroom':Constants.Stickiness},
        'Sunfire_Lily':{
            'Bottled Echos':None,
            'Nightrose':Constants.Fire,
            'Whisperthorn':Constants.Heating,
            'Frostblossom':Constants.Frostburn,
            'Sunfire_Lily':Constants.Fire_Resistance,
            'Powdered_Moonstone':Constants.Spicy,
            'Obsidian_Ash':Constants.Insect_Fighting_Bravery,
            'Phoenix_Feather_Dust':Constants.Levitation,
            'Whispleaf':None,
            'Glowing_Mushroom':None},
        'Powdered_Moonstone':{
            'Bottled Echos':None,
            'Nightrose':None,
            'Whisperthorn':None,
            'Frostblossom':Constants.Cooling,
            'Sunfire_Lily':Constants.Spicy,
            'Powdered_Moonstone':Constants.Slight_Invisibility,
            'Obsidian_Ash':Constants.Indigestion,
            'Phoenix_Feather_Dust':None,
            'Whispleaf':Constants.Invisibility,
            'Glowing_Mushroom':None},
        'Obsidian_Ash':{
            'Bottled Echos':Constants.Teleportation,
            'Nightrose':Constants.Second_Thoughts,
            'Whisperthorn':Constants.Heavy_Poison,
            'Frostblossom':None,
            'Sunfire_Lily':Constants.Insect_Fighting_Bravery,
            'Powdered_Moonstone':Constants.Indigestion,
            'Obsidian_Ash':Constants.Memory_Enhancement,
            'Phoenix_Feather_Dust':None,
            'Whispleaf':None,
            'Glowing_Mushroom':Constants.Mold_Removal},
        'Phoenix_Feather_Dust':{
            'Bottled Echos':Constants.Energy,
            'Nightrose':Constants.Rusting,
            'Whisperthorn':None,
            'Frostblossom':None,
            'Sunfire_Lily':Constants.Levitation,
            'Powdered_Moonstone':None,
            'Obsidian_Ash':None,
            'Phoenix_Feather_Dust':Constants.Power_Amplification,
            'Whispleaf':Constants.Digestion,
            'Glowing_Mushroom':Constants.Enlargement},
        'Whispleaf':{
            'Nightrose':Constants.Slowness,
            'Bottled Echos':None,
            'Whisperthorn':Constants.Light_Poison,
            'Frostblossom':Constants.Electricity,
            'Sunfire_Lily':None,
            'Powdered_Moonstone':Constants.Invisibility,
            'Obsidian_Ash':None,
            'Phoenix_Feather_Dust':Constants.Digestion,
            'Whispleaf':Constants.Create_Flowers,
            'Glowing_Mushroom':Constants.Regeneration},
        'Glowing_Mushroom': {
            'Nightrose':None,
            'Bottled Echos':Constants.Speed,
            'Whisperthorn':Constants.Shrinking,
            'Frostblossom':Constants.Stickiness,
            'Sunfire_Lily':None,
            'Powdered_Moonstone':None,
            'Obsidian_Ash':Constants.Mold_Removal,
            'Phoenix_Feather_Dust':Constants.Enlargement,
            'Whispleaf':Constants.Regeneration,
            'Glowing_Mushroom':Constants.Glowing},
    }