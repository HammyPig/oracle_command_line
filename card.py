class Card:

    def __init__(self, name, description, type):
        self.name = name
        self.description = description
        self.type = type

    def __repr__(self):
        return f"{self.name}"

class Attack(Card):

    def use(self, caster, target):
        old_target_health = target.health
        target.health -= 1
        print(f"Player {caster.name} used {self.name} on player {target.name}, reducing their health from {old_target_health} to {target.health}!")
