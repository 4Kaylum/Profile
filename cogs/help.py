from random import randint, choice

from discord import Embed
from discord.ext.commands import Context, Group, command

from cogs.utils.custom_bot import CustomBot
from cogs.utils.custom_cog import Cog


class Help(Cog):

    def __init__(self, bot:CustomBot):
        super().__init__(self.__class__.__name__)
        self.bot = bot 


    @command(name='help', aliases=['commands'], hidden=True)
    async def newhelp(self, ctx:Context, *, command_name:str=None):
        '''
        Gives you the new help command uwu
        '''

        # Get all the cogs
        if not command_name:
            cogs = self.bot.cogs.values()
            cog_commands = [cog.get_commands() for cog in cogs]
        else:
            command = self.bot
            for i in command_name.split():
                command = command.get_command(i)
                if not command:
                    await ctx.send(f"The command `{command_name}` could not be found.")
                    return
            base_command = command
            if isinstance(base_command, Group):
                cog_commands = [list(set(command.walk_commands()))]
            else:
                cog_commands = []

        # See which the user can run
        runnable_commands = []
        for cog in cog_commands:
            runnable_cog = []
            for command in cog:
                # try:
                #     runnable = await command.can_run(ctx) and command.hidden == False and command.enabled == True
                # except Exception:
                #     runnable = False 
                runnable = command.hidden == False and command.enabled == True
                if runnable:
                    runnable_cog.append(command) 
            runnable_cog.sort(key=lambda x: x.name.lower())
            if len(runnable_cog) > 0:
                runnable_commands.append(runnable_cog)

        # Sort cogs list based on name
        runnable_commands.sort(key=lambda x: x[0].cog_name.lower())

        # Make an embed
        help_embed = Embed()
        help_embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
        help_embed.colour = randint(1, 0xffffff)
        extra = [
            {'text': 'ProfileBot - Made by Caleb#2831'},
            {'text': f'ProfileBot - Add me to your own server! ({ctx.prefix}invite)'}
        ]
        if self.bot.config.get('dbl_token'):
            extra.append({'text': f'ProfileBot - Add a vote on Discord Bot List! ({ctx.prefix}vote)'})
        if self.bot.config.get('patreon'):
            extra.append({'text': f'ProfileBot - Support me on Patreon! ({ctx.prefix}patreon)'})
        if self.bot.config.get('guild'):
            extra.append({'text': f'ProfileBot - Join the official Discord server! ({ctx.prefix}server)'})
        footer = choice(extra)
        footer['text'] = footer['text'].replace(f"<@!{self.bot.user.id}> ", f"<@{self.bot.user.id}> ").replace(f"<@{self.bot.user.id}> ", self.bot.config['default_prefix'])
        help_embed.set_footer(**footer)

        # Add commands to it
        if command_name:
            # if isinstance(base_command, Group):
            help_embed.add_field(name=f"{ctx.prefix}{base_command.qualified_name}", value=f"{base_command.help}")
            # else:
            #     help_embed.description = f"{ctx.prefix}{base_command.signature}\n\n{base_command.help}"
        for cog_commands in runnable_commands:
            value = '\n'.join([f"{ctx.prefix}{command.qualified_name} - *{command.short_doc}*" for command in cog_commands])
            help_embed.add_field(
                name=cog_commands[0].cog_name,
                value=value
            )
        
        # Send it to the user
        try:
            await ctx.author.send(embed=help_embed)
            if ctx.guild:
                await ctx.send('Sent you a PM!')
        except Exception:
            await ctx.send("I couldn't send you a PM :c")


def setup(bot:CustomBot):
    bot.remove_command('help')
    x = Help(bot)
    bot.add_cog(x)
    
