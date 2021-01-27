from random import shuffle


def merge_sort(seq):
    if len(seq) == 1:
        return seq
    mid = len(seq) // 2
    s1 = merge_sort(seq[:mid])
    s2 = merge_sort(seq[mid:])

    i, j, s1_len, s2_len = 0, 0, len(s1), len(s2)
    new_seq = [None] * (s1_len + s2_len)
    while (i + j) < (s1_len + s2_len):
        if (j == s2_len) or (i < s1_len and s1[i] < s2[j]):
            new_seq[i+j] = s1[i]
            i += 1
        else:
            new_seq[i+j] = s2[j]
            j += 1
    return new_seq


a = list(range(5, 20))
shuffle(a)
print(a)
print(merge_sort(a))
