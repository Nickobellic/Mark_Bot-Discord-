from discord.ext import commands
import os
import discord
from bot import get_cae_marks
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True


client = commands.Bot(intents=intents, command_prefix="|")

token = os.getenv("TOKEN")


@client.command()
async def hello(ctx):
    await ctx.send("Hello!")

@client.command()
async def mark(ctx, *, arg):
    msg = await ctx.send("Fetching the data...")
    register_no = os.environ["REGNO"]
    password = os.environ["PASS"]
    print(arg, password)
    print("Obtaining Results")
    result = get_cae_marks(register_no, password)[arg]
    CAE_1 = result["CAE-1"]
    CAE_2 = result["CAE-2"]

    subjects_CAE_1 = "\n".join(str(subject) for subject in list(CAE_1.keys()))
    marks_CAE_1 = "\n".join(str(marks) for marks in list(CAE_1.values()))

    subjects_CAE_2 = "\n".join(str(subject) for subject in list(CAE_2.keys()))
    marks_CAE_2 = "\n".join(str(marks) for marks in list(CAE_2.values()))

    await msg.delete()
    embed = discord.Embed(
        title=arg+" CAE-1 Marks",
        color=discord.Color.green()
    )
    embed.add_field(name="Subject", value=subjects_CAE_1, inline=True)
    embed.add_field(name="Marks", value=marks_CAE_1, inline=True)
    await ctx.send(embed=embed)
    embed = discord.Embed(
        title=arg+" CAE-2 Marks",
        color=discord.Color.green()
    )
    embed.add_field(name="Subject", value=subjects_CAE_2, inline=True)
    embed.add_field(name="Marks", value=marks_CAE_2, inline=True)
    await ctx.send(embed=embed)

@client.event
async def on_ready():
    print(f"Logged In as a bot {client.user}")

keep_alive()
client.run(os.environ['TOKEN'])