def func(**kwargs):
    print("type(kwargs):", type(kwargs),kwargs)
    print("func:",kwargs['x']+kwargs['y'])

func(x=10,y=20)

