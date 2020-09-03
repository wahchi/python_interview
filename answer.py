
def get_high_score(desk, mine):
    # 你的实现
    pop_mine = sorted(mine).copy()

    result = []
    score = 0

    for i in range(len(desk)):
        j = 0
        while j < len(pop_mine):
            if pop_mine[j] > desk[i]:
                result.append(pop_mine[j])
                pop_mine.remove(pop_mine[j])
                score += 1
                break
            j += 1
        if len(result) != i+1:
            result.append(None)

    # fill None
    for i in range(len(result)):
        if result[i] is None:
            result[i] = pop_mine.pop()

    # return result, score
    return result, score
