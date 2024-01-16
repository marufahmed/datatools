ints=[1,2,3]
def calculate_sum(ints):
    start_index, end_index = 0,len(ints)-1
    total = 0  # Initialize total sum
    while start_index<=end_index:
        if start_index == end_index:  # If list has odd number of elements
            pair_sum = ints[start_index]
        else:
            pair_sum = ints[start_index] + ints[end_index]
        print(f"integer at starting index={ints[start_index]} and integer at ending index={ints[end_index]} and sum of them is: {pair_sum}")
        total += pair_sum  # Add pair_sum to total
        start_index+=1
        end_index-=1
    return total
print(f"Total:",calculate_sum(ints))

calculate_sum(ints)