intents = discord.Intents()
intents.all()

bot = commands.Bot(command_prefix=".", intents=intents)

client = discord.Client()