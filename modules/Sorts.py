# coding=utf-8

l = [155, 187, 172, 160, 163, 166, 173, 182, 165, 159]

def BubbleSort(l):
    """
    冒烟排序算法
    :param l: 需要排序的列表　
    :return: 返回排序后的列表
    """
    for i in range(len(l) - 1):
        for j in range(len(l) - i - 1):
            if (l[j] > l[j + 1]):
                l[j], l[j + 1] = l[j + 1], l[j]

def SelectSort(l):
    """
    快速排序算法
    :param l: 需要排序的列表
    :return: 返回排序后的列表
    """
    for i in range(len(l) - 1):  # 循环次数
        max = 0
        for j in range(len(l) - i):
            if (l[j] > l[max]):
                max = j
        l[max], l[len(l) - 1 - i] = l[len(l) - 1 - i], l[max]

# 递归方法
def QuickSort(list1, left, right):
    """
    快速排序算法
    :param list1: 需要排序的列表
    :param left: 左边界
    :param right: 右边界
    :return: 返回排序后的列表
    """
    # 出口
    if (left >= right):
        return
    base = list1[left]
    l = left
    r = right
    while (l < r):
        # base的右边比较
        while (l < r):
            if (list1[r] < base):
                list1[r], list1[l] = list1[l], list1[r]
                l += 1
                break
            else:
                r -= 1
        # base的左边比较
        while (l < r):
            if (list1[l] > base):
                list1[l], list1[r] = list1[r], list1[l]
                r -= 1
                break
            else:
                l += 1
    # 递归调用
    QuickSort(list1, left, l - 1)
    QuickSort(list1, r + 1, right)