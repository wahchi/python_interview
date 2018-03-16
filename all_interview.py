# 面试题
# 凯兰高集团周三下午都有康体,其中一周的主题为数字大比拼

# 规则如下:
# 桌面上有数字卡片, 它们对应的数字[A1,A2,A3, .. An](顺序不可变), 你手上卡片的数字有[B1, B2, B3, .. Bn]
# 按照某个顺序摆放, 若当前位置卡片上的数字大于桌面上的数字, 你就能够积1分, 若不能, 则积0分

# 如:桌面上卡片的数字[6, 5, 4, 1], 你手中卡片的数字[3, 2, 2, 1],
#         如果你按照[3, 2, 1, 2] 摆放, 你就能获得最高1分 ;
#         如果你按照[3, 2, 2, 1] 摆放, 你就只能获得0分 ;

# 请问如何安排卡片顺序, 能够获得的分数最高?
# 要求: 按照给定桌面上卡片数字的列表, 以及你手上的卡片数字列表, 输出一个元组A, A=(摆放列表, 你能获得的最高分数)


# 解
import copy
import pandas as pd


def get_high_score(table, hand):
    # 最快想到的保留索引信息的方法...
    ts = pd.Series(table)

    # 桌面上的卡片排序
    tss = ts.sort_values(ascending=False)
    ind = list(tss.index)
    t = list(tss.values)

    # 如果不copy, 会影响到外面的参数
    h = copy.copy(hand)
    h.sort(reverse=True)

    # 初设值
    n = []  # 最优解
    rn = list(range(len(t)))  # 按排序前的位置放
    win = 0  # 获得的分数

    # 若最大的比不上最大的,就用最小的顶上
    for i in t:
        if h[0] <= i:
            n.append(h.pop(-1))
        else:
            n.append(h.pop(0))
            win += 1

    # 手上卡片, 按桌面原先的顺序摆好
    for i in range(len(t)):
        rn[ind[i]] = n[i]

    return rn, win


if __name__ == '__main__':
    table = [3, 2, 1, 1, 2, 3]
    hand = [1, 2, 3, 3, 2, 1]
    n, win = get_high_score(table=table, hand=hand)
    print(n, win)


# 单元测试验证
import pytest
from pydash import collections


def check_hit(t, h):
    """
    # 检查按顺序获得的分数
    :param t: list, 桌面的数字列表
    :param h: list, 手上的数字列表
    :return:  int, 获得的分数
    """
    hit = collections.filter_(list(zip(t, h)), lambda x: x[0] > x[1])
    return len(hit)


@pytest.mark.parametrize('high, low, result, name', [
    ([6, 5, 4, 1], [3, 2, 2, 1], 1, 'demo'),
    ([3, 2, 1], [3, 2, 1], 2, '倒序'),
    (list(range(999))[::-1], list(range(999))[::-1], 999-1, '大量倒序'),
    ([2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], 0, '全等'),
    ([4, 3, 2, 1, 0, -1], [5, 4, 3, 2, 2, 1], 6, '有负分数'),
    ([1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], 5, '正序'),
    (list(range(999)), list(range(999)), 999 - 1, '大量正序'),
    ([3, 2, 1, 1, 2, 3], [1, 2, 3, 3, 2, 1], 4, '不定序')
])
def test_get_high_score(high, low, result, name):
    res = get_high_score(high, low)
    score = check_hit(res[0], high)
    assert res[1] == result == score