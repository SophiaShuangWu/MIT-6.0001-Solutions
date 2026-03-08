x = int(input("Enter an integer x: "))
y = int(input("Enter an integer y: "))
z = int(input("Enter an integer z: "))

if x % 2 ==1:
    if (y % 2 ==1) and (x < y):
        if (z % 2 == 1) and (z > y):
            print(z)
        else:
            print(y)
    elif (z % 2 ==1) and (x < z):
        print(z)
    else:
        print(x)
elif (y % 2 ==1) and (z % 2 ==1):
    if (y < z):
        print(z)
    else:
        print(y)
elif y % 2 ==1:
    print(y)
elif z % 2 ==1:
    print(z)
else:
    print("No odd numbers")