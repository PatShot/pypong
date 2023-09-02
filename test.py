# def signs_flipped(A, B):
#     if len(A) != len(B):
#         raise ValueError("Input lists must have the same length")

#     for a, b in zip(A, B):
#         if (a < 0 and b >= 0) or (a >= 0 and b < 0):
#             return True

#     return False

# A_list = [1.4, 3.2]
# B_list = [-1.4, -3.2]

# print(signs_flipped(A_list, B_list))

# center_A = [220, 300]
# dim_A = 50
# dim_B = 5
# center_B = [210, 301]

# print([x-y for x,y in zip(center_A, center_B)])


# from collections import deque

# testq = deque(maxlen=10)

# for i in range(20):
#     testq.append([i, i+1])

# print([x for x, y in testq])

class A():
    def __init__(self, a) -> None:
        self.a = a
    
    def func1(self):
        self.a += 1
        return self.a
    
OBJ = A(a=1)
print(OBJ.func1())
print(OBJ.func2())