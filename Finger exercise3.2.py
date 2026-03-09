s = '1.23,2.4,3.123'
ans = 0
num = ''

for i in s:
    if i != ',':
        num += i
    else:
        ans += float(num)
        num = ''
        
ans += float(num)
print(ans)