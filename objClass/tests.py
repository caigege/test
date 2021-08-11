# Create your tests here.
def gets():
    return False, 1


# print(gets()[0])

json = [{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}, {"id": 5}]
js = {"f": 5}
print(js.get())
json.append(js)
# print(js["f"])
# print(js["d"])
# print(js.get("d"))
print({"id": 1} in json)
str = "fafffeee'ssff"

print(str.replace("'", "\""))
# print(json)
# for j in json:
#     if j.get("id")==1:
#         json.remove(j)
#     else:
#         j["f"]=1
#         print(json[0].get("id"))
#         print(json[0]["id"])
# print(json)
