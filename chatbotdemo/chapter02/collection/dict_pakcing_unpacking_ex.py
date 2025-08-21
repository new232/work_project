def sum(x,y):
    print("func2:",x+y)

def packing(**kwargs):
    print("type(kwargs:)",type(kwargs),kwargs)
    print("func1 : ", kwargs['x']+kwargs['y'])
    sum(**kwargs)

packing(x=10,y=20)