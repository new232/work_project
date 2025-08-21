def sort_by_age(person):
    return person['age']

members = [{'name':"이현경", "age":31},
           {'name':"이현루", "age":29},
           {'name':"이민준", "age":22}]

sorted_members = sorted(members, key=sort_by_age(members), reverse=True)
print(sorted_members)