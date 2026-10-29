def result(prime_numbers):
    ''' Stores the list of prime numbers in a .txt file '''
    prime_text = ",".join(prime_numbers) # Convert list to string sep by comma
    with open("AWS/Python/results.txt", "w") as file:
        file.write(prime_text)
    print("Successfully created results.txt")

def is_prime(lower_value, upper_value):
    ''' Lists the prime numbers within a certain range '''
    prime_list = []

    # Edge case: Checks if number 2 is between the lower and upper value
    if (lower_value <= 2) and (upper_value >= 2):
        prime_list.append("2")

    # Checks if the starting value is even or odd
    if lower_value % 2 == 0:
        start = lower_value + 1
    else: 
        start = lower_value

    # Iterates over all odd values in the given range skipping even values
    for num in range(start, upper_value+1, 2):
        if (num > 1):
            prime = True

            # Checks divisibility of the num for all values up to sqrt(num) skipping even values
            for i in range(3, int((num ** 0.5)+1),2):
                if num % i == 0:
                    prime = False
                    break
            if prime:
                prime_list.append(str(num))

    print(prime_list)
    result(prime_list)


def main():
    # Prompts user for an input range
    value_range = input("Give a range of values (separated by space): ")
    (start, end) = value_range.split()

    # Lists the prime numbers within the range
    is_prime(int(start), int(end))

if __name__ == "__main__":
    main()