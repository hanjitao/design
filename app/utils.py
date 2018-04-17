# ecoding=utf-8

def splite_poetry(content):
    line = {}
    ss = content.split('。')
    print('ss is', ss)
    s1 = ss[0].split('，')
    s2 = ss[1].split('，')
    line['first'] = s1[0]
    line['second'] = s1[1]
    line['third'] = s2[0]
    line['forth'] = s2[1]
    print(line)
    return line
