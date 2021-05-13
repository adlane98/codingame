def merge(arr1, arr2):
    sort_arr = []
    i = 0
    j = 0

    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            sort_arr.append(arr1[i])
            i += 1
        else:
            sort_arr.append(arr2[j])
            j += 1

    if i < len(arr1):
        sort_arr.extend(arr1[i:])
    elif j < len(arr2):
        sort_arr.extend(arr2[j:])

    return sort_arr


def divide(arr):
    return arr[:int(len(arr)/2)], arr[int(len(arr)/2):]


def merge_sort(arr):
    if len(arr) > 1:
        arr1, arr2 = divide(arr)
        sarr1 = merge_sort(arr1)
        sarr2 = merge_sort(arr2)
        return merge(sarr1, sarr2)
    return arr


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(merge_sort([8, 6, 9, 4, 0, -1, -7, 5, -14, 65]))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
