def func(x,y):
    print("func:")
    return x+y

dict_var = {"x":10,"y":20}
func(**dict_var)