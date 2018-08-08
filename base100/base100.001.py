'''
【程序1】

题目：有1、2、3、4个数字，能组成多少个互不相同且无重复数字的三位数？都是多少？
'''


def assemblyList(maxNum):
    for x in range(1, maxNum):
        for y in range(1, maxNum):
            for z in range(1, maxNum):
                if x != y and x != z and y != z:
                    print(x * 100 + y * 10 + z)


assemblyList(5)
