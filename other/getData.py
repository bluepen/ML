


def getData(str):
    lists = str.split('\n')
    dic = {}
    for list in lists:
        # dic[list.split(':')[0]] = list.split(':')[1]
        s_index = list.find(':')
        key = list[:s_index].strip()
        value = list[s_index + 1:len(list) + 1]
        dic[key] = value

    return dic

