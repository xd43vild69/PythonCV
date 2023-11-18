# Example list with repeated values
original_list = [1, 2, 3, 4, 2, 3, 5, 6, 6]

# Create a dictionary to store the count of each item
count_dict = {}

# Count the occurrences of each item in the list
for item in original_list:
    if item in count_dict:
        count_dict[item] += 1
    else:
        count_dict[item] = 1

# Print the original list and the count dictionary
print("Original List:", original_list)

print("Count Dictionary:", count_dict)