"""Real products from the Out of Town Yinzers Printful store
(https://outoftownyinzers.printful.me/). Manually maintained -- update this
list whenever a product is added/removed/repriced in Printful. No live API
sync since it's a small, infrequently-changing catalog.

Checkout happens on Printful's side (buy_url) -- Printful blocks being
iframed (X-Frame-Options: SAMEORIGIN), and third-party checkout flows don't
play well inside frames anyway, so products are shown natively here and
link out for the actual purchase.
"""

PRODUCTS = [
    {
        "name": "Out of Town Yinzers Short Sleeve T-shirt",
        "price": "$22.00",
        "image": "img/products/tshirt.png",
        "buy_url": "https://outoftownyinzers.printful.me/product/short-sleeve-t-shirt",
    },
    {
        "name": "Out of Town Yinzers Toddler Short Sleeve Tee",
        "price": "$17.00",
        "image": "img/products/toddler-tee.png",
        "buy_url": "https://outoftownyinzers.printful.me/product/out-of-town-yinzers-toddler-short-sleeve-tee",
    },
    {
        "name": "Out of Town Yinzers Premium Sweatshirt",
        "price": "$30.00",
        "image": "img/products/sweatshirt.png",
        "buy_url": "https://outoftownyinzers.printful.me/product/out-of-town-yinzers-premium-sweatshirt",
    },
    {
        "name": "Out of Town Yinzers Trucker Hat",
        "price": "$25.00",
        "image": "img/products/trucker-hat.png",
        "buy_url": "https://outoftownyinzers.printful.me/product/out-of-town-yinzers-trucker-hat",
    },
]

STORE_URL = "https://outoftownyinzers.printful.me/"
