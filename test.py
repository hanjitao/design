# encoding=utf-8
import jieba

while True:
    ss = input()

    seg_list = jieba.cut(ss)  # 默认是精确模式
    print(", ".join(seg_list))
