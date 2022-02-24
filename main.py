num = 100


# print(num)
# print("我是个py")


# print(round(num))


# for i in num:
#     print(i)

def printSomething(age):
    print(age)


def child_or_adult(age):
    if age > 18:
        return "adult"
    else:
        return "child"


# printSomething(20)

# print(child_or_adult(20))


def func():
    global num
    num = 200
    x = num + 100
    print(x)


# func()
# print(num)


if __name__ == '__main__':
    func()