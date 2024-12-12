import csv

# read csv
def read_chat(id: int):
    with open("chat.csv", mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = list(reader)

    res = list()
    for d in data:
        if d['id'] == str(id):
            res.append(d)
    return res

def read_all_chat():
    with open("chat.csv", mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = list(reader)

    ids = list()
    results = list()
    for d in data[::-1]:
        if d['id'] not in ids:
            ids.append(d['id'])
            results.append({'id':d['id'], 'msg': d['msg'], 'isUser': d['isUser']})
    return results