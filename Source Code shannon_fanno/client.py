import socket
from functools import reduce
from functools import total_ordering

from math import log2
lst1 = list()

@total_ordering
class Char:
    def __init__(self, name, freq) -> None:
        self._name = name
        self._freq = freq
        self._code = ""

    def __lt__(self, other):
        return True if self._freq < other.get_freq() else False

    def __eq__(self, other):
        return True if self._name == other.get_name() and self._freq == other.get_freq() else False

    def __str__(self):
        return "{0}\t {1}\t {2}".format(self._name, str(self._freq), self._code)

    def __iter__(self):
        return self

    def get_name(self):
        return self._name

    def get_freq(self):
        return self._freq

    def get_code(self):
        return self._code

    def append_code(self, code):
        self._code += str(code)


def find_middle(lst):
    if len(lst) == 1: return None
    s = k = b = 0
    for p in lst: s += p.get_freq()
    s /= 2
    for p in range(len(lst)):
        k += lst[p].get_freq()
        if k == s: return p
        elif k > s:
            j = len(lst) - 1
            while b < s:
                b += lst[j].get_freq()
                j -= 1
            return p if abs(s - k) < abs(s - b) else j
    return


def shannon_fano(lst):
    middle = find_middle(lst)
    if middle is None: return
    for i in lst[: middle + 1]:
        i.append_code(0)
        lst1.append(0)
    shannon_fano(lst[: middle + 1])
    for i in lst[middle + 1:]:
        i.append_code(1)
        lst1.append(1)
    shannon_fano(lst[middle + 1:])

HEADER = 64
PORT = 5053
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

x = ' '
while x != 'quit':
    lst = list()
    m = input('Enter 1 to enter message ')
    if m == '1':
        m = input("message ---> ")
        s = frozenset(m)
        for c in s: lst.append(Char(c, m.count(c)/len(m)))
    elif m == '2':
        i = 1
        while True:
            m = input("{} --->".format(i))
            if m == "":
                print("end")
                break
            m = m.replace(' ', '')
            lst.append(Char(m[: m.find(':')], float(m[m.find(':') + 1:])))
            i += 1
    else:
        lst.append(Char('a', 0.5))
        lst.append(Char('b', 0.25))
        lst.append(Char('c', 0.098))
        lst.append(Char('d', 0.052))
        lst.append(Char('e', 0.04))
        lst.append(Char('f', 0.03))
        lst.append(Char('g', 0.019))
        lst.append(Char('h', 0.011))

    lst.sort(reverse=True)
    shannon_fano(lst)
    h = l = 0
    for c in lst:
        send(str(c))
        # print(c)
        h += c.get_freq() * log2(c.get_freq())
        l += c.get_freq() * len(c.get_code())
        print(c.get_freq())
    h = abs(h)
    # print("H_max = {}".format(log2(len(lst))))
    # print("h = {}".format(h))
    # print("l_cp = {}".format(l))
    # print("K_c.c. = {}".format(log2(len(lst))/l))
    # print("K_o.э. = {}".format(h/l))
    # print(f"message: {lst}")
    # print(len(m))
    # print(len(m)*8/len(lst1)/h)
    # pembagian = len(lst1)/len(m)/l
    send(str(len(m)*8/len(lst1)/h))


send(DISCONNECT_MESSAGE)