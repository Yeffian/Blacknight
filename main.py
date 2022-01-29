import os
import lightbulb
import hikari

from globals import get_config_manager, get_logger

EXTENSIONS = [
    'extensions.dev',
    'extensions.misc',
    'extensions.fun'
]

config = get_config_manager()
logger = get_logger()


def load_extensions():
    for ext in EXTENSIONS:
        client.load_extensions(ext)


client = lightbulb.BotApp(
    token=config.get_config('token'),
    prefix=config.get_config('prefix') if config.get_config('usePrefix') else '',
    intents=hikari.Intents.ALL,
    default_enabled_guilds=794602434281996289,
    help_slash_command=True,
    owner_ids=config.get_config('ownerId'),
    logs="DEBUG"
)


@client.listen(hikari.StartedEvent)
async def on_start(event: hikari.StartedEvent) -> None:
    load_extensions()


@client.listen(hikari.MessageCreateEvent)
async def on_message_sent(event: hikari.MessageCreateEvent) -> None:
    if event.author.is_bot:
        return

    logger.info('%s >> %s', event.author, event.content)


@client.listen(lightbulb.CommandErrorEvent)
async def on_command_error(event: lightbulb.CommandErrorEvent) -> None:
    # Unwrap the exception to get the original cause
    exception = event.exception.__cause__ or event.exception

    if isinstance(event.exception, lightbulb.CommandInvocationError):
        await event.context.respond(f"Something went wrong during invocation of command `{event.context.command.name}`.")
        raise event.exception

    if isinstance(exception, lightbulb.NotOwner):
        await event.context.respond("This command can only be ran by the owner of the bot.")
    elif isinstance(exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(f"This command is on cooldown. Retry in `{exception.retry_after:.2f}` seconds.")
    elif isinstance(exception, lightbulb.MissingRequiredPermission):
        await event.context.respond(f"You have insufficient permissions to run this command.")
    elif isinstance(exception, lightbulb.BotMissingRequiredPermission):
        await event.context.respond(f"I have insufficient permissions to execute this command.")
    elif isinstance(exception, lightbulb.NotEnoughArguments):
        await event.context.respond(f"Insufficient arguments for this command.")


@client.listen(lightbulb.SlashCommandInvocationEvent)
async def on_slash_command_invoked(event: lightbulb.SlashCommandInvocationEvent) -> None:
    logger.info(f'{event.context.command.name} was ran by {event.context.author.username}')


if __name__ == '__main__':
    if os.name != "nt":
        import uvloop

        uvloop.run()

    client.run()
