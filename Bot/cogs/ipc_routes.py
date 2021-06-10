from discord.ext import commands, ipc

class IpcRoutes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @ipc.server.route()
    async def get_all_guilds(self, data):
        return self.bot.guilds

    @ipc.server.route()
    async def get_all_channels(self, data):
        guild = self.bot.get_guild(data.guild_id)
        channels_dict = {}
        
        for channel in guild.text_channels:
            channels_dict[channel.name] = channel.id

        return channels_dict

    @ipc.server.route()
    async def get_guild(self, data):
        guild = self.bot.get_guild(data.guild_id)

        if guild is None: 
            return None
        
        try:
            return {
            "name": guild.name,
            "id": guild.id,
            "icon_url": str(guild.icon_url),
            "member_count": int(guild.member_count),
            "role_count": int(len(guild.roles)), 
            "region": str(guild.region), 
            "owner": str(guild.owner),
            "channel_count": int(len(guild.channels)),
            "category_count": int(len(guild.categories))
        }
        
        except:
            return None

def setup(bot):
    bot.add_cog(IpcRoutes(bot))