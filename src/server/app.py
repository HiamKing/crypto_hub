from flask import Flask
from flask_cors import CORS

from .coin_market_cap.views import cmc_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(cmc_bp, url_prefix='/coin-market-cap')
