#coding=utf-8
__author__ = 'ldd'


def my_split(s, sep=' ', ignore='"'):
    """以seq分割，重复的seq按一个计算，忽略ignore中的seq,返回开始、结束这样的索引数组"""
    ignore_flag = False  # 是否在ignore中
    sep_flag = True  # 上一个是否是
    indexs = []
    for index, i in enumerate(s):
        if i in ignore:
            ignore_flag = not ignore_flag
        elif i == sep:
            if not ignore_flag and not sep_flag:
                sep_flag = True
                indexs[-1].append(index - 1)  # 结束的索引
        else:
            if sep_flag:
                indexs.append([index])  # 开始的索引
            sep_flag = False
    if s[-1] != sep:  # 最后一个不是seq，将最后一个索引添加
        indexs[-1].append(len(s) - 1)
    return indexs
