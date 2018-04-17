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
            if len(line2) == 3:
                if line2[2] != '':
                    continue
                a, b = line2[0].split(u'，')
                if (len(a) !=7 ) or (len(b) != 7):
                    continue

                a, b = line2[1].split(u'，')

                if (len(a) !=7) or (len(b) != 7):
                    continue

                w.write(line)

                Sum += 1
            elif len(line2) == 5:
                if line2[4] != '':
                    continue
                a, b = line2[0].split(u'，')
                if (len(a) !=7 ) or (len(b) != 7):
                    continue

                a, b = line2[1].split(u'，')
                if (len(a) != 7) or (len(b) != 7):
                    continue

                a, b = line2[2].split(u'，')
                if (len(a) !=7) or (len(b) != 7):
                    continue

                a, b = line2[3].split(u'，')
                if (len(a) !=7) or (len(b) != 7):
                    continue

                w.write(line)

                Sum += 1
        except Exception as e:
            print(x)
        #poems.append(content)
print(Sum)
