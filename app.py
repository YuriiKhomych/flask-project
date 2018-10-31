from flask import Flask
from local_config import Config


app = Flask(__name__)
app.amount_limits = Config.AMOUNT_LIMITS_CONFIG


if __name__ == '__main__':
    app.config.from_object(Config)
    app.run(debug=True)
