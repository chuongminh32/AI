 while hero.is_alive() and enemy.is_alive():
        self_play = False
        while True:
            c = input("Bạn muốn tự chơi hay không ? [y/n]")
            if c == 'y':
                self_play = True
                break
            elif c == 'n':
                self_play = False
                break
            else:
                print('Nhập không hợp lệ, vui lòng nhập lại')
                continue
        if self_play:
            while True:
                a = input(print('Nhập 1 để tấn công, Nhập 2 để tấn công đặc biệt'))
                if a == '1':
                    hero.attack(enemy)
                elif a == '2':
                    hero.special_attack(enemy)
                else:
                    print('Nhập không hợp lệ, vui lòng nhập lại')
                    continue
        else:
            while True:
                choose = random.randint(1, 2)
                if choose == 1:
                    hero.attack(enemy)
                    break
                else:
                    hero.special_attack(enemy)
                    break
        # Kết quả trận đấu
        if hero.is_alive():
            print(f"{hero.name} đã chiến thắng!")
        else:
            print(f"{enemy.name} đã chiến thắng!")