def main(s):
    n = int(s)
    q1 = 0b1111111111 & n
    q2 = 0xff1 & (n>>10)
    q3 = 0xf1 & (n>>19)
    q4= 0x111f & (n>>24)
    q5 = 0x111 & (n>>30)
    q6 = 0x111 &(n>>34)
    return [q1,q2,q3,q4,q5,q6]

print(main('31558779789'))