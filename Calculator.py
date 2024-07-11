from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

WINDOW_SIZE = 10
window = []

# fetch numbers from the test server
def fetch_numbers(number_id):
    if number_id == 'p':
        url = "http://29.244.56.144/test/primes"
    elif number_id == 'f':
        url = "http://20.244.56.144/test/fibo"
    elif number_id == 'e':
        url = "http://20.244.56.144/test/even"
    elif number_id == 'r':
        url = "http://20.244.56.144/test/rand"
    else:
        return []

    try:
        response = requests.get(url, timeout=0.5)
        if response.status_code == 200:
            numbers = response.json().get('numbers', [])
            return numbers
    except requests.RequestException:
        return []

# unique numbers and window size
def update_window(new_numbers):
    global window
    # Add only unique numbers
    new_numbers = [num for num in new_numbers if num not in window]
    # Update window
    window.extend(new_numbers)
    if len(window) > WINDOW_SIZE:
        window = window[-WINDOW_SIZE:]

# calculate average
def calculate_average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

@app.route('/numbers/<number_id>', methods=['GET'])
def get_numbers(number_id):
    new_numbers = fetch_numbers(number_id)
    # previous state
    window_prev_state = window.copy()
    # Update window
    update_window(new_numbers)
    # Calculate average
    avg = calculate_average(window)
    return jsonify({
        "numbers": new_numbers,
        "windowPrevState": window_prev_state,
        "windowCurrState": window,
        "avg": round(avg, 2)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9876, debug=True)
