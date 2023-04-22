#Initialize empty list for Comparable Rents (user input)
comparable_list = []

#initialize vars
sum_comp = 0
min_comp = 100000
max_comp = 0
len_comp = 0

#for loop - 5 values entered
for i in range(0,5):
    
    #input as float
    s = float(input("Enter number: "))
    
    #append to list
    comparable_list.append(s)
    
    #sum floats
    sum_comp = sum_comp + s    #or use sum_comp += s
    
    #count inputs
    len_comp += 1
    
    #find min
    if s == 100000:
        min_comp = s
    elif s < min_comp:
        min_comp = s
    
    #find max
    if s == 0:
        max_comp = s
    elif s > max_comp:
        max_comp = s
        
avg_comp = sum_comp / len_comp
print(f'Max Comp Rent: ${max_comp}')
print(f'Average Rent of Comps is ${avg_comp}')
print(f'Min Comp Rent: ${min_comp}')
print(f'Comps Included: {len_comp}')