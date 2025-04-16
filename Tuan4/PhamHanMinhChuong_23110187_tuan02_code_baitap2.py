import random

class Character:
    def __init__(self, name, hp, attack_power):
        self.name = name
        self.hp = hp
        self.attack_power = attack_power
    
    def attack(self, opponent):
        if self.is_alive():
            damage = random.randint(self.attack_power - 2, self.attack_power + 2) # Sát thương dao động từ attack_power - 2 đến attack_power + 2
            opponent.hp -= damage
            print(f"{self.name} tấn công {opponent.name} gây {damage} sát thương!")
    
    def is_alive(self):
        return self.hp > 0

class Hero(Character):
    def special_attack(self, opponent):
        if self.is_alive():
            damage = random.randint(self.attack_power , self.attack_power * 2) # Sát thương dao động từ attack_power đến attack_power * 2
            opponent.hp -= damage
            print(f"{self.name} sử dụng đòn đánh đặc biệt gây {damage} sát thương!")

class Enemy(Character):
    def Enemey_attack(self, opponent):
        if self.is_alive() and self.hp < 20:
            damage = random.randint(self.attack_power , self.attack_power * 2)
            opponent.hp -= damage
            print(f"Quái vật {self.name} sử dụng đòn đánh đặc biệt gây {damage} sát thương!")
        else :
            super().attack(opponent)
    def taunt(self):
        if self.is_alive():
            print(f"{self.name} nói: \"Ngươi sẽ không bao giờ đánh bại ta!\"")

# Khởi tạo nhân vật
hero = Hero("Chiến Binh", 50, 10)
enemy = Enemy("Quái Vật", 50, 10)

auto = False 
c = input("Bạn muốn tự chơi không [y/n] ?: ");
if c == 'y':
    auto = True
else:
    auto = False

if auto == False:
    # Vòng lặp chiến đấu
    while hero.is_alive() and enemy.is_alive():
        action = input("Nhập '1' để tấn công, '2' để dùng đòn đặc biệt: ")
        if action == '1':
            hero.attack(enemy)
        elif action == '2':
            hero.special_attack(enemy)
        else:
            print("Hành động không hợp lệ! Bỏ lượt.")

        if enemy.is_alive():
            enemy.taunt() # Quái vật nói trước khi tấn công
            enemy.Enemey_attack(hero)
        
        print(f"Lượng máu: {hero.name}: {hero.hp} HP | {enemy.name}: {enemy.hp} HP")
        print("-" * 40)

    # Kết quả trận đấu
    if hero.is_alive():
        print(f"{hero.name} đã chiến thắng!")
    else:
        print(f"{enemy.name} đã chiến thắng!")
else:
    while hero.is_alive() and enemy.is_alive():
        hero.attack(enemy)
        if enemy.is_alive():
            enemy.taunt() # Quái vật nói trước khi tấn công
            enemy.Enemey_attack(hero)
        
        print(f"Lượng máu: {hero.name}: {0 if hero.hp < 0 else hero.hp} HP | {enemy.name}: {enemy.hp} HP")
        print("-" * 40)

        # Kết quả trận đấu
        if hero.is_alive():
            print(f"{hero.name} đã chiến thắng!")
        else:
            print(f"{enemy.name} đã chiến thắng!")
