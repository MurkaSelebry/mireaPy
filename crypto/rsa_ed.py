from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64
from sympy import randprime, mod_inverse
from random import choice


class Encryption(object):
    def __init__(self):
        self.random_generator = Random.new().read

    def generate_p_q(self):
        print(2 ** 29)
        p = randprime(2 ** 100, 2 ** 101)
        q = randprime(2 ** 100, 2 ** 101)
        return p, q

    '''
    def getKey(self):
       # Generate p and q
       p, q = self.generate_p_q()
       # rsa algorithm generation example
       rsa = RSA.construct((p * q, 65537))  # 65537 is a common choice for e
       # Master's key pair generation
       private_pem = rsa.exportKey()
       public_pem = rsa.publickey().exportKey()
       key = {}
       key["private"] = private_pem
       key["public"] = public_pem
       return key
    '''

    def getKey(self, p=0, q=0, e=0):
        if (p == 0):
            (p, q) = self.generate_p_q()
            print(p, q)
            e = choice([17, 257, 65537])
        n = p * q
        phi = (p - 1) * (q - 1)
        d = mod_inverse(e, phi)

        rsa1 = RSA.construct((n, e, d, p, q))
        print("dsadsa", rsa1.size_in_bits())
        rsa = RSA.generate(1024, self.random_generator)
        print("dsads1a", rsa.size_in_bits())

        private_pem = rsa1.exportKey()
        public_pem = rsa1.publickey().exportKey()
        key = {}
        key["private"] = private_pem
        print(len(private_pem))
        key["public"] = public_pem
        print("pdsppd", len(public_pem))

        return key

    def rsa_long_encrypt(self, msg, pub_key_str, length=100):

        length = 14
        pubobj = RSA.importKey(pub_key_str)
        pubobj = Cipher_pkcs1_v1_5.new(pubobj)
        res = []
        for i in range(0, len(msg), length):
            res.append(
                str(
                    base64.b64encode(pubobj.encrypt(
                        msg[i:i + length].encode(encoding="utf-8"))), 'utf-8'
                )
            )

        return "".join(res)

    def rsa_long_decrypt(self, msg, priv_key_str, length=172):

        length = 36
        privobj = RSA.importKey(priv_key_str)
        privobj = Cipher_pkcs1_v1_5.new(privobj)
        res = []
        for i in range(0, len(msg), length):
            res.append(
                str(
                    privobj.decrypt(
                        base64.b64decode(msg[i:i + length])
                        , 'xyz'), 'utf-8'
                )
            )
        return "".join(res)

    def cut_string(self, message, length=14):
        result = []
        temp_char = []
        for msg in message:
            msg_encode = msg.encode("utf-8")
            temp_encode = "".join(temp_char).encode("utf-8")
            if len(temp_encode) + len(
                    msg_encode) <= length:
                temp_char.append(msg)
            else:
                result.append("".join(temp_char))
                temp_char.clear()
                temp_char.append(msg)
        result.append("".join(temp_char))
        return result

    def rsa_encrypt_file(self, file_path, save_path, pub_key):

        with open(file_path, "r", encoding="utf-8") as f:
            line = f.readline()
            while line:
                cut_lines = self.cut_string(line)
                for cut_line in cut_lines:
                    context = self.rsa_long_encrypt(cut_line, pub_key)
                    with open(save_path, "a", encoding="utf-8") as w:
                        w.write(context + "\n")
                line = f.readline()

    def rsa_decrypt_file(self, file_path, save_path, priv_key):

        with open(file_path, "r", encoding="utf-8") as f:
            line = f.readline()
            while line:
                context = self.rsa_long_decrypt(line.strip("\n"), priv_key)
                with open(save_path, "a", encoding="utf-8") as w:
                    w.write(context)
                line = f.readline()


if __name__ == '__main__':
    str1 = "fsdflslkdasdjajdlkajskdjalksjdlkjsdjkasjdlksajlkdajslkjdlkasjlkdjalkdjlkasl"
    a = Encryption()
    choose = input("Хотите ввести свои параметры (p,q,e): (y/n)")
    if choose == 'y':
        p = int(input("p = "))
        q = int(input("q = "))
        e = int(input("e = "))
        key = a.getKey(p, q, e)
    else:
        key = a.getKey()
    prikey = '-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQC5GOlknwPrENofdQcu5oXBrVcyPkjkjXIry7Lp3NKwSRqCue+7\nNrfnJ6qoihTu79Ux4i/8F8PwOTub12FfiR6+4Uo8PeLk4l3plriZUPyuLVM2Qjoh\n8VPEF9E5eggN9CmGWdlCcvgNrag0RoO5gWkG4sadtTAep3Z0xVsY+jevbwIDAQAB\nAoGACBvORaktq8OOOqiOywAwRd7JHhtaaCDGKqL+0H3rAOwC7E0m8mWgQtEbCc0a\nw6jgBxJolbuYytJHCTmzO1MvdIwd1iRfYBqkZT71GxRvsPwN014/TleRRtPR14/s\nyzShjQFxX+QSerF6UYZqWVk8zQm4aWBQ8m5mMd/4ImkLRckCQQDLICMNeNf5QrpI\nFAGZuHYK6Nf/RJHy95O4pd7V8RQ4M3e3nd1VTBKsK8u09lN0SiFtBpH//cDU/Sv9\nR6L52IurAkEA6UdpVQQW5VENTYqkPXvpVUIG3vE62ZFjAqSWfkA/mouIyzcVzl5s\n9zsMZJ+FS/hwyEd7jFRFziNNZ1QS1MwHTQJAJTe2NHm32MwJJbvEr03FEyqmqPb/\nZu1F+8colTqe4c1MWjBqpX5SzYkYwgeAMwaCKV/S0HzGIEBjFv1RN0YeEQJBALmL\nylULtqZZDIqzjqU0zMe6h7qGBvgMcsMkZGsw8SYcfAae3uJRKryOo/HZC+38QsCa\nUsOwOAGZBLT+IyhMzDUCQAm6uJ07t9msJ6IBbp7VvscX9yAGiIvfMEmLWuUkmZXx\nluoyK+3fcPyloPFXp1IfGO+i8oDFjKzmQ9PlaP29aPk=\n-----END RSA PRIVATE KEY-----'
    pubkey = '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC5GOlknwPrENofdQcu5oXBrVcy\nPkjkjXIry7Lp3NKwSRqCue+7NrfnJ6qoihTu79Ux4i/8F8PwOTub12FfiR6+4Uo8\nPeLk4l3plriZUPyuLVM2Qjoh8VPEF9E5eggN9CmGWdlCcvgNrag0RoO5gWkG4sad\ntTAep3Z0xVsY+jevbwIDAQAB\n-----END PUBLIC KEY-----'
    print(key["private"])
    print(key["public"])
    print(str1)
    cipher_text = a.rsa_long_encrypt(str1, key["public"])
    print(cipher_text)
    plaintext = a.rsa_long_decrypt(cipher_text, key["private"])
    print(plaintext)
    a.rsa_encrypt_file('enc.txt', 'enc1.txt', key["public"])
    a.rsa_decrypt_file('enc1.txt', 'dec1.txt', key["private"])

# p = 2493372152845847296329163017107
# q = 1948350438503796371183576430341
# e = 65537
