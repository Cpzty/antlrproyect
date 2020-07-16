import graphviz

class Dictlist(dict):
    def __setitem__(self, key, value):
        try:
            self[key]
        except KeyError:
            super(Dictlist, self).__setitem__(key, [])
        self[key].append(value)
d = Dictlist()
with open("test.txt") as f:
    for line in f:
        (key, val) = line.split()
        d[int(key)] = val

for value in d.values():
    print(value)
