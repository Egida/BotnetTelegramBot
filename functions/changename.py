import random
from telethon.tl.functions.account import UpdateProfileRequest
from rich.console import Console

from functions.function import Function

console = Console()


class ChangeNameFunc(Function):
    """Change names"""

    async def execute(self):
        from_file = console.input("[bold red]from file? (y/n)> ")

        for session in self.sessions:
            if from_file == "y":
                with open("assets/names.txt") as file:
                    names = file.read().strip().splitlines()

                name = random.choice(names).split()
            else:
                name = console.input("[bold red]name> [/]").split()

            first_name = name[0]

            if len(name) == 2:
                last_name = name[1]
            else:
                last_name = ""

            async with self.storage.ainitialize_session(session):
                await session(
                    UpdateProfileRequest(
                        first_name=first_name,
                        last_name=last_name
                    )
                )
