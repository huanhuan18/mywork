import random
def sum_judge(former, later, n):
    if former + later >= n:
        return False
    else:
        return True

def main(n, m):
    money = n
    sum = 0
    for i in range(m):
        div = random.randint(0, n)
        while True:
            if sum_judge(sum, div, n):
                if i != m-1:
                    money -= div
                    sum += div
                    print("第{}个人分了{}元".format(i+1, div))
                    break
                else:
                    div = money
                    print("第{}个人分了{}元".format(i + 1, div))
                    break
            else:
                div = random.randint(0, n)

if __name__ == '__main__':
    main(90, 4)