import itertools

i = itertools.count()
n = next

NUL = n(i)

ENTITIES = {
    "SELF": n(i),
    "ENEMY": n(i),
    "FOOD": n(i)
}

DATA = {
    "POSITION": n(i),
    "SIZE": n(i),
    "SPEED": n(i),
    "RANGE": n(i),
    "ENERGY": n(i)
}
