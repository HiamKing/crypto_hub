from flask import Flask
from flask_cors import CORS

from .coin_market_cap.views import cmc_bp
from .binance.views import binance_bp
from .analytics.views import analytics_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(cmc_bp, url_prefix='/coin-market-cap')
app.register_blueprint(binance_bp, url_prefix='/binance')
app.register_blueprint(analytics_bp, url_prefix='/analytics')
