import discord
import asyncio
import os
import random

from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context
from dotenv import load_dotenv

# Загрузка .env файла
load_dotenv()

# Получение токена из переменной окружения
TOKEN = os.environ.get('DISCORD_TOKEN')

# Настройка интентов
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Инициализация бота
bot = Bot(command_prefix="/", intents=intents, help_command=None)

# Событие: когда бот готов
@bot.event
async def on_ready() -> None:
    print("----------------------------------")
    print(f"Bot [{bot.user.name}] is now online!")
    print("----------------------------------")
    status_task.start()
    await bot.tree.sync()  # Синхронизация / команд


# Обновление статуса
@tasks.loop(minutes=1.0)
async def status_task() -> None:
    statuses = ["/play 🎶"]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))


# Обработка входящих сообщений
@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author == bot.user or message.author.bot:
        return
    await bot.process_commands(message)


# Обработка ошибок
@bot.event
async def on_command_error(context: Context, error) -> None:
    embed = discord.Embed(
        title="Error!",
        description=f"An error occurred while executing the command\n`{error}`",
        color=discord.Color.red()
    )
    return await context.send(embed=embed)


# Загрузка всех команд из папки cogs/
async def load_cogs() -> None:
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"cogs.{extension}")
                print(f"✅ Loaded cog '{extension}'")
            except Exception as e:
                print(f"❌ Failed to load cog '{extension}': {type(e).__name__}: {e}")


# Главная точка входа
async def main():
    await load_cogs()
    await bot.start(TOKEN)

# Запуск
asyncio.run(main())
