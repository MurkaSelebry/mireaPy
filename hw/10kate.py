class State:
    def __init__(self, share=None, coat=None, skew=None, crash=None):
        self.__share = share
        self.__coat = coat
        self.__skew = skew

    @property
    def share(self):
        return self.__share

    @property
    def coat(self):
        return self.__coat

    @property
    def skew(self):
        return self.__skew


class Mealy:
    def __init__(self):
        self.current_state = 'A'
        self.branches = {'A': State(share=['B', 0], coat=['C', 1],
                                    skew=['G', 2]),
                         'B': State(share=['C', 3]),
                         'C': State(coat=['D', 4]),
                         'D': State(share=['E', 5], skew=['F', 6]),
                         'E': State(coat=['B', 8], skew=['F', 7]),
                         'F': State(coat=['G', 9]),
                         'G': State(),
                         }

    def share(self):
        curr_method = self.branches[self.current_state].play
        if curr_method:
            self.current_state = curr_method[0]
            return curr_method[1]
        raise MealyError('share')

    def coat(self):
        curr_method = self.branches[self.current_state].scan
        if curr_method:
            self.current_state = curr_method[0]
            return curr_method[1]
        raise MealyError('coat')

    def skew(self):
        curr_method = self.branches[self.current_state].skew
        if curr_method:
            self.current_state = curr_method[0]
            return curr_method[1]
        raise MealyError('skew')


class MealyError(Exception):
    pass


def test():
    # Test Mealy initialization
    m = main()
    assert m.current_state == 'A'

    # Test share() method
    assert m.share() == 0
    assert m.current_state == 'B'
    assert m.share() == 3
    assert m.current_state == 'C'
    assert m.coat() == 4
    assert m.current_state == 'D'
    assert m.share() == 5
    assert m.current_state == 'E'
    assert m.coat() == 8
    assert m.current_state == 'B'
    assert m.share() == 3
    assert m.current_state == 'C'
    assert m.coat() == 4
    assert m.current_state == 'D'
    assert m.skew() == 6
    assert m.current_state == 'F'
    assert m.coat() == 9
    assert m.current_state == 'G'
    raises(lambda: m.share(), MealyError)

    # Test coat() method
    m.current_state = 'A'
    assert m.coat() == 1
    assert m.current_state == 'C'
    assert m.coat() == 4
    assert m.current_state == 'D'
    assert m.share() == 5
    assert m.current_state == 'E'
    assert m.skew() == 7
    assert m.current_state == 'F'
    assert m.coat() == 9
    assert m.current_state == 'G'
    raises(lambda: m.coat(), MealyError)

    # Test skew() method
    m.current_state = 'A'
    assert m.skew() == 2
    assert m.current_state == 'G'
    m.current_state = 'D'
    assert m.skew() == 6
    assert m.current_state == 'F'
    raises(lambda: m.skew(), MealyError)


def main():
    return Mealy()


def raises(method, error):
    output = None
    try:
        output = method()
    except Exception as e:
        assert type(e) == error
    assert output is None
