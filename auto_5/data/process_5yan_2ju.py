# -*- coding:utf-8 -*-

poems=[]
file_name = 'poems.txt.bk'
Sum = 0
x = 0
w = open('poems.txt', "w")
with open(file_name, "r", encoding='utf-8', ) as f:
    for line in f.readlines():
        x += 1
        try:
            title, content = line.strip().split(':')
            content = content.replace(' ', '')
            line2= content.strip().split(u'。')
            #print(line1)
            if len(line2) != 3:
                continue
            if line2[2] != '':
                continue
            a, b = line2[0].split(u'，')
            if (len(a) !=5 ) or (len(b) != 5):
                continue

            a, b = line2[1].split(u'，')

            if (len(a) !=5) or (len(b) != 5):
                continue

            w.write(line)
            poems.append(line)
            Sum += 1
        except Exception as e:
            print(x)
        #poems.append(content)
print(Sum)
