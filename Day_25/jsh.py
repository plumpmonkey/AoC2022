from sys import argv
from time import perf_counter


def read_file(filename):
    with open(filename) as file:
        text = file.read()
    return text


def get_input_file():
    if len(argv) == 1:
        return "sample.txt"
    elif len(argv) == 2:
        return argv[1] if argv[1] != "i" else "input.txt"


def calculate(digit, power, second):
    if second:
        return digit * 5**power - -2 * 5 ** (power - 1)
    return digit * 5**power


def padd(alist, n):
    return ["0"] * (n) + list(alist)


def add(num1, num2):
    """Input should be list of strings or strings"""
    new = []
    extra = 0
    convert = {
        "2": 2,
        "1": 1,
        "0": 0,
        "-": -1,
        "=": -2,
        2: "2",
        1: "1",
        0: "0",
        -1: "-",
        -2: "=",
    }
    if len(num1) > len(num2):
        num2 = padd(num2, len(num1) - len(num2))
    else:
        num1 = padd(num1, len(num2) - len(num1))
    for n1, n2 in zip(num1[::-1], num2[::-1]):
        number = convert[n1] + convert[n2] + extra
        if number > 2:
            new.append(convert[number - 5])
            extra = 1
        elif number < -2:
            extra = -1
            new.append(convert[number + 5])
        else:
            new.append(convert[number])
            extra = 0
    if extra:
        new.append(str(extra))
    return list(reversed(new))


def fix(alist):
    """['2-', '1', '2='] -> ['2', '-', '1', '2', '=']"""
    output = []
    for item in alist:
        output.extend(list(item))
    return output


def snafu(score):
    """Converts from decimal to snafu"""
    flag = True
    current = ["1", "0"]
    numbers = ["1", "2", "1=", "1-"]
    while True:
        if decimal(current) < score:  # finds the decimal places
            current.append("0")
        else:
            current.pop()
            break
    while flag:
        for i, lead in enumerate(numbers):
            current[0] = lead
            if decimal("".join(current)) > score:
                current[0] = numbers[i - 1]
                flag = False
                break
            elif i == 3:
                flag = False
                break

    current = fix(current)
    remaining = score - decimal("".join(current))
    if remaining == 0:
        return "".join(current)
    return "".join(add(current, snafu(remaining)))


def decimal(num):
    score = 0
    convert = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
    for power, char in enumerate(num[::-1]):
        score += 5**power * convert[char]
    return score


def main():  # solves by converting to decimal, summing then converting back to snafu
    current_score = 0
    text = read_file("Day_25/input.txt").splitlines()
    for num in text:
        current_score += decimal(num)
    return snafu(current_score)


def main2():  # solves by summing in snafu
    text = read_file("Day_25/input.txt").splitlines()
    current = []
    for line in text:
        current = add(current, list(line))
    return "".join(current)


if __name__ == "__main__":
    start = perf_counter()
    print(main2())
    print(f"Time taken: {(perf_counter() - start) *1000} miliseconds")
    start = perf_counter()
    print(main())
    print(f"Time taken: {(perf_counter() - start) *1000} miliseconds")