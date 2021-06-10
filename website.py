from quart import Quart, render_template, redirect, url_for
from quart_discord import DiscordOAuth2Session
from discord.ext import ipc
import os

ipc_client = ipc.Client(secret_key = "ipcSecret123")
template_folder_path = os.path.abspath('Website/src')
static_folder_path = os.path.abspath('Website/static')

app = Quart(__name__, 
    template_folder = template_folder_path, 
    static_folder = static_folder_path
)

app.config["SECRET_KEY"] = "test123"
app.config["DISCORD_CLIENT_ID"] = 737101723340111962   
app.config["DISCORD_CLIENT_SECRET"] = "p78Jop3I9NXngkN06PKT2ZcWD0x5OL1e"
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"   

discord_session = DiscordOAuth2Session(app)

@app.route("/")
async def home():
    return await render_template("index.html", authorized = await discord_session.authorized)

@app.route("/login")
async def login():
    return await discord_session.create_session()

@app.route("/callback")
async def callback():
    try:
        await discord_session.callback()
    except Exception:
        pass

    return redirect(url_for("dashboard"))

@app.route("/dashboard")
async def dashboard():
    if not await discord_session.authorized:
        return redirect(url_for("login")) 

    guilds = [guild for guild in await discord_session.fetch_guilds() if guild.permissions.administrator]
    
    return await render_template("dashboard.html", guilds = guilds)

@app.route("/dashboard/<int:guild_id>")
async def dashboard_server(guild_id):
    if not await discord_session.authorized:
        return redirect(url_for("login")) 
    
    guild = await ipc_client.request("get_guild", guild_id = guild_id)

    if guild is None:
        return redirect(f'https://discord.com/oauth2/authorize?&client_id={app.config["DISCORD_CLIENT_ID"]}&scope=bot&permissions=8&guild_id={guild_id}&response_type=code&redirect_uri={app.config["DISCORD_REDIRECT_URI"]}')

    return await render_template(
        "guild_id.html", guild=guild
    )


if __name__ == "__main__":
    app.run(debug=True)
