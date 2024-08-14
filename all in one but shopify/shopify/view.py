import os
import discord
import requests
from dotenv import load_dotenv

load_dotenv()
SHOPIFY_PASSWORD = os.getenv('SHOPIFY_PASSWORD')
SHOPIFY_SHOP_NAME = os.getenv('SHOPIFY_SHOP_NAME')
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

def get_open_orders():
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': SHOPIFY_PASSWORD
    }
    SHOPIFY_API_URL = f'https://{SHOPIFY_SHOP_NAME}.myshopify.com/admin/api/2022-01/orders.json?status=open'
    try:
        response = requests.get(SHOPIFY_API_URL, headers=headers)
        response.raise_for_status()
        orders = response.json()['orders']
        return orders
    except requests.exceptions.RequestException as err:
        print(f'Error retrieving orders from Shopify: {err}')
        return []

def setup_view(bot):
    @bot.command(name='view')
    async def view(ctx):
        orders = get_open_orders()
        channel = bot.get_channel(DISCORD_CHANNEL_ID)
        if not orders:
            await ctx.send("No open orders found.")
        else:
            for order in orders:
                embed = discord.Embed(
                    title=f"Order #{order['order_number']}",
                    description=f"Customer: {order.get('customer', {}).get('first_name', 'N/A')} {order.get('customer', {}).get('last_name', 'N/A')}",
                    color=discord.Color.blue()
                )
                embed.add_field(name="Email", value=order.get('email', 'N/A'), inline=True)
                embed.add_field(name="Total Price", value=f"${order.get('total_price', 'N/A')}", inline=True)
                embed.add_field(name="Created at", value=order.get('created_at', 'N/A'), inline=True)
                embed.add_field(name="Order Number", value=order.get('order_number', 'N/A'), inline=True)
                embed.add_field(name="Customer Email", value=order.get('email', 'N/A'), inline=True)
                await channel.send(embed=embed)
