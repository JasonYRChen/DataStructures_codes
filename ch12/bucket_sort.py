from random import randrange


def bucket_sort(data, end):
    bucket = [[] for _ in range(end)]
    for i in data:
        bucket[i].append(i)
    result = []
    result.extend(num for item in bucket for num in item)
    return result


data = [randrange(5) for _ in range(20)]
print(data)
print(bucket_sort(data, 5))
