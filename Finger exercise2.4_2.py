itersLeft = 10
tag = False

while (itersLeft != 0 and not tag):
    num = int(input('Enter an integer:'))
    if num % 2 == 1:
        tag = True
        numPrint = num
    itersLeft -= 1

if itersLeft != 0:
    while itersLeft != 0:
        num = int(input('Enter an integer: '))
        if (num % 2 == 1) and (num > numPrint):
            numPrint = num
        itersLeft -= 1
    print('The largest odd number is:', numPrint)
elif tag == True:
    print('The largest odd number is:', numPrint)
else:
    print('No odd number was entered.')