from flask import Flask

from .coin_market_cap.views import cmc_bp

app = Flask(__name__)

app.register_blueprint(cmc_bp, url_prefix='/coin-market-cap')
