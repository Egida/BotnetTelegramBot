from telethon.tl.functions.account import UpdateProfileRequest
from rich.console import Console

from functions.function import Function

console = Console()


class ChangeBioFunc(Function):
    """Change bio"""

    async def execute(self):
        bio = console.input("[bold red]bio> [/]")

        for session in self.sessions:
            async with self.storage.ainitialize_session(session):
                await session(
                    UpdateProfileRequest(about=bio)
                )
