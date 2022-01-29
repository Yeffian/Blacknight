import lightbulb

from globals import get_logger
from libs.evaluator import evaluate

misc = lightbulb.Plugin(
    name='Misc',
    description='Miscellaneous that i dont know which category to put in'
)

logger = get_logger()


@misc.command()
@lightbulb.option('message', 'the message to echo', type=str)
@lightbulb.command('echo', 'makes the bot say back whatever is passed as an argument')
@lightbulb.implements(lightbulb.SlashCommand)
async def echo(ctx: lightbulb.Context) -> None:
    await ctx.respond(ctx.options.message.replace('@', ' '))


@misc.command()
@lightbulb.option('expr', 'the expression to evaluate', type=str)
@lightbulb.command('eval', 'evaluates a mathematical expression')
@lightbulb.implements(lightbulb.SlashCommand)
async def evaluate_expr(ctx: lightbulb.Context) -> None:
    result = evaluate(ctx.options.expr)
    await ctx.respond(result)


load = lambda client: client.add_plugin(misc)
unload = lambda client: client.remove_plugin(misc)