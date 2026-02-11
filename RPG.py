# Bobby Pagliaro
# Final Project
# 12/5/25

import random
import time     # Slower printing of lines to make them easier to read

def slow_print(text, delay = 0.6):
    print(text)
    time.sleep(delay)

def med_print(text, delay = 0.4):
    print(text)
    time.sleep(delay)

def fast_print(text, delay = 0.2):
    print(text)
    time.sleep(delay)

# Character base class

class Character:
    def __init__(self, name, health, attack_power, mana, level):
        self.name = name
        
        self.health = health
        self.max_health = health
        
        self.mana = mana
        self.max_mana = mana

        self.attack_power = attack_power
        
        self.level = level
        self.xp = 1
        self.xp_to_next_level = 100

        self.money = 0
        
        self.attack_buff = 0.0                      # From Mage spell
        self.attack_buff_turns = 0
        self.defense_buff = 0                       # From Knight spell
        self.defense_buff_turns = 0
        self.next_attack_multiplier = 1.0           # From Warrior spell

    def is_alive(self):
        return self.health > 0
    
    def heal(self, amount):
        self.health = min(self.health + amount, self.max_health)   # "min" is used to prevent healing beyond max health
        med_print(f"\n{self.name} healed for {amount} health points. Current health: {self.health}/{self.max_health}")

    def restore_mana(self, amount):
        self.mana = min(self.mana + amount, self.max_mana)       # Prevent  restoring beyond max mana
        med_print(f"\n{self.name} restored {amount} mana points. Current mana: {self.mana}/{self.max_mana}")

    def gain_xp(self, amount):
        self.xp += amount
        self.level_up()     # Check to see if character has enough xp to level up

    def levels_up(self):
        while self.xp >= self.xp_to_next_level:
            self.xp -= self.xp_to_next_level                                # Subtract xp needed for level up
            self.level += 1
            self.xp_to_next_level = int(self.xp_to_next_level * 1.3)        # Increase xp needed for next level
            self.health = min(self.health + int(self.max_health * 0.50), self.max_health)   # Restore 50% of health on level up
            self.mana = min(self.mana + int(self.max_mana * 0.25), self.max_mana)           # Restore 25% of mana on level up

            slow_print(f"{self.name}'s health and mana have been partially restored.")
    
    def take_damage(self, damage):
        if self.defense_buff_turns > 0:   # Apply Rakukaja defense buff
            damage = max(0, damage - self.defense_buff) # "Max" prevents damage from being negative

        self.health -= damage

        if self.health <= 0:
            self.health = 0

    
    def attack(self, target):
        total_attack_power = self.attack_power + self.attack_buff       # Tarukaja attack buff
        damage = int(total_attack_power * self.next_attack_multiplier)  # Charge attack multiplier

        target.take_damage(damage)
        real_damage = max(0, damage - target.defense_buff)    # Makes it print the correct amount of damage taken
        
        slow_print(f"\n{self.name} attacked {target.name} for {real_damage} damage. Current health of {target.name}: {target.health}/{target.max_health}")
        if target.health == 0:
            med_print(f"\n{target.name} has been downed!")
        
        self.next_attack_multiplier = 1.0    # Reset charge multiplier after attack

# Party class

class Party:
    def __init__(self, members):
        self.members = members     # list of Characters
        self.money = 0
        self.inventory = {
            "Health Potion": 3,
            "Greater Health Potion": 0,
            "Mana Potion": 3
        }

    def alive_members(self):
        return [m for m in self.members if m.is_alive()]

    def is_defeated(self):
        return all(not m.is_alive() for m in self.members)

    def show_status(self):
        print("\n--- Party Status ---")
        for m in self.members:
            fast_print(f"{m.name}: Level {m.level} | HP {m.health}/{m.max_health} | MP {m.mana}/{m.max_mana}")
    
    def has_item(self, item_name):
        return self.inventory.get(item_name, 0) > 0     # Check if item is in inventory
    
    def use_item(self, item_name, target):
        if not self.has_item(item_name):
            fast_print(f"No {item_name}'s left!")
            return False
        
        if item_name == "Health Potion":
            if target.health == target.max_health:
                fast_print(f"\n{target.name} is already at full health.")
                return False
            if target.health == 0:
                med_print(f"\n{target.name} is downed and cannot be healed!")   # Prevents using health potions on dead teammates
                return False
            target.heal(50)
        elif item_name == "Mana Potion":
            if target.mana == target.max_mana:
                fast_print(f"\n{target.name} already has full mana.")
                return False
            if target.health == 0:
                med_print(f"\n{target.name} is downed and cannot restore mana!")   # Prevents using mana potions on dead teammates
                return False
            target.restore_mana(30)
        elif item_name == "Greater Health Potion":
            if target.health == target.max_health:
                fast_print(f"\n{target.name} is already at full health.")
                return False
            if target.health == 0:
                med_print(f"\n{target.name} is downed and cannot be healed!")   # Prevents using health potions on dead teammates
                return False
            target.heal(100)
        else:
            fast_print(f"{item_name} is not a valid item.")
            return False
        
        self.inventory[item_name] -= 1  # Decrease item count
        med_print(f"\n{target.name} used a {item_name}. {self.inventory[item_name]} left.")
        return True
    
    def add_item(self, item_name, amount=1):
        if item_name in self.inventory:
            self.inventory[item_name] += amount
        else:
            self.inventory[item_name] = amount
    
    def show_inventory(self):
        print("\n--- Inventory ---")
        
        for item, count in self.inventory.items():
            med_print(f"{item}: {count}")

    def add_money(self, amount):
        self.money += amount
        med_print(f"\nThe party received {amount} reeve! Total reeve: {self.money}")

    def distribute_xp(self, enemies):
        total_xp = sum(e.xp_reward for e in enemies)
        total_money = sum(e.money_reward for e in enemies)
        
        print("\n--- Battle Rewards ---")
        med_print(f"All surviving party members gained {total_xp} xp!")
        fast_print(f"Party gained {total_money} reeve!")

        for member in self.alive_members():
            member.gain_xp(total_xp)
            slow_print(f"{member.name} xp: {member.xp}/{member.xp_to_next_level}")

        self.add_money(total_money)


# Subclasses for different character types

class Warrior(Character):   # Names of character types are based on "Metaphor ReFantazio"
    def __init__(self, name):
        super().__init__(name, health = 100, attack_power = 15, mana = 20, level = 1)   # "super" is used to call something from the parent class

    def cast_charge(self): # Names and functions of spells are based on the Persona (Shin Megami Tensei) series
        mana_cost = 5

        if self.mana < mana_cost:   # Checks for enough mana
            fast_print(f"\n{self.name} does not have enough mana to cast Charge.")
            return False
        
        if self.next_attack_multiplier == 2.5:
            fast_print(f"\n{self.name} is already charged up! Next attack will deal 2.5x damage.")
            return False
        
        self.mana -= mana_cost     # Use mana from character
        self.next_attack_multiplier = 2.5
        fast_print(f"\n{self.name} is charged up! Next attack will deal 2.5x damage.")
        return True
    
    def cast_vorpal_blade(self, enemies):
        mana_cost = 8

        if self.mana < mana_cost:   
            fast_print(f"\n{self.name} does not have enough mana to cast Vorpal Blade.")
            return False
    
        total_attack_power = self.attack_power + self.attack_buff
        damage = int(total_attack_power * self.next_attack_multiplier)
        damage = int(damage * 1.25)

        self.mana -= mana_cost

        for enemy in enemies:
            enemy.take_damage(damage)
            slow_print(f"\n{self.name} hit {enemy.name} for {damage} damage. Current health of {enemy.name}: {enemy.health}/{enemy.max_health}")
            if enemy.health == 0:
                med_print(f"\n{enemy.name} has been downed!")
        self.next_attack_multiplier = 1.0
        return True
    
    def cast_brave_blade(self, target):
        mana_cost = 7
        
        if self.mana < mana_cost:
            fast_print(f"\n{self.name} does not have enough mana to cast Brave Blade.")
            return False
        
        total_attack_power = self.attack_power + self.attack_buff
        damage = int(total_attack_power * self.next_attack_multiplier)
        damage = damage * 2

        self.mana -= mana_cost

        target.take_damage(damage)
        slow_print(f"\n{self.name} hit {target.name} for {damage} damage. Current health of {target.name}: {target.health}/{target.max_health}")
        if target.health == 0:
            med_print(f"\n{target.name} has been downed!")
        self.next_attack_multiplier = 1.0
        return True
    
    def cast_armageddon(self, enemies):    # Kills all enemies instantly, used only for testing
        for enemy in enemies:             # Must enter "begone" in spell menu to use
            enemy.take_damage(9999)
            slow_print(f"\n{self.name} hit {enemy.name} for {9999} damage. Current health of {enemy.name}: {enemy.health}/{enemy.max_health}")
            if enemy.health == 0:
                med_print(f"\n{enemy.name} has been downed!")
        return True


    def level_up(self):
        while self.xp >= self.xp_to_next_level:
            fast_print(f"\n{self.name} leveled up to level {self.level}!")
            self.max_health += 15
            fast_print("Max health: + 15")
            self.max_mana += 5
            fast_print("Max mana: + 5")
            self.attack_power += 5
            fast_print("Attack power: + 5")
            super().levels_up()

class Mage(Character):
    def __init__ (self, name):
        super().__init__(name, health = 70, attack_power = 10, mana = 70, level = 1)

    def cast_tarukaja(self, target):
        mana_cost = 10

        if self.mana < mana_cost:
            fast_print(f"\n{self.name} does not have enough mana to cast Tarukaja.")
            return False
        
        self.mana -= mana_cost

        if target.attack_buff_turns > 0:    # If buff already active refresh durationt
            target.attack_buff_turns = 3
            med_print(f"\n{self.name} refreshes Tarukaja on {target.name}! Buff duration reset to 3 turns.")
            return True
        else:
            target.attack_buff += 5       # Apply new buff
            target.attack_buff_turns = 3
            med_print(f"\n{self.name} casts Tarukaja on {target.name}, increasing attack by 5 for 3 turns.")
            return True
        
    def cast_matarukaja(self, party):
        mana_cost = 20

        if self.mana < mana_cost:
            fast_print(f"\n{self.name} does not have enough mana to cast Matarukaja.")
            return False
        
        self.mana -= mana_cost

        for member in party:
            if member.attack_buff_turns > 0:    # If buff already active refresh duration
                member.attack_buff_turns = 3
                med_print(f"\n{self.name} refreshes Matarukaja on {member.name}! Buff duration reset to 3 turns.")
            else:
                member.attack_buff += 5       # Apply new buff
                member.attack_buff_turns = 3
                med_print(f"\n{self.name} casts Matarukaja on {member.name}, increasing attack by 5 for 3 turns.")
        return True
    
    def cast_megidolaon(self, enemies):
        mana_cost = 25

        if self.mana < mana_cost:   
            fast_print(f"\n{self.name} does not have enough mana to cast Megidolaon.")
            return False
    
        total_attack_power = self.attack_power + self.attack_buff
        damage = int(total_attack_power * self.next_attack_multiplier)
        damage = damage * 3

        self.mana -= mana_cost

        for enemy in enemies:
            enemy.take_damage(damage)
            slow_print(f"\n{self.name} hit {enemy.name} for {damage} damage. Current health of {enemy.name}: {enemy.health}/{enemy.max_health}")
            if enemy.health == 0:
                med_print(f"\n{enemy.name} has been downed!")

        return True

    def level_up(self):
        while self.xp >= self.xp_to_next_level:    
            fast_print(f"\n{self.name} leveled up to level {self.level}!")
            self.max_health += 10
            fast_print("Max health: + 10")
            self.max_mana += 15
            fast_print("Max mana: + 15")
            self.attack_power += 2
            fast_print("Attack power: + 2")
            super().levels_up()

class Knight(Character):
    def __init__ (self, name):
        super().__init__(name, health = 150, attack_power = 10, mana = 30, level = 1)

    def cast_rakukaja(self, target):
        mana_cost = 10

        if self.mana < mana_cost:
            fast_print(f"\n{self.name} does not have enough mana to cast Rakukaja.")
            return False

        self.mana -= mana_cost

        if target.defense_buff_turns > 0:   # If buff already active refresh duration
            target.defense_buff_turns = 3
            med_print(f"\n{self.name} refreshes Rakukaja on {target.name}! Buff duration reset to 3 turns.")
            return True
        else:                               # Apply new buff
            target.defense_buff += 5
            target.defense_buff_turns = 3
            med_print(f"\n{self.name} cast Rakukaja on {target.name}, increasing defense by 5 for 3 turns.")
            return True
        
    def cast_marakukaja(self, party):
        mana_cost = 20

        if self.mana < mana_cost:
            fast_print(f"\n{self.name} does not have enough mana to cast Marakukaja.")
            return False

        self.mana -= mana_cost

        for member in party:
            if member.defense_buff_turns > 0:   # If buff already active refresh duration
                member.defense_buff_turns = 3
                med_print(f"\n{self.name} refreshes Marakukaja on {member.name}! Buff duration reset to 3 turns.")
            else:                               # Apply new buff
                member.defense_buff += 5
                member.defense_buff_turns = 3
                med_print(f"\n{self.name} cast Marakukaja on {member.name}, increasing defense by 5 for 3 turns.")
        return True
    
    def cast_jump_thrust(self, target):
        mana_cost = 7
        
        if self.mana < mana_cost:
            fast_print(f"{self.name} does not have enough mana to cast Jump Thrust.")
            return False
        
        total_attack_power = self.attack_power + self.attack_buff
        damage = int(total_attack_power * self.next_attack_multiplier)
        damage = damage * 2

        self.mana -= mana_cost

        target.take_damage(damage)
        slow_print(f"\n{self.name} hit {target.name} for {damage} damage. Current health of {target.name}: {target.health}/{target.max_health}")
        if target.health == 0:
            med_print(f"\n{target.name} has been downed!")

        return True

    def level_up(self):
        while self.xp >= self.xp_to_next_level:
            fast_print(f"\n{self.name} leveled up to level {self.level}!")
            self.max_health += 20
            fast_print("Max health: + 20")
            self.max_mana += 10
            fast_print("Max mana: + 10")
            self.attack_power += 3
            fast_print("Attack power: + 3")
            super().levels_up()

class Healer(Character):
    def __init__(self, name):
        super().__init__(name, health = 75, attack_power = 5, mana = 80, level = 1)

    def cast_dia(self, target):
        mana_cost = 10
        heal_amount = int(target.max_health * 0.66)

        if self.mana < mana_cost:
            fast_print(f"\n{self.name} does not have enough mana to cast Dia.")
            return False

        if target.health == target.max_health:
            fast_print(f"\n{target.name} is already at full health.")
            return False
        
        if target.health == 0:
            med_print(f"\n{target.name} is downed and cannot be healed!")   # Jsut a failsafe, can't even target dead teammates in game
            return False
        
        self.mana -= mana_cost
        target.heal(heal_amount)
        med_print(f"\n{self.name} cast Dia on {target.name}, healing them for {heal_amount} health.")
        return True


    def cast_media(self, party, member):
        mana_cost = 20

        if self.mana < mana_cost:
            fast_print(f"\n{self.name} does not have enough mana to cast Media.")
            return False

        all_full = all(member.health == member.max_health for member in party)  # Check if all party members are at full health
        if all_full:
            fast_print("\nParty is already at full health.")
            return False
        
        self.mana -= mana_cost
        for member in party:
            if member.health == 0:
                heal_amount = 0
                med_print(f"\n{member.name} is downed and cannot be healed!")   # Prevents dead teammates from being unintentionally revived
            else:
                heal_amount = int(member.max_health * 0.50) # Round to whole number
                member.heal(heal_amount)
        return True

    def cast_recarm(self, party_members):
        mana_cost = 25

        if self.mana < mana_cost:
            fast_print(f"\n{self.name} does not have enough mana to cast Recarm.")
            return False

        fallen = [m for m in party_members if not m.is_alive()] # Finds downed members

        if not fallen:
            fast_print("\nThere are no fallen party members to revive.")
            return False

        med_print("\n--- Recarm Target ---")    # Choose who to revive in multiple are down
        for i, member in enumerate(fallen, 1):
            slow_print(f"{i}. {member.name}")

        choice = input("Choose a target to revive: ")

        if not choice.isdigit() or not (1 <= int(choice) <= len(fallen)):
            print("\nInvalid choice.")
            return False

        target = fallen[int(choice) - 1]

        revive_amount = target.max_health // 2  # Revive with half HP
        target.health = revive_amount

        self.mana -= mana_cost
        slow_print(f"\n{self.name} revived {target.name} with {revive_amount} HP!")

        return True

    def level_up(self):
        while self.xp >= self.xp_to_next_level:
            fast_print(f"\n{self.name} leveled up to level {self.level}!")
            self.max_health += 10
            fast_print("Max health: + 10")
            self.max_mana += 13
            fast_print("Max mana: +12")
            self.attack_power += 2
            fast_print("Attack power: + 2")
            super().levels_up()

# Enemy class

class Enemy(Character):
    def __init__(self, name, health, attack_power, level, xp_reward, money_reward):
        super().__init__(name, health, attack_power, mana = 0, level=level)
        self.xp_reward = xp_reward
        self.money_reward = money_reward

    def choose_action(self, target):
        self.attack(target)

# Enemy types

Enemies = {
    "Slime":    {"health": 50,  "attack": 8,  "xp": 20, "money": 10},
    "Goblin":   {"health": 80,  "attack": 12, "xp": 35, "money": 20},
    "Orc":      {"health": 120, "attack": 18, "xp": 50, "money": 35},
    "Skeleton": {"health": 75,  "attack": 12, "xp": 30, "money": 15},
    "Zombie":   {"health": 90,  "attack": 14, "xp": 40, "money": 25},
}

# Enemy generator

def generate_enemies(party, min_enemies = 2, max_enemies = 5):
    num_enemies = random.randint(min_enemies, max_enemies)          # Randomly determine number of enemies
    enemies = [generate_enemy(party) for _ in range(num_enemies)]   # Generate enemies independently
    return enemies

def generate_enemy(party):
    player_level = max(member.level for member in party.members)        # Find highest level in party
    enemy_level = max(1, player_level + random.randint(-1, 2))  # Enemy level ranges from 1 below to 2 above highest player level

    enemy_type = random.choice(list(Enemies.keys()))            # Randomly select enemy type from list
    t = Enemies[enemy_type]                                     # Get enemy stats from list

    health_growth = 10
    attack_growth = 2

    scaled_health = t["health"] + (enemy_level - 1) * health_growth  # Scale enemy stats based on level
    scaled_attack = t["attack"] + (enemy_level - 1) * attack_growth
    scaled_xp = t["xp"] + (enemy_level - 1) * 5
    scaled_money = t["money"] + (enemy_level - 1) * 3

    return Enemy(
        name = enemy_type,
        health = scaled_health,
        attack_power = scaled_attack,
        level = enemy_level,
        xp_reward = scaled_xp,
        money_reward = scaled_money
    )

# Boss class

class Boss(Enemy):
    def choose_action(self, party):
        roll = random.random()

        if roll < 0.20:  # Normal attack
            target = random.choice(party.alive_members())
            self.attack(target)

        elif roll < 0.50:    # Heavy attack
            target = random.choice(party.alive_members())
            damage = int(self.attack_power * 1.7)
            target.take_damage(damage)
            med_print(f"{self.name} uses Savage Blow on {target.name} for {damage} damage! Current health of {target.name}: {target.health}/{target.max_health}")
            if target.health == 0:
                    med_print(f"\n{target.name} has been downed!")

        else:   # All part members
            med_print(f"{self.name} unleashes Sweeping Edge!")
            for member in party.alive_members():
                damage = int(self.attack_power * 1.2)
                member.take_damage(damage)
                med_print(f"{member.name} takes {damage} damage! Current health of: {member.health}/{member.max_health}")
                if member.health == 0:
                    med_print(f"\n{member.name} has been downed!")

def generate_boss(party):

    player_level = max(member.level for member in party.members)

    boss_level = max(1, player_level + random.randint(2, 4))    # Boss is always a couple levels above party

    boss_base = {   # Base stats
        "name": "Demon Lord",
        "health": 350,
        "attack": 30,
        "xp": 150,
        "money": 200
    }

    health_growth = 40
    attack_growth = 6
    xp_growth = 15
    money_growth = 10

    scaled_health = boss_base["health"] + (boss_level - 1) * health_growth  # Scaling
    scaled_attack = boss_base["attack"] + (boss_level - 1) * attack_growth
    scaled_xp = boss_base["xp"] + (boss_level - 1) * xp_growth
    scaled_money = boss_base["money"] + (boss_level - 1) * money_growth

    return Boss(
        name = boss_base["name"],
        health = scaled_health,
        attack_power = scaled_attack,
        level = boss_level,
        xp_reward = scaled_xp,
        money_reward = scaled_money
    )

def boss_battle(party):
    boss = generate_boss(party)
    enemies = [boss]

    med_print("\nA boss approaches")
    slow_print(f"The {boss.name} emerges with {boss.health} HP!")

    battle(party, enemies)

# Item menu

def item_menu(member, party):
    party.show_inventory()

    print("\nChoose an item:")
    items = list(party.inventory.keys())

    for i, item in enumerate(items):
        med_print(f"{i+1}. {item}")

    choice = input("Item: ")

    if not choice.isdigit() or not (1 <= int(choice) <= len(items)):
        fast_print("Invalid item choice.")
        return

    item_name = items[int(choice) - 1]

    print("\nChoose a target:")      # Select target
    for i, ally in enumerate(party.members):
        slow_print(f"{i+1}. {ally.name} (HP: {ally.health}/{ally.max_health}, MP: {ally.mana}/{ally.max_mana})")

    target_choice = input("Target: ")

    if not target_choice.isdigit() or not (1 <= int(target_choice) <= len(party.members)):
        fast_print("Invalid target choice.")
        return

    target = party.members[int(target_choice) - 1]

    party.use_item(item_name, target)

    return True

# Battle system

def battle(party, enemies):    
    med_print("A battle has started!")

    all_enemies = enemies.copy()  # Keep original enemies for rewards
    turn_number = 1

    while True:
        print(f"\n=== Turn {turn_number} ===")
        party.show_status()
        med_print("\n--- Enemy Status ---")
        for e in enemies:
            fast_print(f"{e.name}: HP {e.health}/{e.max_health}")

        for member in party.alive_members():    # Party turn
            turn_used = False    # Allows player to go back to action select menu without skipping their turn
            while not turn_used:
                if not enemies:  # No enemies left
                    print("\nAll enemies defeated!")

                    for member in party.alive_members():
                        member.next_attack_multiplier = 1.0        
                        buff_clense(member) # Get rid of buffs after battle
                    med_print("All buffs removed")

                    party.distribute_xp(all_enemies)
                    return
                fast_print(f"\n{member.name}'s turn:")
                med_print("1. Attack")
                med_print("2. Cast Spell")
                med_print("3. Use Item")
                med_print("4. Status")

                choice = input("Choose an action: ")

                if choice == "1":
                    target = choose_target(enemies)
                    if target:
                        member.attack(target)
                        turn_used = True
                    else:
                        fast_print("No valid target!")
                        continue
                    

                elif choice == "2":
                    success = cast_spell_menu(member, party.members, enemies)
                    if success: 
                        turn_used = True       # Only end turn if spell actually wokrs
                    else: 
                        continue               # Spell fails, reselect

                elif choice == "3":
                    used = item_menu(member, party)
                    if used: 
                        turn_used = True
                    else:
                        continue

                elif choice == "4":
                    party.show_status()
                    print("\n--- Enemy Status ---")
                    for e in enemies:
                        slow_print(f"{e.name}: HP {e.health}/{e.max_health}")
                    continue

                else: 
                    fast_print("Invalid command.")

                if not enemies:
                    print("\nAll enemies defeated!")
                    party.distribute_xp(all_enemies)
                    return

            enemies = [e for e in enemies if e.is_alive()]  # Remove defeated enemies
            buff_tickdown(member)

        print("\n--- Enemies Turn ---")    # Enemy turn

        for enemy in enemies:
            if len(party.alive_members()) == 0:
                break

            if not enemy.is_alive():
                continue

            if isinstance(enemy, Boss):
                enemy.choose_action(party)  # Boss attacks override normal attacks
            else:
                target = random.choice(party.alive_members())
                enemy.choose_action(target)

        if party.is_defeated(): # Check if party died
            print("\nAll party members have been downed! GAME OVER.")
            return
            
        turn_number += 1


def choose_target(enemies):
    alive_enemies = [e for e in enemies if e.is_alive()]  # Only show alive enemies
    if not alive_enemies:
        return None

    print("\nSelect a target:")
    for i, enemy in enumerate(alive_enemies):
        fast_print(f"{i + 1}. {enemy.name} (HP: {enemy.health}/{enemy.max_health})")

    while True:
        try:
            choice = int(input("Choose target: "))
            if 1 <= choice <= len(alive_enemies):
                return alive_enemies[choice - 1]
            else:
                fast_print("Invalid choice — out of range.")
        except ValueError:  # Doesn't crash on invalid input
            fast_print("Invalid input — please enter a number.")


def cast_spell_menu(member, party, enemies):
    print("\n--- Spells ---:")

    if isinstance(member, Warrior): # Warrior spells, checks who is casting
        while True:                 # Allows for re-selection of spell if invalid or info requested
            fast_print("1. Charge (5 MP)")
            fast_print("2. Vorpal Blade (8 MP)")
            fast_print("3. Brave Blade (7 MP)")
            fast_print("Type 'info' for spell descriptions.")
            spell = input("Choose a spell: ")
            
            if spell == "1":
                return member.cast_charge()
            
            if spell == "2":
                return member.cast_vorpal_blade(enemies)
            
            if spell == "3":
                target = choose_target(enemies)
                return member.cast_brave_blade(target)
            
            if spell == "begone":
                return member.cast_armageddon(enemies)


            elif spell.lower() == "info":
                print("\n--- Spell Descriptions ---")
                fast_print("Charge (5 MP): Increases the damage of the next attack by 2.5 times, can only be used on self.")
                fast_print("Vorpal Blade (8 MP): Attack all enemies (including buffs).")
                fast_print("Brave Blade (7 MP): Deal heavy damage to one enemy (including buffs).")
                print("")   # Extra line for spacing

            else:
                fast_print("Invalid spell choice.")
                return None

    elif isinstance(member, Mage):   # Mage spells \
        while True:                
            fast_print("1. Tarukaja (10 MP)")
            fast_print("2. Matarukaja (20 MP)")
            fast_print("3. Megidolaon (25 MP)")
            fast_print("Type 'info' for spell descriptions.")
            spell = input("Choose a spell: ")
                
            if spell == "1":
                target = choose_target(party)
                return member.cast_tarukaja(target)
            
            if spell == "2":
                return member.cast_matarukaja(party)
            
            if spell == "3":
                return member.cast_megidolaon(enemies)

            elif spell.lower() == "info":
                print("\n--- Spell Descriptions ---")
                fast_print("Tarukaja (10 MP): Increases a target's attack power by 5 for three turns.")
                fast_print("Matarukaja (20 MP): Increases the party's attack power by 5 for three turns")
                fast_print("Megidolaon (25 MP): Deals heavy damage to all enemies (including buffs).")
                print("")

            else:
                fast_print("Invalid spell choice.")
                return None

    elif isinstance(member, Knight): # Knight spells
        while True:
            fast_print("1. Rakukaja (10 MP)")
            fast_print("2. Marakukaja (20 MP)")
            fast_print("3. Jump Thrust (7 MP)")
            fast_print("Type 'info' for spell descriptions.")
            spell = input("Choose a spell: ")
        
            if spell == "1":
                target = choose_target(party)
                return member.cast_rakukaja(target)
            
            elif spell == "2":
                return member.cast_marakukaja(party)
            
            elif spell == "3":
                target = choose_target(enemies)
                return member.cast_jump_thrust(target)

            elif spell.lower() == "info":
                print("\n--- Spell Descriptions ---")
                fast_print("Rakukaja (10 MP): Increases a target's defense by 5 for three turns.")
                fast_print("Marakukaja (20 MP): Increases the party's defence by 5 for three turns")
                fast_print("Jump Thrust (7 MP): Deals heavy damage to one enemy (including buffs)")
                print("")

            else:
                fast_print("Invalid spell choice.")
                return None

    elif isinstance(member, Healer): # Healer spells
        while True:
            fast_print("1. Dia (10 MP)")
            fast_print("2. Media (20 MP)")
            fast_print("3. Recarm (25 MP)")
            fast_print("Type 'info' for spell descriptions.")
            spell = input("Choose a spell: ")
            
            if spell == "1":
                target = choose_target(party)
                return member.cast_dia(target)

            elif spell == "2":
                return member.cast_media(party, member)
            
            elif spell == "3":
                return member.cast_recarm(party)   # Recarm needs to target dead allies so it has it's own targeting function

            elif spell.lower() == "info":
                print("\n--- Spell Descriptions ---")
                fast_print("Dia (10 MP): Heals a single target for 2/3 of their health (must be alive).")
                fast_print("Media (20 MP): Heals all party members for 1/2 of their health (must be alive).")
                fast_print("Recarm (25 MP): Revive one fallen ally with half HP (must be dead)")
                print("")

            else:
                fast_print("Invalid spell choice.")
                return None

def buff_tickdown(member):  # Decrease buff durations at end of turn
    if member.attack_buff_turns >= 1:
        member.attack_buff_turns -= 1
        if member.attack_buff_turns == 0:
            member.attack_buff = 0
            med_print(f"{member.name}'s attack buff wore off.")

    if member.defense_buff_turns >= 1:
        member.defense_buff_turns -= 1
        if member.defense_buff_turns == 0:
            member.defense_buff = 0
            med_print(f"{member.name}'s defense buff wore off.")

def buff_clense(member):  # Remove buffs after battle without text clutter
    member.attack_buff_turns = 0
    member.attack_buff = 0

    member.defense_buff_turns = 0
    member.defense_buff = 0
    # med_print("All buffs removed") -> in battle

def town_menu(party):   # For between fights
    while True:
        fast_print("\n--- Welcome to the town ---")
        med_print("1. Inn (Revive/Heal)")
        med_print("2. Shop (Buy more items)")
        med_print("3. Party status")
        med_print("4. Leave town")

        choice = input("Choose an option: ")
        if choice == "1":
            revive_inn(party)
        elif choice == "2":
            shop_menu(party)
        elif choice == "3":
            party.show_status()
        elif choice == "4":
            fast_print("Leaving town...")
            return False
        else: 
            print("Invalid option")

def revive_inn(party):
    cost = 60
    med_print(f"\nThe innkeeper will charge {cost} reeve to rest for the night (Revive all fallen party members, heal 50% health and mana to living party members)")
    fast_print(f"Reeve: {party.money}")

    if party.money < cost:
        fast_print("You don't have enough reeve!")
        return
    
    confirm = input("\nWould you like the party to rest? (y/n): ").lower()
    if confirm != "y":  # != makes it so anything other than "y" will return
        return
    
    party.money -= cost

    for member in party.members:
        if member.is_alive():
            member.health = min(member.health + int(member.max_health * 0.50), member.max_health)
            member.mana = min(member.mana + int(member.max_mana * 0.50), member.max_mana)
            med_print(f"{member.name} restored HP and MP! HP: {member.health}/{member.max_health} | MP: {member.mana}/{member.max_mana}")

    for member in party.members:
        if not member.is_alive():
            member.health = member.max_health // 2
            med_print(f"{member.name} has been revived with {member.health}/{member.max_health} HP!")
        
    med_print("\nThe party has rested.")

shop_items = {  # List of purchacable items
    "Health Potion": {"price": 20, "effect": "health", "amount": 50},
    "Mana Potion": {"price": 30, "effect": "mana", "amount": 30},
    "Greater Health Potion": {"price": 40, "effect": "health", "amount": 100}
}

def shop_menu(party):
    while True:
        print("\n--- Item Shop ---")
        fast_print(f"Reeve: {party.money}")

        for i, item in enumerate(shop_items, 1):    # Numbers items in shop
            price = shop_items[item]["price"]
            slow_print(f"{i}. {item} ({price} reeve)")

        print (f"{len(shop_items) + 1}. Leave Shop")

        choice = input("'What would you like?': ")

        try:
            choice = int(choice)
            if choice == len(shop_items) + 1:
                return
            if 1 <= choice <= len(shop_items):
                item_name = list(shop_items.keys())[choice - 1] # Finds chosen item
                buy_item(party, item_name)
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid choice.")    # Handles non-integer input

def buy_item(party, item_name):
    item = shop_items[item_name]

    if party.money < item["price"]:
        print("Not enough reeve!")
        return

    party.money -= item["price"]
    party.add_item(item_name)  

    slow_print(f"Bought 1 {item_name}!")


def main():
    print("Here starts the heroic journy...")
    fast_print("Name your party:")
   
    warrior = Warrior(input("Warrior name: "))
    mage = Mage(input("Mage name: "))
    knight = Knight(input("Knight name: "))
    healer = Healer(input("Healer name: "))

    party = Party([warrior, mage, knight, healer])

    while not party.is_defeated():
        for i in range(2):  # Two battles before town and boss
            enemies = generate_enemies(party)

          
            med_print("\nYour party enters the battlefield!")
            slow_print("\nEnemies appear!")

            for e in enemies:
                med_print(f"{e.name} (Level {e.level}) - HP: {e.health}/{e.max_health}")

            battle(party, enemies)

            if party.is_defeated():
                return

            print("\nBattle finished!")

        town_menu(party)

        boss_battle(party)
        
        if party.is_defeated():
            return

        print("\nBattle finished!")

        town_menu(party)

main()