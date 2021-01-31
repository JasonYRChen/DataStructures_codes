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
    # in-place sorting(?) with non-constant memory usage
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


def quick_sort3(seq, start, end):
    # in-place sorting
    if end - start < 2:
        return
    pivot = randrange(start, end)
    end -= 1
    seq[pivot], seq[end] = seq[end], seq[pivot]
    left, right = start, end - 1
    while left <= right:
        while seq[left] <= seq[end] and left <= right:
            left += 1
        while seq[right] > seq[end] and left <= right:
            right -= 1
        if left < right:
            seq[left], seq[right] = seq[right], seq[left]
    seq[end], seq[left] = seq[left], seq[end]
    quick_sort3(seq, start, left)
    quick_sort3(seq, left+1, end+1)


def testing(func, data, repeat, *args):
    start = time()

    for n in range(repeat):
        func(data, *args)
        print(f"{n} round")
    delta = time() - start
    print(f"Total laps: {delta}, average: {delta/repeat}")


data = list(range(1000000))
testing(quick_sort1, data, 5)
testing(quick_sort2, data, 5, 0, len(data))
testing(quick_sort3, data, 5, 0, len(data))

# a = list(range(3, 15))
# a = [6.7, 3, 9, 11.2, 5, 32, 65, 7, 3, 11, 9]
# shuffle(a)
# print(a)
# quick_sort3(a, 0, len(a))
# print(a)
# print(a == [3, 3, 5, 6.7, 7, 9, 9, 11, 11.2, 32, 65])
