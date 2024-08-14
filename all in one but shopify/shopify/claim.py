import os
import discord
import requests
from dotenv import load_dotenv
from roblox import setup_roblox

load_dotenv()
SHOPIFY_PASSWORD = os.getenv('SHOPIFY_PASSWORD')
SHOPIFY_SHOP_NAME = os.getenv('SHOPIFY_SHOP_NAME')

def get_shopify_order(order_number):
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': SHOPIFY_PASSWORD
    }
    try:
        response = requests.get(
            f'https://{SHOPIFY_SHOP_NAME}.myshopify.com/admin/api/2024-07/orders.json',
            headers=headers,
            params={'status': 'any', 'name': order_number}
        )
        response.raise_for_status()
        orders = response.json()['orders']
        return orders[0] if orders else None
    except requests.exceptions.RequestException as err:
        print(f'Error retrieving order from Shopify: {err}')
        return None

def setup_claim(bot):
    setup_roblox(bot)

    @bot.command(name='claim')
    async def claim(ctx):
        await ctx.send('Please enter your order number:')

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        order_number_msg = await bot.wait_for('message', check=check)
        order_number = order_number_msg.content

        order = get_shopify_order(order_number)
        if order:
            await ctx.send(f'Order #{order_number} found. Claim successful!')
            verify_command = bot.get_command('verify')
            await ctx.invoke(verify_command, order_number=order_number)
        else:
            await ctx.send('No order found with this number. Please try again.')
