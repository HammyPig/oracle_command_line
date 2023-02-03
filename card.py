class Card:

    def __init__(self, name, description, type):
        self.name = name
        self.description = description
        self.type = type

    def __repr__(self):
        return f"{self.name}"

    def use(self, caster):
        card_i = caster.hand.index(self)
        caster.hand.remove(self)
        status_code, status_description = self.use_effect(caster)

        if status_code == 1:
            caster.hand.insert(card_i, self)
        
        return status_code, status_description

class Attack(Card):

    def use_effect(self, caster):
        if caster.attack_count >= caster._attack_limit():
            return 1, "Already used maximum amount of attacks! Please choose another card."
        
        target = caster.choose_target()
        if not target.is_targettable():
            return 1, f"Player {target.name} is not targettable! Please choose another player."

        old_target_health = target.health
        target.health -= caster._attack_damage()
        target.health = max(0, target.health)
        
        return 0, f"Player {caster.name} used {self.name} on player {target.name}, reducing their health from {old_target_health} to {target.health}!"

class Backstab(Card):

    def use_effect(self, caster):
        target = caster.choose_target()
        if not target.is_targettable():
            return 1, f"Player {target.name} is not targettable! Please choose another player."

        old_target_health = target.health
        target.health -= 1

        return 0, f"Player {caster.name} used {self.name} on player {target.name}, reducing their health from {old_target_health} to {target.health}!"

class Capture(Card):

    def use_effect(self, caster):
        target, target_building = caster.choose_building()

        if target == None or target_building == None:
            return 1, "None selected."

        if not target.is_targettable():
            return 1, f"Player {target.name} is not targettable! Please choose another player."

        if not target.buildings:
            return 1, f"Player {target.name} does not own any buildings! Please choose another player."

        target.buildings.remove(target_building)
        caster.buildings.append(target_building)

        return 0, f"Player {caster.name} used {self.name} on player {target.name}, capturing their {target_building.name}!"

class Destroy(Card):

    def use_effect(self, caster):        
        target, target_building = caster.choose_building()

        if target == None or target_building == None:
            return 1, "None selected."

        if not target.is_targettable():
            return 1, f"Player {target.name} is not targettable! Please choose another player."

        if not target.buildings:
            return 1, f"Player {target.name} does not own any buildings! Please choose another player."

        target.buildings = [building for building in target.buildings if building.name != target_building.name]

        return 0, f"Player {caster.name} used {self.name} on player {target.name}, destroying their {target_building.name}(s)!"

class Heist(Card):

    def use_effect(self, caster):
        target = caster.choose_target()
        if not target.is_targettable():
            return 1, f"Player {target.name} is not targettable! Please choose another player."

        old_target_hand = target.hand
        target.hand = caster.hand
        caster.hand = old_target_hand

        return 0, f"Player {caster.name} used {self.name} on player {target.name}, switching their hands!"

class Sabotage(Card):

    def use_effect(self, caster):
        target = caster.choose_target()
        if not target.is_targettable():
            return 1, f"Player {target.name} is not targettable! Please choose another player."

        card1 = caster.choose_card_from(target)
        if card1 == None: return 1, f"Player {target.name} has no cards."
        
        target.hand.remove(card1)

        card2 = caster.choose_card_from(target)
        if card2 == None: return 0, f"Player {caster.name} used {self.name} on player {target.name}, removing their last card {card1.name}!"
        
        target.hand.remove(card2)

        return 0, f"Player {caster.name} used {self.name} on player {target.name}, removing {card1.name} and {card2.name}!"

class Spy(Card):

    def use_effect(self, caster):
        target = caster.choose_target()
        if not target.is_targettable():
            return 1, f"Player {target.name} is not targettable! Please choose another player."
            
        return 0, f"Player {caster.name} used {self.name} on player {target.name}, a useless card!"

class GoodyBag(Card):

    def use_effect(self, caster):
        caster.draw_cards(2)
        return 0, f"Player {caster.name} used {self.name}."

class GoodyBagPlus(Card):

    def use_effect(self, caster):
        caster.draw_cards(3)
        return 0, f"Player {caster.name} used {self.name}."

class Building(Card):

    def use_effect(self, caster):
        caster.buildings.append(self)

        return 0, f"Player {caster.name} used {self.name}"
