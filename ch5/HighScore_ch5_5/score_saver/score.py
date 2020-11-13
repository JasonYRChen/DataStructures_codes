class Iterables:
    pass


class ScoreManagement:
    def __init__(self, players: Iterables=None, rank_reserve=10):
        self._players = []
        self._rank = rank_reserve
        if players:
            for player in players:
                self.register(player)

    def __repr__(self):
        title = f"{'Name':<10} {'Score'}"
        output = [title]
        for player in self._players:
            output.append(f"{player.name:<10} {player.score:>5}")
        output = '\n'.join(output)
        return f'{output}'

    def __getitem__(self, item):
        return self._players[item]

    def register(self, new_player):
        for i, player in enumerate(self._players):
            if new_player.score > player.score:
                self._players.insert(i, new_player)
                break
        else:
            self._players.append(new_player)
        if len(self._players) > self._rank:
            del self._players[-1]
        return 'Score update complete.'
