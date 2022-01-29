import random

import hikari
import lightbulb
import pyjokes
import requests

from globals import get_logger

fun = lightbulb.Plugin(
    name='Fun',
    description='Fun commands to mess around with'
)

logger = get_logger()


@fun.command()
@lightbulb.command('joke', 'tells you a joke!')
@lightbulb.implements(lightbulb.SlashCommand)
async def jokes(ctx: lightbulb.Context) -> None:
    await ctx.respond(pyjokes.get_joke('en', 'neutral'))


@fun.command()
@lightbulb.command('yomomma', 'like the joke command, but for yomomma jokes')
@lightbulb.implements(lightbulb.SlashCommand)
async def yomomma(ctx: lightbulb.Context) -> None:
    endpoint = 'https://yomomma-api.herokuapp.com/jokes'
    joke = requests.get(endpoint).json()['joke']

    await ctx.respond(joke)


@fun.command()
@lightbulb.option('question', 'the question for the magic 8ball')
@lightbulb.command('8ball', 'let the magic 8 ball decide your fate')
@lightbulb.implements(lightbulb.SlashCommand)
async def eight_ball(ctx: lightbulb.Context) -> None:
    answers = [
        'it is decidedly so',
        'without a doubt',
        'it is certain',
        'yes',
        'no',
        'signs point to no',
        'very doubtful',
        'reply hazy, try again',
        'unsure'
    ]

    embed = hikari.Embed(
        title='The Magic 8 Ball Says..'
    )

    embed.add_field('Question', ctx.options.question)
    embed.add_field('Answer', random.choice(answers))

    await ctx.respond(embed)


load = lambda client: client.add_plugin(fun)
unload = lambda client: client.remove_plugin(fun)
