from datetime import datetime

from flask import Flask, jsonify
from local_config import Config


app = Flask(__name__)
app.amount_limits = Config.AMOUNT_LIMITS_CONFIG

result = {
    'amounts': [],
    'write_date': None
}


@app.route('/request/<int:amount>', methods=['GET'])
def check_amount(amount):
    write_date = result.get('write_date')
    limits = app.amount_limits
    if write_date:
        time_difference = (datetime.now() - result.get('write_date')).total_seconds()
        for key in limits.keys():
            if key >= time_difference:
                time_limit = key
                break
    else:
        time_limit = min(app.amount_limits, key=app.amount_limits.get)
    amounts = result.get('amounts')
    if sum(amounts) < limits.get(time_limit) and amount < limits.get(time_limit):
        amounts.append(amount)
        result.update(amounts=amounts)
        if not write_date:
            result.update(write_date=datetime.now())
        return jsonify({'result': "OK"})
    else:
        return jsonify(
            {'error': f"Amount limit exceeded {limits.get(time_limit)}/{time_limit}"}
        )


if __name__ == '__main__':
    app.config.from_object(Config)
    app.run(debug=True)
