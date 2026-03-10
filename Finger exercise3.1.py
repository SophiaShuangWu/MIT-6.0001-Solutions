num = int(input('Enter an integer: '))
exists = False

# ignore pwr==1, otherwise num**1 == num for all integers
for pwr in range(2, 6):
    if (num >= 0) or (pwr % 2 == 1):
        root = 0
        while root**pwr < abs(num):
            root = root + 1
        if root**pwr == abs(num):
            exists = True
            if num < 0:
                root = -root
            print('root = ', root,', pwr = ', pwr)
            break

if exists == False:
        print('No integer pair root and pwr exists for num =', num)