from loguru import logger

from src import scheduler, app

if __name__ == "__main__":
    logger.success("Bot started!")

    scheduler.start()
    app.run()
