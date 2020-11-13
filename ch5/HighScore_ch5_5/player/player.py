from ch5.HighScore_ch5_5.deco import decorates as deco


@deco.property_decoration()
class Player:
    name = deco.NameProperty()
    score = deco.PositiveIntegerProperty()

    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.score})"


if __name__ == '__main__':
    j = Player('j', 5)
    print(j)
