from flask import Flask, request, jsonify
import traceback
import os
from flask import send_from_directory

app = Flask(__name__)

# use a memoization dict to store the value of the nth special math calculation
cache = {}

def helper(n):
    if n in cache:
        return cache[n]

    if n == 0:
        val = 0
    elif n == 1:
        val = 1
    else:
        val = n + helper(n - 1) + helper(n - 2)

    cache[n] = val
    return val


@app.route('/specialmath/<n>')
def specialmath(n):
    try:
        if type(int(n)) != int or int(n) < 0:
            raise ValueError("Please provide a positive number in integer format")
        n = int(n)

        val = helper(n)

        return jsonify(value=val)
    except ValueError as e:
        print(f"{str(e)}")
        return jsonify(msg=str(e))
    except Exception as e:
        print(traceback.print_exc())
        print(f"Error while getting specialmath: {str(e)}")
        return jsonify(msg="Failed to do special math")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def home():
    return jsonify(msg="endpoint should be in example format: https://172.20.0.2/5000/specialmath/7")


if __name__ == '__main__':
    app.run(host="0.0.0.0")

