import math
import time

def find_polynom(points, target):
    # x1 can be zero so shift
    (x1,x2,x3,y1,y2,y3) = points
    if x1 == 0:
        return x2
    if x1 == x2:
        return x2
    k = x2*x2/x1
    l = x3*x3/x1
    if (((k/x1)-1)*(((l)-x3)/(k-x2))-(l/x1-1)) == 0:
        return x2
    c = ((((k*y1/x1)-y2)*(l-x3)/(k-x2))-(((l/x1)*y1)-y3))/(((k/x1)-1)*(((l)-x3)/(k-x2))-(l/x1-1))
    b = ((y1*k/x1)-y2-((k/x1-1)*c))/(k-x2)
    a = (y1-c-x1*b)/(x1*x1)
    c_t = c-target
    det = math.sqrt((b*b) - 4*a*c_t)
    ret1 =  ((-1*b) + det) / (2*a)  
    ret2 = ((-1*b) - det) / (2*a)
    if (x1 < ret1 < x3) and (x1 < ret2 < x3) : 
        return int((ret1 + ret2) / 2)
    if (x1 < ret1 < x3) :
        return int(ret1)
    if (x1 < ret2 < x3) :
        return int(ret2)
    return int(x3)

def poly_prolly_search(values, target):
    steps = 0
    left, right = 0, len(values) - 1

    while left <= right and values[left] <= target <= values[right]:
        steps += 1
        if values[right] == values[left]:
            # avoid division by zero
            offset = 0
        else:
            # calculate the offset using interpolation (prolly search)
            offset = ((target - values[left]) * (right - left)) // (values[right] - values[left])
        mid_p = left + offset
        points = (left, mid_p , right , values[left], values[mid_p], values[right])
        middle = find_polynom(points, target)

        if target == values[middle]:
            return steps, middle
        elif target < values[middle]:
            right = middle - 1
        else:
            left = middle + 1

    return steps, -1



# we are looking for this target value in the given list of values
# returns a tuple:
# first item is the number of comparisons we have to make
# second item is the index if found, return -1 if not found
def binary_search(values, target):
    steps = 0
    left, right = 0, len(values) - 1

    while left <= right:
        steps += 1

        offset = (right-left) // 2
        middle = left + offset

        if target == values[middle]:
            # found
            return steps, middle
        elif target < values[middle]:
            # search the left
            right = middle - 1
        else:
            # search the right
            left = middle + 1
    return steps, -1


# same signature as binary_search
def prolly_search(values, target):
    steps = 0
    left, right = 0, len(values) - 1

    while left <= right and values[left] <= target <= values[right]:
        steps += 1

        # this is the key difference: how we calculate middle.
        # basically we do not split the remaining range in half,
        # but split it proportionally to the difference to target.
        # another key difference is the second part of the while condition above. without it, infinite loops!
        # there should be a way of stopping the infinite looping by checking the offset, but I didn't fully work this out.
        if values[right] == values[left]:
            # avoid division by zero
            offset = 0
        else:
            # calculate the offset using interpolation (prolly search)
            offset = ((target - values[left]) * (right - left)) // (values[right] - values[left])
        middle = left + offset

        if target == values[middle]:
            # found
            return steps, middle
        elif target < values[middle]:
            # search the left
            right = middle - 1
        else:
            # search the right
            left = middle + 1

    return steps, -1

def tripleTest(testname, test_values) :
    print("")
    print(testname)
    binary_total_steps = []
    prolly_total_steps = []
    poly_prolly_total_steps = []
    binary_total_time = []
    prolly_total_time = []
    poly_prolly_total_time = []
    for i in range(100):
        
        test_target = random.randint(0, number_upper_bound)

        start = time.time()
        bin_steps, bin_result = binary_search(test_values, test_target)
        end = time.time()
        binary_total_steps.append(bin_steps)
        binary_total_time.append(end-start)

        start = time.time()
        pro_steps, pro_result = prolly_search(test_values, test_target)
        end = time.time()
        prolly_total_steps.append(pro_steps)
        prolly_total_time.append(end-start)

        start = time.time()
        poly_pro_steps, poly_pro_result = poly_prolly_search(test_values, test_target)
        end = time.time()
        poly_prolly_total_steps.append(poly_pro_steps)
        poly_prolly_total_time.append(end-start)

        if test_values[bin_result] != test_values[pro_result]:
            print("IT'S BROKEN!!!")

    print(f"{'Algoritma':<25} {'Ortalama':<10} {'Min':<10} {'Max':<10} {'Zaman Ort':<12} {'Min Zaman':<12} {'Max Zaman':<12}")
    print("-" * 95)
    print(f"{'Binary_search':<25} {sum(binary_total_steps)/100:<10.2f} {min(binary_total_steps):<10} {max(binary_total_steps):<10} {sum(binary_total_time)/100:<12.4e} {min(binary_total_time):<12.4e} {max(binary_total_time):<12.4e}")
    print(f"{'Prolly_search':<25} {sum(prolly_total_steps)/100:<10.2f} {min(prolly_total_steps):<10} {max(prolly_total_steps):<10} {sum(prolly_total_time)/100:<12.4e} {min(prolly_total_time):<12.4e} {max(prolly_total_time):<12.4e}")
    print(f"{'Poly_Prolly_search':<25} {sum(poly_prolly_total_steps)/100:<10.2f} {min(poly_prolly_total_steps):<10} {max(poly_prolly_total_steps):<10} {sum(poly_prolly_total_time)/100:<12.4e} {min(poly_prolly_total_time):<12.4e} {max(poly_prolly_total_time):<12.4e}")



import random
values_count = 2 ** 20
number_upper_bound = 2 ** 20
random.seed(42)

test_values = []
for i in range(values_count):
    test_values.append(random.randint(0, number_upper_bound))
test_values = sorted(test_values)

tripleTest("Test1 - Random Values", test_values)

test_values = []
mean_value = number_upper_bound / 5
for _ in range(values_count):
    val = int(random.expovariate(1/mean_value))
    # see https://docs.python.org/3/library/random.html#random.expovariate
    test_values.append(min(val, number_upper_bound))
test_values = sorted(test_values)


tripleTest("Test2 - Non Uniform Random Values", test_values)

