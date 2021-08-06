# -- coding: utf-8 --
# By: Snu

import discord
from discord.ext import commands
from colorama import Style, Fore
from requests import get
from os import system
from platform import system as os

token = "" # token aqui
client = commands.Bot("h!", self_bot=True, case_insensitive=True, help_command=None)
clear_terminal = lambda: system("cls" if os() == "Windows" else "clear")

banner = f"""{Fore.RED} ______   _    __ & _____    _________  
| |  \\ \\ | |  / /  | | \\ \\  | | | | | \\ 
| |  | | | |-< <   | |  | | | | | | | | 
|_|  |_| |_|  \\_\\  |_|_/_/  |_| |_| |_| 
                                        {Fore.BLUE}By: Snu{Style.RESET_ALL}\n"""
@client.event
async def on_ready():
	print(f"{Fore.GREEN}online na conta -> {client.user}{Style.RESET_ALL}")


@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.message.delete()
		print(f"{Fore.RED}Você digitou um comando inválido.{Style.RESET_ALL}")

	# Debug
	"""
	else:
		print(error)
	"""


@client.command()
@commands.has_permissions(manage_channels=True)
async def nuke(ctx):
	new_channel = await ctx.channel.clone(reason="Novo canal")
	await ctx.channel.delete(reason="Nukando canal")
	await new_channel.edit(position=ctx.channel.position, sync_permissions=True)
	await new_channel.send("O canal foi limpado", delete_after=5)
	print(f"{Fore.GREEN}O canal {ctx.channel.name} foi nukado com sucesso.{Style.RESET_ALL}")


@nuke.error
async def nuke_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		print(f"{Fore.RED}Você não tem permissão para executar o comando h!nuke no canal {ctx.channel.name}{Style.RESET_ALL}")


@client.command()
async def clear(ctx, mount:int=None):
	msg = 0
	async for message in ctx.channel.history(limit=mount):
		if message.author.id == client.user.id:
			try:
				await message.delete()

			except:
				print(f"{Fore.RED}Erro ao deletar uma mensagem{Style.RESET_ALL}")

			else:
				msg += 1

	print(f"{Fore.GREEN}{msg} mensagens foram deletadas com sucesso{Style.RESET_ALL}")


@client.command()
async def help(ctx):
	await ctx.message.delete()
	embed = discord.Embed(
		title="Nk&Dm",
		description="**Comandos:**",
		color=16722512
	)
	embed.add_field(name="h!nuke", value="Apaga o canal e cria um novo exatamente igual", inline=False)
	embed.add_field(name="h!clear {quantidade}", value="Apaga a quantidade de mensagens escolhidas\nObs: deixe vazio para apagar todas as mensagens")
	embed.set_thumbnail(url=client.user.avatar_url)
	embed.set_footer(text="By: Snu")
	await ctx.send(embed=embed)

if __name__ == "__main__":
	url = "https://discordapp.com/api/v9/users/@me/guilds"
	headers = {"Authorization" : token}
	clear_terminal()
	print(banner)

	if get(url, headers=headers).status_code != 200:
		print(f"{Fore.RED}Token inválida.{Style.RESET_ALL}")
		exit(1)

	client.run(token, bot=False)
