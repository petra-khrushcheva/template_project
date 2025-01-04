from aiogram import Bot, types


async def set_default_commands(bot: Bot):
    """
    Устанавливает список команд для бота.
    Команды отображаются в интерфейсе Telegram (меню команд).
    """
    await bot.set_my_commands(
        [
            types.BotCommand(command="start", description="Начать работу"),
            types.BotCommand(command="help", description="Что может этот бот"),
        ]
    )
