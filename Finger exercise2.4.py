numXs = int(input('How many times should I print the letter X?'))
toPrint = ''
# Handle negative numXs
itersLeft = abs(numXs)
while (itersLeft != 0):
    toPrint += 'X'
    itersLeft -=1
print(toPrint)