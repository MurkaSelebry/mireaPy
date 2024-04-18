class State:
    def __init__(self, play=None, scan=None, skew=None, crash=None):
        self.__play = play
        self.__scan = scan

    @property
    def play(self):
        return self.__play

    @property
    def scan(self):
        return self.__scan


class Mealy:
    def __init__(self):
        self.current_state = 'A'
        self.branches = {'A': State(play=['B', 0], scan=['D', 1]),
                         'B': State(play=['C', 2], scan=['F', 3]),
                         'C': State(scan=['D', 4]),
                         'D': State(play=['E', 5], scan=['B', 6]),
                         'E': State(scan=['F', 7]),
                         'F': State(scan=['D', 8]),
                         'scan_error': State()
                         }

    def play(self):
        curr_method = self.branches[self.current_state].play
        if curr_method:
            self.current_state = curr_method[0]
            return curr_method[1]
        raise MealyError('play')

    def scan(self):
        curr_method = self.branches[self.current_state].scan
        if curr_method:
            self.current_state = curr_method[0]
            return curr_method[1]
        raise MealyError('scan')


class MealyError(Exception):
    pass


def test():
    o = main()
    assert o.play() == 0
    assert o.play() == 2
    assert o.scan() == 4
    assert o.scan() == 6
    assert o.scan() == 3
    assert o.scan() == 8
    assert o.play() == 5
    assert o.scan() == 7
    assert o.scan() == 8
    assert o.play() == 5
    assert o.scan() == 7
    raises(lambda: o.play(), MealyError)
    assert o.scan() == 8
    o.current_state = 'scan_error'
    raises(lambda: o.scan(), MealyError)


def main():
    return Mealy()


def raises(method, error):
    output = None
    try:
        output = method()
    except Exception as e:
        assert type(e) == error
    assert output is None
