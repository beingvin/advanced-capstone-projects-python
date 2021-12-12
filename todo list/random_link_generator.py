# Python3 code to demonstrate
# generating random strings
# using random.choices()
import string
import random

# initializing size of string
N = 10

# using random.choices()
# generating random strings
random_link = ''.join(random.choices(string.ascii_lowercase +
							string.digits, k = N))

# print result
# print("The generated random string : " + str(res))
