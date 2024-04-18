class State:
    def __init__(self, share=None, coat=None, skew=None, crash=None):
        self.__share = share
        self.__coat = coat
        self.__skew = skew
        self.__crash = crash

    @property
    def share(self):
        return self.__share

    @property
    def coat(self):
        return self.__coat

    @property
    def skew(self):
        return self.__skew

    @property
    def crash(self):
        return self.__crash


class Mealy:
    def __init__(self):
        self.current_state = 'A'
        self.branches = {'A': State(share=['B', 0], coat=['G', 1]),
                         'B': State(coat=['C', 2], skew=['D', 3]),
                         'C': State(share=['D', 4]),
                         'D': State(share=['E', 5]),
                         'E': State(crash=['F', 6]),
                         'F': State(coat=['G', 7]),
                         'G': State(share=['H', 8], coat=['B', 9]),
                         'H': State(share=['H', 10], coat=['A', 11])
                         }

    @property
    def get_cur_state(self):
        return self.current_state

    @property
    def get_branches(self):
        return self.branches

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

    def crash(self):
        curr_method = self.branches[self.current_state].crash
        if curr_method:
            self.current_state = curr_method[0]
            return curr_method[1]
        raise MealyError('crash')


class MealyError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return self.message
        else:
            return ''


def test():
    o = main()
    o.coat()  # 1
    o.share()  # 8
    o.coat()  # 11
    o.share()  # 0
    o.coat()  # 2
    o.share()  # 4
    o.share()  # 5
    o.crash()  # 6
    o.coat()  # 7
    o.share()  # 8
    o.share()  # 10
    o.share()  # 10
    o.coat()  # 11
    try:
        o.skew()
    except MealyError:
        pass
    finally:
        o.share()


def main():
    return Mealy()
