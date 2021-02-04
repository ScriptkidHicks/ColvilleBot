
class character:

    def __init__(self, name: str):
        self.name = name
        self.level = None
        self.charClass = None
        self.age = None
        self.player = None
        self.hp = None
        self.inspiration = False
        self.proficiencyBonus = None

        self.attributes = {"str": None, "dex": None, "con": None, "int": None, "wis": None, "cha": None}

        self.attributeBonuses = {"str": None, "dex": None, "con": None, "int": None, "wis": None, "cha": None}

        self.saves = {"str": None, "dex": None, "con": None, "int": None, "wis": None, "cha": None}

        self.skills = {"athletics": None, "acrobatics": None, "sleightofhand": None, "stealth": None,
                       "arcana": None, "history": None, "religion": None, "nature": None, "investigation": None,
                       "animalhandling": None, "insight": None, "medicine": None, "perception": None,
                       "survival": None, "persuasion": None, "deception": None, "intimidation": None,
                       "performance": None}

    def updateAttribute(self, attribute, value):
        self.attributes[attribute] = value

    def updateAttributeBonus(self, attribute, bonus):
        self.attributeBonuses[attribute] = bonus

    def updateSkill(self, skill, bonus):
        self.attributes[skill] = bonus

    def updateSave(self, save, boolean):
        self.saves[save] = boolean

    def UpdateCharacter(self):
        if self.proficiencyBonus is None:
            return None

        for attribute in self.attributes:
            if self.attributes[attribute] is not None:
                self.attributeBonuses[attribute] = (self.attributes[attribute] - 10)// 2
