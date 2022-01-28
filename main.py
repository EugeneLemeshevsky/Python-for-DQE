import random  

res = [random.randrange(1, 1001, 1) for i in range(100)]
print(res)  #
new_res = []

while res:
    minimum = res[0]
    for x in res:
        if x < minimum:
            minimum = x
    new_res.append(minimum)
    res.remove(minimum)
print(new_res)

even_count, odd_count, even_sum, odd_sum = 0, 0, 0, 0
for num in new_res:
    if num % 2 == 0:
        even_count += 1
        even_sum += num
    else:
        odd_count += 1
        odd_sum += num
print("Even numbers in the list: ", even_count, even_sum)
print("Odd numbers in the list: ", odd_count, odd_sum)

even_avg = even_sum / even_count
odd_avg = odd_sum / odd_count

print(even_avg, odd_avg)
