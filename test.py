import functools

def remove_one(x):
    global y
    print(y)
    y+=1
    return x

y = 1
map(functools.partial(remove_one), [0,1,2])
print(y)
