import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

from config import TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- клавиатура под полем ввода ---
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/help")],
        [KeyboardButton(text="/calc 2 + 2")],
        [KeyboardButton(text="/calc 10 / 3")],
    ],
    resize_keyboard=True
)


def calculate(a: float, op: str, b: float):
    """Простой калькулятор для двух чисел и операции."""
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        if b == 0:
            return "Ошибка: деление на ноль"
        return a / b
    return "Неизвестная операция"


@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer(
        "Привет! 👋\n"
        "Я учебный калькулятор-бот.\n\n"
        "Команды:\n"
        "/start — начать\n"
        "/help — помощь\n"
        "/calc a op b — посчитать выражение\n"
        "Например: /calc 2 + 2\n"
        "Поддерживаемые операции: +  -  *  /",
        reply_markup=main_kb
    )


@dp.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer(
        "Я умею считать выражения вида:\n"
        "/calc a op b\n\n"
        "Примеры:\n"
        "/calc 2 + 2\n"
        "/calc 10 - 3\n"
        "/calc 5 * 6\n"
        "/calc 8 / 2\n\n"
        "Поддерживаемые операции: +  -  *  /"
    )


@dp.message(Command("calc"))
async def calc_cmd(message: Message):
    # ожидаем формат: /calc a op b
    try:
        parts = message.text.split()

        if len(parts) != 4:
            await message.answer(
                "Неверный формат.\nИспользуй: /calc a op b\nНапример: /calc 2 + 2"
            )
            return

        _, a_str, op, b_str = parts

        a = float(a_str)
        b = float(b_str)

        result = calculate(a, op, b)

        await message.answer(f"Результат: {result}")
    except ValueError:
        await message.answer(
            "Не получилось преобразовать числа.\n"
            "Проверь, что a и b — это числа.\n"
            "Пример: /calc 2.5 * 4"
        )
    except Exception as e:
        logging.exception(e)
        await message.answer("Произошла ошибка при вычислении.")


@dp.message()  # все остальные сообщения
async def echo(message: Message):
    await message.answer("Неизвестная команда. Попробуй /help")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
