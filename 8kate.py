from re import split


def main(s):
    split_list = list(filter(None, split(
        " |'|def|@|<=|[[]|[]]|\n", s)))
    res = [(split_list[i], int(split_list[i + 1])) for i in range(
        0, len(split_list), 2)]
    return dict(res)

s = "[ def @'bela_252' <= 7656 def @'iser_675'<= -3440 def " \
    "@'iser_181' \
<=-5042 ]"

print(main(s))
