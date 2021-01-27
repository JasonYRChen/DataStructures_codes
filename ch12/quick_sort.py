from random import randrange, shuffle
from time import time


def quick_sort1(seq):
    if len(seq) < 2:
        return seq
    pivot = seq[randrange(0, len(seq))]
    seq_less, seq_eq, seq_more = [], [], []
    for item in seq:
        if item < pivot:
            seq_less.append(item)
        elif item > pivot:
            seq_more.append(item)
        else:
            seq_eq.append(item)

    seq_less = quick_sort1(seq_less)
    seq_more = quick_sort1(seq_more)
    return seq_less + seq_eq + seq_more


def quick_sort2(seq, start, end):
    # in-place sorting
    seq_len = end - start
    if seq_len < 2:
        return

    pivot = randrange(0, seq_len)
    seq[start], seq[start+pivot] = seq[start+pivot], seq[start]
    pivot, i = start, start+1
    while i < start+seq_len:
        if seq[i] < seq[pivot]:
            seq[pivot+1:i+1], seq[pivot] = seq[pivot:i], seq[i]
            pivot += 1
        i += 1
    quick_sort2(seq, start, pivot)
    quick_sort2(seq, pivot+1, end)


def testing(func, data, repeat):
    start = time()

    for n in range(repeat):
        func(data)
        print(f"{n} round")
    delta = time() - start
    print(f"Total laps: {delta}, average: {delta/repeat}")


# data = list(range(1000000))
# testing(quick_sort1, data, 5)
# testing(quick_sort2, data, 5)

# a = list(range(3, 15))
a = [6.7, 3, 9, 11.2, 5, 32, 65, 7, 3, 11, 9]
shuffle(a)
print(a)
print(quick_sort2(a, 0, len(a)))
print(a)
