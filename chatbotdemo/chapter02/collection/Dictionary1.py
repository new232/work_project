# dictionary : 말처럼 사전같은 자료형. 낱말에 해당하는 key 뜻에 해당하는 value로 구성. 중복을 허용하지 않음. 
# list가 배열처럼 대괄호로 묶었다면 dictionary는 {}로 묶음

fruits = {'수박':'박과의 여름 과일', '사과':'사과나무의 열매', '딸기':'나무딸기속 식물'}
print("모든과일", fruits)

print("모든과일", fruits['수박'], fruits['사과'], fruits['딸기'])
#딕셔너리는 리스트의 인덱스처럼 키값으로 요소에 접근함. 

print(type(fruits))