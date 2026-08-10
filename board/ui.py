class PlayerUI:
    def draw(players:tuple[dict], screen, write, coin):
        SCREEN_W, SCREEN_H = screen.get_size()
        for idx, player in enumerate(players):
            match idx:
                case 0: loc = (0, 0)
                case 1: loc = (SCREEN_W-64, 0)
                case 2: loc = (0, SCREEN_H-64)
                case 3: loc = (SCREEN_W-64, SCREEN_H-64)
            screen.blit(player["image"], loc)
            match idx:
                case 0 | 2:
                    l, _ = write(f"{player["coins"]}", loc[0] + 64, loc[1])
                    screen.blit(coin, (loc[0] + 64 + l + 8, loc[1]))
                case _:
                    l, _ = write(f"{player["coins"]}", loc[0], loc[1], extras=('SUB_LENGTH'))
                    screen.blit(coin, (loc[0] - l - 40, loc[1]))