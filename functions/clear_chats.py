import asyncio
from telethon import functions, types, TelegramClient
from rich.console import Console
from rich.prompt import Confirm

from functions.function import Function

console = Console()


class ClearDialogsFunc(Function):
    """Clear all dialogs"""

    async def clear(self, session: TelegramClient):
        async with self.storage.ainitialize_session(session):
            async for dialog in session.iter_dialogs():
                console.log(dialog)

                if not isinstance(dialog.entity, types.Channel):
                    await session(functions.messages.DeleteHistoryRequest(
                        peer=dialog.entity,
                        max_id=0,
                        just_clear=True,
                        revoke=True
                    ))
                else:
                    await session(
                        functions.channels.LeaveChannelRequest(dialog.id)
                    )

                console.log(dialog)

    async def execute(self):
        confirm = Confirm.ask("[bold red]are you sure?[/]")

        if confirm:
            await asyncio.wait([
                self.clear(session)
                for session in self.sessions
            ])

