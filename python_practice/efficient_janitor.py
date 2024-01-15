bags=[1.1,1.2,1.5,2.8,2.1,1.7,1.3,1.9,2.0,2.2,2.3,2.4,2.5,2.6,2.7,2.9]

def trips(bags):
    """
    This function calculates the minimum number of trips the janitor has to make.
    It takes as input a list of bag weights and returns the minimum number of trips.
    Each trip can carry a maximum weight of 3.0.

    Parameters:
    bags (list): A list of floats representing the weights of the bags.

    Returns:
    int: The minimum number of trips the janitor has to make.
    """
    sorted_bags=sorted(bags,reverse=True)
    trips=0
    i,j=0,len(sorted_bags)-1 #This line is using Python's multiple assignment feature. The values on the right side of the = are being assigned to the variables on the left side in the same order
    while i<=j:
        if sorted_bags[j]+sorted_bags[i]<=3.0:
            print(f"Taking bags {i+1} (weight {sorted_bags[i]}) and {j+1} (weight {sorted_bags[j]}) : combined weight {sorted_bags[j]+sorted_bags[i]}")
            j-=1
        else:
            print(f"Taking bag {i+1} (weight {sorted_bags[i]})")
            i+=1
        trips+=1
    return trips

trips(bags)
