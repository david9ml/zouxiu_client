import functools

def remove_one(x, y):
    print(y)
    y.remove(x)
    return x

y = [0,1,2]
map(functools.partial(remove_one, y=y), [0,1,2])
print(y)
