# A program that compares the efficiency of Newton-Raphson and bisection search
epsilon = 0.01
k = 24.0
guess = k/2.0
numGuesses_newton = 0
low = 0.0
high = max(1.0, k)
ans = (high + low)/2.0
numGuesses_bisection = 0

while abs(guess**2 - k) >= epsilon:
    guess = guess - ((guess**2) - k)/(2*guess)
    numGuesses_newton += 1

while abs(ans**2 - k) >= epsilon:
    numGuesses_bisection += 1
    if ans**2 <k:
        low = ans
    else:
        high = ans
    ans = (high + low)/2.0

print('numGuesses_newton =', numGuesses_newton)
print('numGuesses_bisection =', numGuesses_bisection)
if (numGuesses_newton < numGuesses_bisection):
    print('Newton-Raphson method is more efficient')
else:
    print('Bisection search method is more efficient')