import random

res = [random.randrange(1, 1001, 1) for i in range(100)]  # Generating a list of 100 random numbers between 1 and 1000
new_res = []

# Generating a new list (new_res) containing the ordered values of the original list (res)
while res:
    minimum = res[0]
    for x in res:
        if x < minimum:
            minimum = x
    new_res.append(minimum)
    res.remove(minimum)

# Creating counters to count Totals and Sum values of even and odd numbers
even_count, odd_count, even_sum, odd_sum = 0, 0, 0, 0
for num in new_res:
    if num % 2 == 0:
        even_count += 1
        even_sum += num
    else:
        odd_count += 1
        odd_sum += num

if even_count == 0:  # Division by zero handling
    print("Even count = 0. Can't divide by zero.")
else:
    even_avg = even_sum / even_count
    print("Even average = ", even_avg)

if odd_count == 0:  # Division by zero handling
    print("Even count = 0. Can't divide by zero.")
else:
    odd_avg = odd_sum / odd_count
    print("Odd average = ", odd_avg)
