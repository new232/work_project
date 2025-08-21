fruits = {'수박':'박과의 여름 과일', '사과':'사과나무의 열매', '딸기':'나무딸기속 식물'}

fruits_keys = fruits.keys()
print(type(fruits_keys)) # <class 'dict_keys'> 딕셔너리 키에 해당. 
print("fruits_keys 딕셔너리 키",fruits_keys)

fruits_keys_lists = list(fruits_keys)
print("fruits_keys 리스트", fruits_keys_lists)
print(type(fruits_keys_lists))

