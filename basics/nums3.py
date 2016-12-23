"""
With a given integral number n, write a program to generate a dictionary that contains (i, i*i) such that is an integral number between 1 and n (both included). and then the program should print the dictionary.
Suppose the following input is supplied to the program:
"""
print("Enter a number")
inp = int(input());
arr = dict()

for x in range (1,inp+1):
    arr[x] = x*x

print(arr)
    