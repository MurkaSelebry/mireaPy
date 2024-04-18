class MealyError(Exception):
    pass


class StateMachine:
    def __init__(self):
        self.state = 'A'

    def wreck(self):
        if self.state == 'A':
            self.state = 'B'
            return 0
        if self.state == 'C':
            self.state = 'D'
            return 3
        if self.state == 'E':
            self.state = 'B'
            return 7
        if self.state == 'G':
            self.state = 'G'
            return 9
        raise MealyError('wreck')

    def peep(self):
        if self.state == 'A':
            self.state = 'C'
            return 1
        if self.state == 'B':
            self.state = 'C'
            return 2
        if self.state == 'C':
            self.state = 'F'
            return 4
        if self.state == 'D':
            self.state = 'E'
            return 5
        if self.state == 'E':
            self.state = 'F'
            return 6
        if self.state == 'F':
            self.state = 'G'
            return 8
        raise MealyError('peep')


def main():
    return StateMachine()


def raises(func, error):
    output = None
    try:
        output = func()
    except Exception as e:
        assert type(e) == error
    assert output is None


def test():
    o = main()
    assert o.wreck() == 0
    assert o.peep() == 2
    assert o.wreck() == 3
    assert o.peep() == 5
    assert o.wreck() == 7
    assert o.peep() == 2
    assert o.peep() == 4
    assert o.peep() == 8
    assert o.wreck() == 9

    o = main()
    assert o.peep() == 1
    assert o.wreck() == 3
    raises(lambda: o.wreck(), MealyError)
    assert o.peep() == 5
    assert o.peep() == 6
    assert o.peep() == 8
    raises(lambda: o.peep(), MealyError)

