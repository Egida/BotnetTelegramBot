import random
import os

from telethon import functions, types

from rich.progress import track
from rich.console import Console

from functions.function import Function

console = Console()


class ChangeProfilePhotoFunc(Function):
    """Change profile photo"""

    async def execute(self):
        path = os.path.join(os.getcwd(), "assets", "photos")
        console.input(
            f"\n[bold white]will be used photos from folder {path}"
            "\nPress [Enter] to continue[/]"
        )
        
        photos = os.listdir(path)

        for index, session in track(
            enumerate(self.sessions),
            "[yellow]Setting photos...[/]",
            total=len(self.sessions)
        ):
            photo = os.path.join(
                path, random.choice(photos)
            )

            async with self.storage.ainitialize_session(session):
                me = await session.get_me()
                try:
                    await session(functions.photos.UploadProfilePhotoRequest(
                        file=await session.upload_file(photo),
                    ))
                except Exception as err:
                    console.print(
                        "[{name}] [bold red]error.[/] {err}"
                        .format(name=me.first_name, error=err)
                    )

