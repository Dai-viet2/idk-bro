import discord
import requests
from discord.ui import Button, View
from datetime import datetime

ROBLOX_API_URL = "https://users.roblox.com/v1/usernames/users"

async def verify_roblox_username(ctx, order_number):
    await ctx.send("Please enter your Roblox username:")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    username_msg = await ctx.bot.wait_for('message', check=check)
    username = username_msg.content

    payload = {
        "usernames": [username],
        "excludeBannedUsers": True
    }

    response = requests.post(ROBLOX_API_URL, json=payload)
    data = response.json()

    if data['data']:
        user = data['data'][0]
        user_id = user['id']
        display_name = user['displayName']

        confirm_view = View()
        yes_button = Button(label="Yes", style=discord.ButtonStyle.green)
        no_button = Button(label="No", style=discord.ButtonStyle.red)

        async def yes_callback(interaction):
            verification_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await interaction.response.send_message("Great! Your Roblox account has been verified.")
            
            await ctx.send("Thank you for ordering from Ropix. Please wait for our delivery team. Their current status is: Sleeping. We will ping you when your order is ready!")

            embed = discord.Embed(title="Order Resume", description="This is an order resume with details", color=discord.Color.green())
            
            embed.set_thumbnail(url=ctx.author.avatar.url)
            
            embed.add_field(name="Customer", value=ctx.author.mention, inline=False)
            embed.add_field(name="Order Number", value=order_number, inline=False)
            embed.add_field(name="Roblox Profile", value=username, inline=False)
            embed.add_field(name="Delivery Team Status", value="Sleeping", inline=False)
            embed.add_field(name="Created at", value=verification_time, inline=False)
            
            try:
                await ctx.send("@everyone", embed=embed)
            except Exception as e:
                print(f"Error sending embed: {e}")
                fallback_msg = f"@everyone\nOrder Resume:\nCustomer: {ctx.author.mention}\nOrder Number: {order_number}\nRoblox Profile: {username}\nDelivery Team Status: Sleeping\nCreated at: {verification_time}"
                await ctx.send(fallback_msg)

        async def no_callback(interaction):
            await interaction.response.send_message("I'm sorry, let's try again.")
            await verify_roblox_username(ctx, order_number)

        yes_button.callback = yes_callback
        no_button.callback = no_callback

        confirm_view.add_item(yes_button)
        confirm_view.add_item(no_button)

        await ctx.send(f"Is this your Roblox account?\nUsername: {username}\nDisplay Name: {display_name}\nUser ID: {user_id}", view=confirm_view)
    else:
        await ctx.send("I couldn't find a Roblox account with that username. Please try again.")
        await verify_roblox_username(ctx, order_number)

def setup_roblox(bot):
    @bot.command(name='verify')
    async def verify(ctx, order_number: str):
        await verify_roblox_username(ctx, order_number)

__all__ = ['setup_roblox']
