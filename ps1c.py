starting_salary = float(input("Enter your the starting salary: "))
portion_left = 0
portion_right = 10000
portion_mid = (portion_left + portion_right) // 2
total_cost = 1000000.0
portion_down_payment = .25
r = .04
semi_annual_raise = .07
count_steps = 0


while portion_left != portion_mid:
    count_steps += 1
    portion_saved = portion_mid / 10000.0
    monthly_salary = starting_salary / 12
    current_savings = 0
    count_months = 0
    for count_months in range(36):
        if (count_months > 0) and (count_months % 6 == 0):
            monthly_salary *= (1 + semi_annual_raise)    
        current_savings += (current_savings * r / 12 + monthly_salary * portion_saved)
        #print("portion_left", portion_left, "portion_right", portion_right, "portion_saved", portion_saved,"current_savings", current_savings)
    
    if current_savings > (portion_down_payment * total_cost - 100.0) and current_savings < (portion_down_payment * total_cost + 100.0):
        message = True
        break

    if current_savings < portion_down_payment * total_cost:
        message = False
        portion_left = portion_mid
    else:
        message = True
        portion_right = portion_mid
    portion_mid = (portion_left + portion_right) // 2

if message == True:
    print("Best savings rate:", portion_saved)
    print("Steps in bisection search:", count_steps)
else:
    print("It is not possible to pay the down payment in three years.")
