class State:
    def __init__(self, scale=None, snap=None, chat=None, crash=None):
        self.__scale = scale
        self.__snap = snap
        self.__chat = chat
        self.__crash = crash

    @property
    def scale(self):
        return self.__scale

    @property
    def snap(self):
        return self.__snap

    @property
    def chat(self):
        return self.__chat

    @property
    def crash(self):
        return self.__crash


class Mealy:
    def __init__(self):
        self.current_state = 'A'
        self.branches = {'A': State(scale=['B', 0], snap=['G', 1]),
                         'B': State(snap=['C', 2], chat=['D', 3]),
                         'C': State(scale=['D', 4]),
                         'D': State(scale=['E', 5]),
                         'E': State(crash=['F', 6]),
                         'F': State(snap=['G', 7]),
                         'G': State(scale=['H', 8], snap=['B', 9]),
                         'H': State(scale=['H', 10], snap=['A', 11])
                         }

    def scale(self):
        curr_method = self.branches[self.current_state].scale
        if curr_method:
            self.current_state = curr_method[0]
            return curr_method[1]
        raise MealyError('scale')

    def snap(self):
        curr_method = self.branches[self.current_state].snap
        if curr_method:
            self.current_state = curr_method[0]
            return curr_method[1]
        raise MealyError('snap')

    def chat(self):
        curr_method = self.branches[self.current_state].chat
        if curr_method:
            self.current_state = curr_method[0]
            return curr_method[1]
        raise MealyError('chat')

    def crash(self):
        curr_method = self.branches[self.current_state].crash
        if curr_method:
            self.current_state = curr_method[0]
            return curr_method[1]
        raise MealyError('crash')


class MealyError(Exception):
    pass


def test():
    o = main()
    assert o.snap() == 1
    raises(lambda: o.chat(), MealyError)
    raises(lambda: o.crash(), MealyError)
    assert o.scale() == 8
    raises(lambda: o.chat(), MealyError)
    raises(lambda: o.crash(), MealyError)
    assert o.snap() == 11
    raises(lambda: o.chat(), MealyError)
    raises(lambda: o.crash(), MealyError)
    assert o.scale() == 0
    raises(lambda: o.scale(), MealyError)
    raises(lambda: o.crash(), MealyError)
    assert o.snap() == 2
    raises(lambda: o.snap(), MealyError)
    raises(lambda: o.chat(), MealyError)
    raises(lambda: o.crash(), MealyError)
    assert o.scale() == 4
    raises(lambda: o.snap(), MealyError)
    raises(lambda: o.chat(), MealyError)
    raises(lambda: o.crash(), MealyError)
    assert o.scale() == 5
    raises(lambda: o.scale(), MealyError)
    raises(lambda: o.snap(), MealyError)
    raises(lambda: o.chat(), MealyError)
    assert o.crash() == 6
    raises(lambda: o.scale(), MealyError)
    raises(lambda: o.chat(), MealyError)
    raises(lambda: o.crash(), MealyError)
    assert o.snap() == 7
    raises(lambda: o.chat(), MealyError)
    raises(lambda: o.crash(), MealyError)
    assert o.scale() == 8
    raises(lambda: o.chat(), MealyError)
    raises(lambda: o.crash(), MealyError)
    assert o.scale() == 10
    raises(lambda: o.chat(), MealyError)
    raises(lambda: o.crash(), MealyError)
    assert o.scale() == 10
    raises(lambda: o.chat(), MealyError)
    raises(lambda: o.crash(), MealyError)
    assert o.snap() == 11
    raises(lambda: o.chat(), MealyError)
    raises(lambda: o.crash(), MealyError)
    assert o.snap() == 1
    raises(lambda: o.chat(), MealyError)
    raises(lambda: o.crash(), MealyError)
    assert o.snap() == 9
    raises(lambda: o.scale(), MealyError)
    raises(lambda: o.crash(), MealyError)
    assert o.chat() == 3
    raises(lambda: o.chat(), MealyError)
    raises(lambda: o.snap(), MealyError)
    raises(lambda: o.chat(), MealyError)
    assert o.scale() == 5
    raises(lambda: o.scale(), MealyError)
    raises(lambda: o.snap(), MealyError)
    raises(lambda: o.chat(), MealyError)
    raises(lambda: o.scale(), MealyError)
    assert o.crash() == 6
    raises(lambda: o.scale(), MealyError)
    raises(lambda: o.chat(), MealyError)
    raises(lambda: o.crash(), MealyError)


def main():
    return Mealy()


def raises(method, error):
    output = None
    try:
        output = method()
    except Exception as e:
        assert type(e) == error
    assert output is None

test()