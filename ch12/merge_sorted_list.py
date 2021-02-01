from random import randrange


def merge_sorted_list(l1, l2):
    """
    Both input list should be sorted in ascending form
    """

    i = j = 0
    result = []
    while i+j < len(l1)+len(l2):
        item, is_l1 = (l1[i], True) if j == len(l2) or (i < len(l1) and l1[i] < l2[j]) else (l2[j], False)
        i += 1 if is_l1 else 0
        j += 1 if not is_l1 else 0
        if not result or item != result[-1]:
            result.append(item)
    return result


a = [randrange(0, 19) for _ in range(10)]
b = [randrange(0, 10) for _ in range(20)]
aa = sorted(a)
bb = sorted(b)
ans = list(set(a) | set(b))
ans.sort()
ans2 = merge_sorted_list(aa, bb)
print(a)
print(b)
print(ans)
print(ans2)
print(ans == ans2)
