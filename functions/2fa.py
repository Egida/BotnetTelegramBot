import asyncio
from rich.console import Console
from functions.function import Function

console = Console()

class SetPasswordFunc(Function):
    """Set two-step verification password to accounts"""

    async def execute(self):
        password = console.input("[bold red]new password> [/]")

        with console.status("Setting password..."):
            await asyncio.wait([
                session.edit_2fa(new_password=password)
                for session in self.sessions
            ])

