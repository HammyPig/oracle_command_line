class Card:

    PLAYED = 0
    INVALID = 1
    BLOCKED = 2
    RESPONDING_TO_CARD = 3

    def __init__(self, name, description, type):
        self.name = name
        self.description = description
        self.type = type

    def __repr__(self):
        return f"{self.name}"

    def use(self, caster, context=None):
        card_i = caster.hand.index(self)
        caster.hand.remove(self)

        if context:
            status_code, status_description = self.use_effect(caster, context)
        else:
            status_code, status_description = self.use_effect(caster)

        if status_code == Card.INVALID:
            caster.hand.insert(card_i, self)
        
        return status_code, status_description

    def defender(self, caster):
        for player in caster.game.players:
            if player == caster:
                continue

            defend_card = player.defend_card()

            if defend_card == None:
                continue

            if player.choose_defend():
                status_code, status_description = defend_card.use(player, Card.RESPONDING_TO_CARD)
                if status_code == Card.PLAYED:
                    return player

        return None

    def nullifier(self, caster):
        for player in caster.game.players:
            
            nullify_card = None
            for card in player.hand:
                if card.name == "Nullify":
                    nullify_card = card
                    break

            if nullify_card == None:
                continue

            if player.choose_nullify():
                status_code, status_description = nullify_card.use(player, Card.RESPONDING_TO_CARD)
                if status_code == Card.PLAYED:
                    return player

        return None

class Attack(Card):

    def use_effect(self, caster):
        if caster.attack_count >= caster._attack_limit():
            return Card.INVALID, "Already used maximum amount of attacks! Please choose another card."
        
        target = caster.choose_target()
        if not target.is_targettable():
            return Card.INVALID, f"Player {target.name} is not targettable! Please choose another player."

        caster.attack_count += 1

        nullifier = self.nullifier(caster)
        if nullifier != None:
            return Card.BLOCKED, f"Player {caster.name} used {self.name} on player {target.name}, but was nullified by player {nullifier.name}!"
        
        defender = self.defender(caster)
        if defender != None:
            return Card.BLOCKED, f"Player {caster.name} used {self.name} on player {target.name}, but was defended by player {defender.name}!"

        fort = target.block_with_fort()
        if fort:
            target.buildings.remove(fort)
            return Card.BLOCKED, f"Player {caster.name} used {self.name} on player {target.name}, but was blocked by their fort!"

        old_target_health = target.health
        target.health -= caster._attack_damage()
        target.health = max(0, target.health)
        
        return Card.PLAYED, f"Player {caster.name} used {self.name} on player {target.name}, reducing their health from {old_target_health} to {target.health}!"

class Backstab(Card):

    def use_effect(self, caster):
        target = caster.choose_target()
        if not target.is_targettable():
            return Card.INVALID, f"Player {target.name} is not targettable! Please choose another player."

        nullifier = self.nullifier(caster)
        if nullifier != None:
            return Card.BLOCKED, f"Player {caster.name} used {self.name} on player {target.name}, but was nullified by player {nullifier.name}!"
        
        defender = self.defender(caster)
        if defender != None:
            return Card.BLOCKED, f"Player {caster.name} used {self.name} on player {target.name}, but was defended by player {defender.name}!"

        fort = target.block_with_fort()
        if fort:
            target.buildings.remove(fort)
            return Card.BLOCKED, f"Player {caster.name} used {self.name} on player {target.name}, but was blocked by their fort!"

        old_target_health = target.health
        target.health -= 1

        return Card.PLAYED, f"Player {caster.name} used {self.name} on player {target.name}, reducing their health from {old_target_health} to {target.health}!"

class Capture(Card):

    def use_effect(self, caster):
        target, target_building = caster.choose_building()

        if target == None or target_building == None:
            return Card.INVALID, "None selected."

        if not target.is_targettable():
            return Card.INVALID, f"Player {target.name} is not targettable! Please choose another player."

        if not target.buildings:
            return Card.INVALID, f"Player {target.name} does not own any buildings! Please choose another player."

        nullifier = self.nullifier(caster)
        if nullifier != None:
            return Card.BLOCKED, f"Player {caster.name} used {self.name} on player {target.name}, but was nullified by player {nullifier.name}!"

        defender = self.defender(caster)
        if defender != None:
            return Card.BLOCKED, f"Player {caster.name} used {self.name} on player {target.name}, but was defended by player {defender.name}!"

        target.buildings.remove(target_building)
        caster.buildings.append(target_building)

        return Card.PLAYED, f"Player {caster.name} used {self.name} on player {target.name}, capturing their {target_building.name}!"

class Destroy(Card):

    def use_effect(self, caster):        
        target, target_building = caster.choose_building()

        if target == None or target_building == None:
            return Card.INVALID, "None selected."

        if not target.is_targettable():
            return Card.INVALID, f"Player {target.name} is not targettable! Please choose another player."

        if not target.buildings:
            return Card.INVALID, f"Player {target.name} does not own any buildings! Please choose another player."

        nullifier = self.nullifier(caster)
        if nullifier != None:
            return Card.BLOCKED, f"Player {caster.name} used {self.name} on player {target.name}, but was nullified by player {nullifier.name}!"

        defender = self.defender(caster)
        if defender != None:
            return Card.BLOCKED, f"Player {caster.name} used {self.name} on player {target.name}, but was defended by player {defender.name}!"

        target.buildings = [building for building in target.buildings if building.name != target_building.name]

        return Card.PLAYED, f"Player {caster.name} used {self.name} on player {target.name}, destroying their {target_building.name}(s)!"

class Heist(Card):

    def use_effect(self, caster):
        target = caster.choose_target()
        if not target.is_targettable():
            return Card.INVALID, f"Player {target.name} is not targettable! Please choose another player."

        nullifier = self.nullifier(caster)
        if nullifier != None:
            return Card.BLOCKED, f"Player {caster.name} used {self.name} on player {target.name}, but was nullified by player {nullifier.name}!"

        defender = self.defender(caster)
        if defender != None:
            return Card.BLOCKED, f"Player {caster.name} used {self.name} on player {target.name}, but was defended by player {defender.name}!"

        old_target_hand = target.hand
        target.hand = caster.hand
        caster.hand = old_target_hand

        return Card.PLAYED, f"Player {caster.name} used {self.name} on player {target.name}, switching their hands!"

class Sabotage(Card):

    def use_effect(self, caster):
        target = caster.choose_target()
        if not target.is_targettable():
            return Card.INVALID, f"Player {target.name} is not targettable! Please choose another player."

        nullifier = self.nullifier(caster)
        if nullifier != None:
            return Card.BLOCKED, f"Player {caster.name} used {self.name} on player {target.name}, but was nullified by player {nullifier.name}!"

        defender = self.defender(caster)
        if defender != None:
            return Card.BLOCKED, f"Player {caster.name} used {self.name} on player {target.name}, but was defended by player {defender.name}!"

        card1 = caster.choose_card_from(target)
        if card1 == None: return Card.INVALID, f"Player {target.name} has no cards."
        
        target.hand.remove(card1)

        card2 = caster.choose_card_from(target)
        if card2 == None: return Card.PLAYED, f"Player {caster.name} used {self.name} on player {target.name}, removing their last card {card1.name}!"
        
        target.hand.remove(card2)

        return Card.PLAYED, f"Player {caster.name} used {self.name} on player {target.name}, removing {card1.name} and {card2.name}!"

class Spy(Card):

    def use_effect(self, caster):
        target = caster.choose_target()
        if not target.is_targettable():
            return Card.INVALID, f"Player {target.name} is not targettable! Please choose another player."

        nullifier = self.nullifier(caster)
        if nullifier != None:
            return Card.BLOCKED, f"Player {caster.name} used {self.name} on player {target.name}, but was nullified by player {nullifier.name}!"


        defender = self.defender(caster)
        if defender != None:
            return Card.BLOCKED, f"Player {caster.name} used {self.name} on player {target.name}, but was defended by player {defender.name}!"

        return Card.PLAYED, f"Player {caster.name} used {self.name} on player {target.name}, a useless card!"

class Defend(Card):

    def use_effect(self, caster, context=None):
        if context != Card.RESPONDING_TO_CARD:
            return Card.INVALID, f"Cannot use defend unless responding to an offensive card!"

        nullifier = self.nullifier(caster)
        if nullifier != None:
            return Card.BLOCKED, f"Player {caster.name} used {self.name}, but was nullified by player {nullifier.name}!"

        return Card.PLAYED, ""

class GoodyBag(Card):

    def use_effect(self, caster):

        nullifier = self.nullifier(caster)
        if nullifier != None:
            return Card.BLOCKED, f"Player {caster.name} used {self.name}, but was nullified by player {nullifier.name}!"

        caster.draw_cards(2)
        return Card.PLAYED, f"Player {caster.name} used {self.name}."

class GoodyBagPlus(Card):

    def use_effect(self, caster):

        nullifier = self.nullifier(caster)
        if nullifier != None:
            return Card.BLOCKED, f"Player {caster.name} used {self.name}, but was nullified by player {nullifier.name}!"

        caster.draw_cards(3)
        return Card.PLAYED, f"Player {caster.name} used {self.name}."

class Building(Card):

    def use_effect(self, caster):

        nullifier = self.nullifier(caster)
        if nullifier != None:
            return Card.BLOCKED, f"Player {caster.name} used {self.name}, but was nullified by player {nullifier.name}!"

        caster.buildings.append(self)

        return Card.PLAYED, f"Player {caster.name} used {self.name}"

class Barrier(Card):

    def use_effect(self, caster):
        if not caster.can_use_spells(): return Card.INVALID, f"Cannot use {self.name}, no Spell Tower is present!"

        nullifier = self.nullifier(caster)
        if nullifier != None:
            return Card.BLOCKED, f"Player {caster.name} used {self.name}, but was nullified by player {nullifier.name}!"

        caster.buildings.append(self)

        return Card.PLAYED, f"Player {caster.name} used {self.name}"

class BlackHole(Card):

    def use_effect(self, caster):
        if not caster.can_use_spells(): return Card.INVALID, f"Cannot use {self.name}, no Spell Tower is present!"

        nullifier = self.nullifier(caster)
        if nullifier != None:
            return Card.BLOCKED, f"Player {caster.name} used {self.name}, but was nullified by player {nullifier.name}!"

        for player in caster.game.players:
            player.buildings = []

        return Card.PLAYED, f"Player {caster.name} used {self.name}"

class BloodMagic(Card):

    def use_effect(self, caster):
        if not caster.can_use_spells(): return Card.INVALID, f"Cannot use {self.name}, no Spell Tower is present!"
        target = caster.choose_target()

        nullifier = self.nullifier(caster)
        if nullifier != None:
            return Card.BLOCKED, f"Player {caster.name} used {self.name}, but was nullified by player {nullifier.name}!"

        old_caster_health = caster.health

        caster.health = target.health
        target.health = old_caster_health

        return Card.PLAYED, f"Player {caster.name} used {self.name}, switching health from {old_caster_health} to {caster.health}"

class Nullify(Card):

    def use_effect(self, caster, context=None):
        if context != Card.RESPONDING_TO_CARD:
            return Card.INVALID, f"Cannot use {self.name} unless responding to a card!"

        nullifier = self.nullifier(caster)
        if nullifier != None:
            return Card.BLOCKED, f"Player {caster.name} used {self.name}, but was nullified by player {nullifier.name}!"

        return Card.PLAYED, ""
