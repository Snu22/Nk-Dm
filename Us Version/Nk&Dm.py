# -- coding: utf-8 --
# By: snu, and thanks to Buraca for the translation

import discord
from discord.ext import commands
from colorama import Style, Fore
from requests import get
from os import system
from platform import system as os

token = ""  # token aqui
client = commands.Bot("h!", self_bot=True, case_insensitive=True, help_command=None)

lambda: return system("cls" if os() == "Windows" else "clear")
lambda title: return print(f'\33]0;{title}\a', end='', flush=True)


URL = "https://discordapp.com/api/v9/users/@me/guilds"
HEADERS = {"Authorization": token}
BANNER = f"""{Fore.RED}
 ______   _    __ & _____    _________  
| |  \\ \\ | |  / /  | | \\ \\  | | | | | \\ 
| |  | | | |-< <   | |  | | | | | | | | 
|_|  |_| |_|  \\_\\  |_|_/_/  |_| |_| |_| 
										{Fore.BLUE}By: Snu{Style.RESET_ALL}\n"""


@client.event
async def on_ready():
	setTitleWindow(f"Nk&Dm | online in the account -> {client.user}")
	print(f"{Fore.GREEN}online in the account -> {client.user}{Style.RESET_ALL}")


@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.message.delete()
		print(f"{Fore.RED}You typed the wrong command.{Style.RESET_ALL}")

	# Debug
	"""
	else:
		print(error)
	"""


@client.command()
@commands.has_permissions(manage_channels=True)
async def nuke(ctx):
	new_channel = await ctx.channel.clone(reason="New Channel")
	await ctx.channel.delete(reason="The channel was cleared")
	await new_channel.edit(position=ctx.channel.position, sync_permissions=True)
	await new_channel.send("The channel was cleared", delete_after=5)
	print(f"{Fore.GREEN}The channel {ctx.channel.name} was successfully nuked.{Style.RESET_ALL}")


@nuke.error
async def nuke_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		print(f"{Fore.RED}You don’t have permission to execute the command “h!nuke” in this channel -> {ctx.channel.name}{Style.RESET_ALL}")


@client.command()
async def clear(ctx, mount: int=None):
	msg = 0
	setTitleWindow(f"Nk&Dm | online in the account -> {client.user} | Executing the command clear in the channel -> {ctx.channel.name}")
	async for message in ctx.channel.history(limit=mount):
		if message.author.id == client.user.id:
			try:
				await message.delete()

			except:
				print(f"{Fore.RED}Failed to delete a message.{Style.RESET_ALL}")

			else:
				msg += 1

	print(f"{Fore.GREEN}{msg} messages were successfully deleted.{Style.RESET_ALL}")


@client.command()
async def cls(ctx):
	await ctx.message.delete()
	clear_terminal()
	print(BANNER)
	print(f"{Fore.GREEN}Terminal successfully cleared.{Style.RESET_ALL}")


@client.command()
async def help(ctx):
	await ctx.message.delete()
	embed = discord.Embed(
		title="Nk&Dm",
		description="**Commands:**",
		color=16722512
	)
	embed.add_field(name="h!nuke", value="Deletes and creates the exact same channel", inline=False)
	embed.add_field(name="h!clear {quantidade}", value="Deletes the the chosen amount of messages\nNote: Leave it empty to delete all the messages", inline=False)
	embed.add_field(name="h!cls", value="Clear your terminal")
	embed.set_thumbnail(url=client.user.avatar_url)
	embed.set_footer(text="By: Snu")
	await ctx.send(embed=embed)


if __name__ == "__main__":
	clear_terminal()
	print(BANNER)

	if get(URL, headers=HEADERS).status_code != 200:
		print(f"{Fore.RED}Invalid Token.{Style.RESET_ALL}")
		exit(1)

	client.run(token, bot=False)
