import asyncio
from argparse import ArgumentParser
from enum import StrEnum
from pathlib import Path
from sys import argv

from alembic import command
from alembic.config import Config
from loguru import logger
from pyrogram import Client

from src import scheduler, app
from src.common.settings import Settings

settings = Settings()
alembic_cfg = Config(Path(settings.base_dir).parent / "alembic.ini")


class Commands(StrEnum):
    GENERATE_SESSION = "generate_session"
    MIGRATE = "migrate"
    START = "start"


async def generate_session_callback(api_id: str, api_hash: str) -> None:
    async with Client(
        name="smedia_session_generate",
        api_id=api_id,
        api_hash=api_hash,
    ) as client:
        session_string = await client.export_session_string()

        return print(session_string)


def register_commands(parser: ArgumentParser) -> None:
    commands = parser.add_subparsers(
        title="Управление ботом", dest="commands", required=True
    )

    generate_session_command = commands.add_parser(
        Commands.GENERATE_SESSION,
        help="Сгенерировать сессию для аккаунта.",
    )
    generate_session_command.add_argument("--id", required=True, help="API ID аккаунта")
    generate_session_command.add_argument(
        "--hash", required=True, help="API Hash аккаунта"
    )

    commands.add_parser(Commands.MIGRATE, help="Мигрировать базу данных.")

    commands.add_parser(Commands.START, help="Запустить бота.")


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="Smedia CLI", description="Интерфейс управление ботом."
    )
    register_commands(parser)

    args = parser.parse_args(argv[1:])

    match args.commands:
        case Commands.GENERATE_SESSION:
            api_id = args.id.strip()
            api_hash = args.hash.strip()

            asyncio.run(generate_session_callback(api_id, api_hash))
        case Commands.MIGRATE:
            command.upgrade(alembic_cfg, "head")
        case Commands.START:
            scheduler.start()
            logger.success("Scheduler started!")

            app.run()
