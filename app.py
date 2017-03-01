# By James Goldstein 2017
# jamesdylangoldstein AT gmail DOT com
# Challenge: Build a terminal app that takes an integer
# Convert the integer to binary
# Then find the number of maximum repeating '1's in binary
# Can not use build in modules/functions for converting to binary
# Can not use anyone else's code

import sys
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

num_half_bytes = 1
num_base = 0
sum_factorial = 0
binary_number = ''
n = 0

def reset():
    num_half_bytes = 1
    num_base = 0
    sum_factorial = 0
    binary_number = ''
    n = 0

def find_num_half_bytes(number):
    global num_base
    global num_half_bytes
    global sum_factorial

    if number > ((15 * (16 ** num_base)) + sum_factorial):
        sum_factorial += (15 * (16 ** num_base))
        num_base += 1
        num_half_bytes += 1
        find_num_half_bytes(number)

def biggest_multiple(number):
    global num_half_bytes

    for x in range(0, 17):
        if number <= 0:
            return 0
        elif (x * (16 ** (num_half_bytes - 1))) > number:
            subtract = ((x - 1) * (16 ** (num_half_bytes - 1)))
            num_half_bytes -= 1
            convert_to_binary(x - 1)
            biggest_multiple(number - subtract)

def convert_to_binary(multiple):
    global binary_number

    multiple_string = str(multiple)
    half_byte_binary = ''

    binary_list = ['0','0','0','0']

    while multiple > 0:
        for y in range(0, 5):
            if multiple == 0:
                break
            elif 2 ** y > multiple:
                if y == 0:
                    binary_list.pop(3)
                    binary_list.insert(3, '1')
                else:
                    binary_list.pop(-(y - 1))
                    binary_list.insert(-(y - 1), '1')
                multiple -= (2 ** (y - 1))
                break
            elif 2 ** y == multiple:
                if y == 0:
                    binary_list.pop(3)
                    binary_list.insert(3, '1')
                else:
                    binary_list.pop(-y)
                    binary_list.insert(-y, '1')
                multiple -= (2 ** (y))
                break

    binary_number += half_byte_binary.join(binary_list)

def run_it_all(n):
    global binary_number
    find_num_half_bytes(n)
    biggest_multiple(n)
    local_binary = binary_number
    reset()
    return local_binary

#@app.route('/converted', methods=['GET', 'POST'])
#def converted(local_binary):
#    return render_template('converted.html', local_binary=local_binary)

@app.route('/', methods=['GET', 'POST'])
def index(local_binary):
    global n
    global binary_number

    if request.method == 'POST':
        n = int(request.form['number'].strip())
        local_binary = run_it_all(n)
        return render_template('index.html', local_binary=local_binary)
    return render_template('index.html', local_binary=local_binary)

if __name__ == '__main__':
    app.run(debug=True)
