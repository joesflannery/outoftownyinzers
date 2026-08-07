"""Real products from the Out of Town Yinzers Printful store
(https://outoftownyinzers.printful.me/). Manually maintained -- update this
list whenever a product is added/removed/repriced in Printful. No live API
sync since it's a small, infrequently-changing catalog.

Checkout happens on Printful's side (buy_url) -- Printful blocks being
iframed (X-Frame-Options: SAMEORIGIN), and third-party checkout flows don't
play well inside frames anyway, so products are shown natively here and
link out for the actual purchase.

Prices are "From" prices -- Printful prices some sizes/variants higher
(e.g. 2XL+), so the listed price is the cheapest variant, matching how the
storefront itself displays it.
"""

PRODUCTS = [
    {
        "name": "Out of Town Yinzers Bridge - Gray T-Shirt",
        "price": "From $20.00",
        "image": "img/products/bridge-gray-t-shirt.png",
        "buy_url": "https://outoftownyinzers.printful.me/product/out-of-town-yinzers-bridge-gray-t-shirt",
    },
    {
        "name": "Out of Town Yinzers Simple - Gray T-Shirt",
        "price": "From $20.27",
        "image": "img/products/simple-gray-t-shirt.png",
        "buy_url": "https://outoftownyinzers.printful.me/product/unisex-organic-mid-light-t-shirt",
    },
    {
        "name": "Pitt Out of Town Yinzers Gray",
        "price": "From $20.00",
        "image": "img/products/pitt-gray-t-shirt.png",
        "buy_url": "https://outoftownyinzers.printful.me/product/pitt-out-of-town-yinzers-gray",
    },
    {
        "name": "Pitt Out of Town Yinzers White T-Shirt",
        "price": "From $20.00",
        "image": "img/products/pitt-white-t-shirt.png",
        "buy_url": "https://outoftownyinzers.printful.me/product/pitt-out-of-town-yinzers-white-t-shirt",
    },
    {
        "name": "Out of Town Yinzers Simple White T-Shirt",
        "price": "From $19.77",
        "image": "img/products/simple-white-t-shirt.png",
        "buy_url": "https://outoftownyinzers.printful.me/product/out-of-town-yinzers-simple-white-t-shirt",
    },
    {
        "name": "Out of Town Yinzers Bridge White T-Shirt",
        "price": "From $19.00",
        "image": "img/products/bridge-white-t-shirt.png",
        "buy_url": "https://outoftownyinzers.printful.me/product/out-of-town-yinzers-bridge-white-t-shirt",
    },
    {
        "name": "Out of Town Yinzers Bridge Short Sleeve T-shirt",
        "price": "From $23.00",
        "image": "img/products/bridge-short-sleeve-t-shirt.png",
        "buy_url": "https://outoftownyinzers.printful.me/product/out-of-town-yinzers-bridge-short-sleeve-t-shirt",
    },
    {
        "name": "Out of Town Yinzers Short Sleeve T-shirt",
        "price": "From $22.00",
        "image": "img/products/short-sleeve-t-shirt.png",
        "buy_url": "https://outoftownyinzers.printful.me/product/short-sleeve-t-shirt",
    },
    {
        "name": "Out of Town Yinzers Toddler Short Sleeve Tee",
        "price": "From $17.00",
        "image": "img/products/toddler-tee.png",
        "buy_url": "https://outoftownyinzers.printful.me/product/out-of-town-yinzers-toddler-short-sleeve-tee",
    },
    {
        "name": "Out of Town Yinzers Premium Sweatshirt",
        "price": "From $30.00",
        "image": "img/products/sweatshirt.png",
        "buy_url": "https://outoftownyinzers.printful.me/product/out-of-town-yinzers-premium-sweatshirt",
    },
    {
        "name": "Out of Town Yinzers Trucker Hat",
        "price": "From $25.00",
        "image": "img/products/trucker-hat.png",
        "buy_url": "https://outoftownyinzers.printful.me/product/out-of-town-yinzers-trucker-hat",
    },
]

STORE_URL = "https://outoftownyinzers.printful.me/"
