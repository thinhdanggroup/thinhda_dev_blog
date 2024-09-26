def cython_recursive_calc(str data, float threshold):
    cdef list str_arr = data.split(',')
    cdef int length = len(str_arr)

    if length == 1:
        return 0

    cdef float first_value = float(str_arr[0])

    if first_value > threshold:
        return 1 + cython_recursive_calc(",".join(str_arr[1:]), threshold)

    return cython_recursive_calc(",".join(str_arr[1:]), threshold)
