# -- coding: utf-8 --
# By: snu, and thanks to Buraca for the translation

import discord
from discord.ext import commands
from colorama import Style, Fore
import requests
from asyncio import sleep
from os import system
from platform import system as os


class ErrorToSendMessage(Exception):
	pass


class ErrorToDeleteMessage(Exception):
	pass


class Raid(object):

	def __init__(self, token, headers):
		self.API = 'https://discord.com/api/v9'
		self.token = token
		self.headers = headers
		self.check_token()


	async def send_message(self, msg, id_channel, delete_after=None):
		payload = {"content": msg}
		if (r := requests.post(f"{self.API}/channels/{id_channel}/messages", headers=self.headers, json=payload)).status_code == 200:
			if delete_after != None:
				await sleep(delete_after)
				await self.delete_message(r.json()["id"], id_channel)

			return

		elif r.status_code == 429:
			time = r.json()['retry_after']
			print(f"{Fore.YELLOW}Rate Limit...{Style.RESET_ALL}")
			await sleep(time)
			self.send_message(msg, id_channel, delete_after)

		else:
			raise ErrorToSendMessage


	async def delete_message(self, msg_id, id_channel):
		url = f"{self.API}/channels/{id_channel}/messages/{msg_id}"
		if (r := requests.delete(url, headers=self.headers)).status_code == 204:
			return

		elif r.status_code == 429:
			time = r.json()['retry_after']
			print(f"{Fore.YELLOW}Rate Limit...{Style.RESET_ALL}")
			await sleep(time)
			await self.delete_message(msg_id, id_channel)

		else:
			raise ErrorToDeleteMessage

	def check_token(self):
		url = "https://discordapp.com/api/v9/users/@me/guilds"
		if requests.get(url, headers=self.headers).status_code != 200:
			print(f"{Fore.RED}Token inválida.{Style.RESET_ALL}")
			exit(1)


token = ""  # token aqui
API = 'https://discord.com/api/v9'
DEBUG = False
PREFIX = "nk!"
URL = "https://discordapp.com/api/v9/users/@me/guilds"
HEADERS = {"Authorization": token}

BANNER = f"""{Fore.RED}
 ______   _    __ & _____    _________  
| |  \\ \\ | |  / /  | | \\ \\  | | | | | \\ 
| |  | | | |-< <   | |  | | | | | | | | 
|_|  |_| |_|  \\_\\  |_|_/_/  |_| |_| |_| 
                                        {Fore.BLUE}by: snu{Style.RESET_ALL}\n"""


clear_terminal = lambda: system("cls" if os() == "Windows" else "clear"); clear_terminal()
setTitleWindow = lambda title: print(f'\33]0;{title}\a', end='', flush=True)
client = commands.Bot(PREFIX, self_bot=True, case_insensitive=True, help_command=None)
raid = Raid(token, HEADERS)


@client.event
async def on_ready():
	setTitleWindow(f"Nk&Dm | Online na conta -> {client.user}")
	print(f"{Fore.GREEN}Online na conta -> {client.user}{Style.RESET_ALL}")
	print(f"Meu prefixo é {PREFIX}, use o comando help para ver todos os comandos")

	
@client.listen()
async def on_command(ctx):
	if DEBUG == True:
		print(f"{Fore.YELLOW}DEBUG: {Fore.WHITE}Comando {PREFIX}{ctx.command.name} foi usado")


@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.message.delete()
		print(f"{Fore.RED}Você digitou um comando errado.{Style.RESET_ALL}")

	elif isinstance(error, commands.MissingPermissions):
		print(f"{Fore.RED}Você não tem permissão para executar o comando “{PREFIX}{ctx.command}” no canal -> {ctx.channel.id}{Style.RESET_ALL}")

	if DEBUG == True:
		print(f"{Fore.YELLOW}DEBUG: {Fore.WHITE}{error}")


@client.command()
@commands.has_permissions(manage_channels=True)
async def nuke(ctx):
	await ctx.channel.delete(reason="O canal foi limpado")
	new_channel = await ctx.channel.clone(reason="Novo canal")
	await new_channel.edit(position=ctx.channel.position, sync_permissions=True)
	await raid.send_message("O canal foi limpado.", new_channel.id, delete_after=5)
	print(f"{Fore.GREEN}O canal {ctx.channel.name} foi nukado com sucesso.{Style.RESET_ALL}")


@nuke.error
async def nuke_error(ctx, error):
	await raid.delete_message(ctx.message.id, ctx.channel.id)


@client.command()
async def clear(ctx, mount: int=None):
	msg = 0
	await raid.delete_message(ctx.message.id, ctx.channel.id)
	channel = client.get_channel(ctx.channel.id)
	setTitleWindow(f"Nk&Dm | Online na conta -> {client.user}")
	async for message in channel.history(limit=None):
		if mount == None or mount > msg:
			if message.author.id == client.user.id:
				try:
					await raid.delete_message(message.id, message.channel.id)

				except ErrorToDeleteMessage:
					print(f"{Fore.RED}Erro ao tentar apagar a mensagem{Style.RESET_ALL}")

				else:
					msg += 1
					print(f"{Fore.YELLOW}DEBUG: {Fore.WHITE}mensagem deletada.") if DEBUG == True else None

		else:
			break

	print(f"{Fore.GREEN}{msg} mensagens deletadas com sucesso.{Style.RESET_ALL}")
	setTitleWindow(f"Nk&Dm | Online na conta -> {client.user}")


@client.command()
async def cls(ctx):
	clear_terminal()
	print(BANNER)
	print(f"{Fore.GREEN}Terminal limpado com sucesso.{Style.RESET_ALL}")
	await raid.delete_message(ctx.message.id, ctx.channel.id)


@client.command()
async def help(ctx):
	embed = discord.Embed(
		title="Nk&Dm",
		description="**Comandos:**",
		color=16722512
	)
	embed.add_field(name=f"{PREFIX}nuke", value="Deleta o canal atual e cria um exatamente igual", inline=False)
	embed.add_field(name=f"{PREFIX}clear [quantidade]", value="deleta a quantidade de mensagens selecionadas\nNota: para deletar todas as mensagens não coloque nada", inline=False)
	embed.add_field(name=f"{PREFIX}cls", value="Limpa o seu terminal")
	embed.set_thumbnail(url=client.user.avatar_url)
	embed.set_footer(text="By: Snu")
	await ctx.send(embed=embed)


if __name__ == "__main__":
	clear_terminal()
	print(BANNER)
	client.run(token, bot=False)
