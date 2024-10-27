import cython

cpdef int test(int x):
    cdef int y = 1
    cdef int i
    for i in range(1, x+1):
        y *= i
    return y

cpdef list mul_c(list A, list B):
    cdef int a_rows = len(A)
    cdef int a_cols = len(A[0])
    cdef int b_cols = len(B[0])
    cdef int i, j, k
    cdef int temp

    result = [[0 for col in range(b_cols)] for row in range(a_rows)]

    for i in range(a_rows):
        for j in range(b_cols):
            temp = 0
            for k in range(a_cols):
                temp += A[i][k] * B[k][j]
            result[i][j] = temp

    return result

