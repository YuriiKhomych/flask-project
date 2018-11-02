from datetime import datetime

from flask import Flask, jsonify
from local_config import Config


app = Flask(__name__)

result = {
    'amounts': [],
    'write_date': None
}


@app.route('/request/<int:amount>', methods=['GET'])
def check_amount(amount):
    write_date = result.get('write_date')
    limits = Config.AMOUNT_LIMITS_CONFIG
    if write_date:
        time_difference = \
            (datetime.now() - write_date).total_seconds()
        for key in limits.keys():
            if key >= time_difference:
                time_limit = key
                break
        else:
            time_limit = max(limits, key=limits.get)
    else:
        time_limit = min(limits, key=limits.get)
    amounts = result.get('amounts')
    if sum(amounts) < limits.get(time_limit) \
            and amount < limits.get(time_limit):
        amounts.append(amount)
        result.update(amounts=amounts, write_date=datetime.now())
        return jsonify({'result': "OK"})
    else:
        return jsonify({
            'error': f"Amount limit exceeded "
                     f"{limits.get(time_limit)}/{time_limit}"
        })


if __name__ == '__main__':
    app.config.from_object(Config)
    app.run(debug=True)
