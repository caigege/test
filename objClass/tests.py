# Create your tests here.
def gets():
    return False, 1


a=0
b=0
c=0
for i in range(4):
    print("a:",a,"b : ",b,"c : ",c)
    a=+1;
    b=b+1;
    c+=1;

# eval('print("123"[0:2])')

# print(gets()[0])

json = [{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}, {"id": 5}]
js = {"f": 5}
json.append(js)

# print(js.get())
# json.append(js)
# print(js["f"])
# print(js["d"])
# print(js.get("d"))
# print({"id": 1} in json)
# str = "fafffeee'ssff"
#
# print(str.replace("'", "\""))
# print(json)
for j in json:

    if j.get("id")==1:
        json.remove(j)
    else:
        j["id"]=1111
        # print(json[0].get("id"))
        # print(json[0]["id"])
print(json)
'''

自然界五行人体五音五味五化五色五气五方五季五脏五腑五官形体情志五声变动五神五液角酸生青风东春木肝胆目筋怒呼握魂泪徵苦长赤暑南夏火心小肠舌脉喜笑忧神汗宫甘化黄湿中长夏土脾胃口肉思歌哕意涎商辛收白燥西秋金肺大肠鼻皮悲哭咳魄涕羽咸藏黑寒北冬水肾膀胱耳骨恐呻栗志唾
'''
