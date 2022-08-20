import asyncio

from rich.progress import track
from rich.console import Console
from rich.prompt import Prompt, Confirm

from telethon import events, types, functions
from telethon.sync import TelegramClient

from functions.function import Function

console = Console()


class ReportFunc(Function):
    """Report a channel"""

    def __init__(self, storage, settings):
        super().__init__(storage, settings)

        self.reasons = (
            ("Child abuse", types.InputReportReasonChildAbuse()),
            ("Copyright", types.InputReportReasonCopyright()),
            ("Fake channel/account", types.InputReportReasonFake()),
            ("Pornography", types.InputReportReasonPornography()),
            ("Spam", types.InputReportReasonSpam()),
            ("Violence", types.InputReportReasonViolence()),
            ("Other", types.InputReportReasonOther())
        )

    async def execute(self):
        self.ask_accounts_count()

        link = Prompt.ask("[bold red]link[/]")
        posts = Prompt.ask("[bold red]enter the post ids[/]")
        posts = [int(i) for i in posts.split(",")]

        print()

        for index, reasons in enumerate(self.reasons):
            reason, _ = reasons

            console.print(
                "[bold white][{}] {}[/]"
                .format(index + 1, reason)
            )

        print()

        choice = int(console.input("[bold white]>> [/]"))
        reason_type = self.reasons[choice - 1][1]

        comment = console.input("[bold red]comment> [/]")

        for index, session in track(
            enumerate(self.sessions),
            "[yellow]Reporting...[/]",
            total=len(self.sessions)
        ):
            async with self.storage.ainitialize_session(session):
                me = await session.get_me()
                try:
                    await session(
                        functions.messages.ReportRequest(
                            peer=link,
                            id=posts,
                            reason=reason_type,
                            message=comment
                        )
                    )
                except Exception as err:
                    console.print(
                        "[{name}] [bold red]error.[/] {error}"
                        .format(name=me.first_name, error=err)
                    )
