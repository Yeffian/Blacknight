import hikari
import lightbulb
from globals import get_logger, get_config_manager

dev = lightbulb.Plugin(
    name='Developer',
    description='Commands meant to be used for the development of the bot'
)

logger = get_logger()


@dev.command()
@lightbulb.command('ping', 'says pong')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    logger.info('ping command was executed in channel %s by %s', ctx.channel_id, ctx.author)
    await ctx.respond('pong')


@dev.command()
@lightbulb.command('info', 'gives information about the bot')
@lightbulb.implements(lightbulb.SlashCommand)
async def info(ctx: lightbulb.Context) -> None:
    config = get_config_manager()

    dependencies = sum(1 for line in open('./requirements.txt'))

    embed = hikari.Embed(
        title='Information about Blacknight',
    )

    embed.add_field('Owner Id', config.get_config('ownerId'))
    embed.add_field('Owner Username', config.get_config('ownerUsername'))
    embed.add_field('Using Prefix', config.get_config('usePrefix'))
    embed.add_field('Used Programming Language', 'Python')
    embed.add_field('Dependencies', str(dependencies))

    await ctx.respond(embed)


@dev.command()
@lightbulb.command('stop', 'disconnects client from discord')
@lightbulb.implements(lightbulb.SlashCommand)
async def stop(ctx: lightbulb.Context) -> None:
    if ctx.author.id == ctx.bot.owner_ids:
        await ctx.respond('Stopping...')
        await ctx.bot.close()
    else:
        raise lightbulb.NotOwner()


load = lambda client: client.add_plugin(dev)
unload = lambda client: client.remove_plugin(dev)
