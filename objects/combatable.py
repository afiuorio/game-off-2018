class CombatObject:
    def __init__(self, hp, attack, defense):
        self.hp = hp
        self.attack = attack
        self.defense = defense
        # FIXME: it may be better if it was damaged_last_turn but where should it be resetted?
        self.damaged = False
        self.nemesis = None

    def attack_target(self, target):
        damage = self.attack - target.defense
        if damage < 0:
            damage = 0
        target.receive_damage(damage)
        target.damaged = True
        target.nemesis = self

    def receive_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.dies()
