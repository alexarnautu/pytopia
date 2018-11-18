from typing import Dict, Optional

import requests
import hmac
import base64
import hashlib
import json
import time

from enum import Enum
from requests.compat import quote_plus
from requests.exceptions import RequestException


class TransactionType(Enum):
    DEPOSIT = 'Deposit'
    WITHDRAW = 'Withdraw'


class TradeType(Enum):
    BUY = 'Buy'
    SELL = 'Sell'


class CancelType(Enum):
    ALL = 'All'
    TRADE = 'Trade'
    TRADEPAIR = 'TradePair'


class Pytopia:
    _base_url: str = "https://www.cryptopia.co.nz/api/"
    _public_url: str = "https://www.cryptopia.co.nz/api/public/"

    def __init__(self, public_key: str, private_key: str):
        self._public_key = public_key
        self._private_key = private_key

    def _headers(self, url: str, data: Dict) -> Dict:
        md5 = hashlib.md5()
        nonce = str(time.time())

        md5.update(data.encode('utf-8'))
        rcb64 = base64.b64encode(md5.digest()).decode('utf-8')
        request_signature = f'{self._public_key}POST{quote_plus(url).lower()}{nonce}{rcb64}'

        hmac_signature = base64.b64encode(hmac.new(base64.b64decode(self._private_key),
                                                   request_signature.encode('utf-8'),
                                                   hashlib.sha256).digest()).decode('utf-8')
        return {
            'Authorization': f'amx {self._public_key}:{hmac_signature}:{nonce}',
            'Content-Type': 'application/json; charset=utf-8'
        }

    def _post(self, url: str, payload: Dict):
        payload = json.dumps(payload)
        response_data = requests.post(url, headers=self._headers(url, payload), data=payload).json()

        if response_data.get('Success') and response_data.get('Success') is True:
            return response_data.get('Data')

        raise RequestException(response_data.get('Error'))

    def _get(self, url: str, query_params: Optional[Dict] = None):
        if query_params:
            for _, v in query_params.items():
                url += f'/{v}'

        response_data = requests.get(url).json()

        if not response_data:
            return None

        return response_data['Data']

    def get_balances(self, currency: str = None):
        return self._post(f"{self._base_url}GetBalance", {'Currency': currency if currency else ''})

    def get_deposit_address(self, currency: str):
        return self._post(f"{self._base_url}GetDepositAddress", {'Currency': currency})

    def get_open_orders(self, market: str, limit: Optional[int] = 100):
        return self._post(f"{self._base_url}GetOpenOrders", {'TradePairId': market, 'Count': limit})

    def get_trade_history(self, market: str, limit: Optional[int] = 100):
        return self._post(f"{self._base_url}TradeHistory", {'Market': market, 'Count': limit})

    def get_transactions(self, transaction_type: TransactionType, limit: Optional[int] = 100):
        return self._post(f"{self._base_url}GetTransactions", {'Type': transaction_type.value, 'limit': limit})

    def submit_trade(self, market, trade_type: TradeType, rate: float, amount: float):
        return self._post(f"{self._base_url}SubmitTrade", {'Market': market, 'Type': trade_type.value, 'Rate': rate,
                                                           'Amount': amount})

    def cancel_trade(self, cancel_type: CancelType, order_id: Optional[int] = None,
                     trade_pair_id: Optional[int] = None):
        return self._post(f"{self._base_url}CancelTrade", {'Type': cancel_type.value,
                                                           'OrderId': order_id if order_id else '',
                                                           'TradePairId': trade_pair_id if trade_pair_id else ''})

    def submit_tip(self, currency: str, active_users: int, amount: float):
        return self._post(f"{self._base_url}SubmitTip", {'Currency': currency, 'ActiveUsers': active_users,
                                                         'Amount': amount})

    def submit_withdraw(self, currency: str, address: str, amount: float):
        return self._post(f"{self._base_url}SubmitWithdraw", {'Currency': currency, 'Address': address,
                                                              'amount': amount})

    def get_currencies(self):
        return self._get(f"{self._base_url}GetCurrencies")

    def get_trade_pairs(self):
        return self._get(f"{self._base_url}GetTradePairs")

    def get_markets(self, base_market: Optional[str] = 'All', hours: Optional[int] = 24):
        return self._get(f"{self._base_url}GetMarkets", {'baseMarket': base_market, 'hours': hours})

    def get_market(self, market: str, hours: Optional[int] = 24):
        return self._get(f"{self._base_url}GetMarket", {'market': market, 'hours': hours})

    def get_market_history(self, market: str, hours: Optional[int] = 24):
        return self._get(f"{self._base_url}GetMarketHistory", {'market': market, 'hours': hours})

    def get_market_orders(self, market: str, order_count: Optional[int] = 100):
        return self._get(f"{self._base_url}GetMarketOrders", {'market': market, 'orderCount': order_count})

    def get_market_order_groups(self, markets: Optional[str] = 'All', order_count: Optional[int] = 100):
        return self._get(f"{self._base_url}GetMarketOrderGroups", {'markets': markets, 'orderCount': order_count})
