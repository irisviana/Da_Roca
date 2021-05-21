import re


def validate_cpf(cpf):
    try:
        cpf = str(cpf)
    except:
        return False

    # Cleans any string in CPF
    cpf = re.sub('[^0-9]', '', cpf)
    if not cpf or len(cpf) != 11:
        return False

    # If string is the same number repeated give error
    if len(set(cpf)) == 1:
        return False

    # Take the first 9 numbers to generate the last 2
    calculated_cpf = cpf[:9]

    # Calculate first validation digit
    prod = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    sum_1 = 0
    for i, number in enumerate(prod):
        result = number * int(calculated_cpf[i])
        sum_1 += result

    rest1 = sum_1 % 11
    if rest1 < 2:
        first_digit = 0
    else:
        first_digit = 11 - rest1

    calculated_cpf += str(first_digit)

    # Calculate second validation digit
    prod_2 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    sum_2 = 0
    for i, number in enumerate(prod_2):
        result = number * int(calculated_cpf[i])
        sum_2 += result

    rest2 = sum_2 % 11
    if rest2 < 2:
        second_digit = 0
    else:
        second_digit = 11 - rest2

    calculated_cpf += str(second_digit)

    # If generated number sequence equal given one, return clean sequence
    if calculated_cpf == cpf:
        return calculated_cpf

    return False
