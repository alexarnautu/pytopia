# :rocket: Pytopia 
Pytopia is a library that allows you to interact with Cryptopia API.

## :memo: Requirements
- Python (3.6, 3.7)

## :floppy_disk: Installation

To install this package, you need to make sure **pip** is installed:
```bash
pip install pytopia
```

## :mortar_board: Example

Let's take a look over a simple example on how to use it:

```python
from pytopia import Pytopia

pytopia = Pytopia(PUBLIC_KEY, PRIVATE_KEY)

# Get the last traded price for every trade pair
trade_pairs =  pytopia.get_trade_pairs()

for trade_pair in trade_pairs:
    market_history = pytopia.get_market_history(trade_pairs[0]['Id'])
    last_traded_price = market_history[0]['Price']
    print(last_traded_price)
    
```