import os
import random
import asyncio
from rich.prompt import Prompt, Confirm
from rich.console import Console

from functions.function import Function

console = Console()


class CommentsFloodFunc(Function):
    """Flood to channel comments"""

    async def flood(self, session, channel, post_id, media):
        await session.connect()
        me = await session.get_me()
        count = 0
        errors = 0

        while count < self.settings.messages_count \
                or self.settings.messages_count == 0:
            text = random.choice(self.settings.messages)

            try:
                if not media:
                    await session.send_message(
                        channel,
                        text,
                        comment_to=post_id,
                        parse_mode="html"
                    )
                else:
                    file = random.choice(os.listdir("media"))

                    await session.send_file(
                        channel,
                        os.path.join("media", file),
                        comment_to=post_id,
                        caption=text,
                        parse_mode="html"
                    )
            except Exception as err:
                console.print(
                    "[{name}] [bold red]not sent.[/] {err}"
                    .format(name=me.first_name, err=err)
                )

                errors += 1

                if errors >= 5:
                    break
            else:
                count += 1
                console.print(
                    "[{name}] [bold green]sent.[/] COUNT: [yellow]{count}[/]"
                    .format(name=me.first_name, count=count)
                )
            finally:
                await self.delay()

    async def execute(self):
        self.ask_accounts_count()

        link = console.input("[bold red]link to post> [/]")

        delay = Prompt.ask(
            "[bold red]delay[/]",
            default="-".join(str(x) for x in self.settings.delay)
        )

        media = Confirm.ask("[bold red]media[/]")
        from_config = Confirm.ask("[bold red]use messages from config?[/]")

        if not from_config:
            self.settings.messages = [console.input("[bold red]message: [/]")]

        self.settings.delay = self.parse_delay(delay)

        channel = "/" .join(link.split("/")[:-1])
        post_id = link.split("/")[-1]

        await asyncio.wait([
            self.flood(session, channel, int(post_id), media)
            for session in self.sessions
        ])
