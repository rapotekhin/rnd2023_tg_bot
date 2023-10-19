import os
from aiogram import types
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputFile,
)
from main import bot, dp
from storage import RamStorage
from utils import save_new_user, select_molecule

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    text = """
    Добро пожаловать в чат-бот для выбора нового продукта!\n
    Помните - всё, что происходит в бойцовском клубе, остаётся в бойцовском клубе 😎

    """
    save_new_user(message)
    model_button = InlineKeyboardButton('Поехали!', callback_data="select_first")
    markup = InlineKeyboardMarkup(inline_keyboard=[[model_button]])

    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=markup,
        parse_mode=types.ParseMode.MARKDOWN,
    )


@dp.callback_query_handler(lambda c: c.data == "select_first")
async def process_callback_select_first(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    select_sema_button = InlineKeyboardButton('Семаглутид', callback_data="select_first_button_sema")
    select_natural_button = InlineKeyboardButton('Натуральный агонист', callback_data="select_first_button_natural")
    select_chimera_button = InlineKeyboardButton('Химеру 🙃', callback_data="select_first_button_chimera")
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [select_sema_button],
            [select_natural_button],
            [select_chimera_button]
        ]
    )
    text = "Что возьмём за основу?"

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=markup,
        parse_mode=types.ParseMode.MARKDOWN,
    )

@dp.callback_query_handler(lambda query: query.data.startswith("select_first_button_"))
async def process_callback_select_model_(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    selected_base = callback_query.data.replace("select_first_button_", "")

    RamStorage.users_data[callback_query.message.chat.id]['selected_base'] = selected_base

    select_3_button = InlineKeyboardButton('3', callback_data="select_second_button_3")
    select_5_button = InlineKeyboardButton('5', callback_data="select_second_button_5")
    select_10_button = InlineKeyboardButton('10', callback_data="select_second_button_10")
    back = InlineKeyboardButton('↩️ Назад', callback_data="select_first")
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [select_3_button],
            [select_5_button],
            [select_10_button],
            [back]
        ]
    )
    text = 'Сколько мутаций можно внести максимально?'

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=markup,
        parse_mode=types.ParseMode.MARKDOWN,
    )

@dp.callback_query_handler(lambda query: query.data.startswith("select_second_button_"))
async def process_callback_select_model_(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    num_mutations = callback_query.data.replace("select_second_button_", "")

    RamStorage.users_data[callback_query.message.chat.id]['num_mutations'] = num_mutations

    select_ecoli_button = InlineKeyboardButton('🦠', callback_data="select_third_button_ecoli")
    select_chem_button = InlineKeyboardButton('🧪', callback_data="select_third_button_chem")
    back = InlineKeyboardButton('↩️ Назад', callback_data="select_first_button_")
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [select_ecoli_button],
            [select_chem_button],
            [back]
        ]
    )
    text = 'Хотите получать с помощью E.coli или обойдёмся химическим синтезом?'

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=markup,
        parse_mode=types.ParseMode.MARKDOWN,
    )


@dp.callback_query_handler(lambda query: query.data.startswith("select_third_button_"))
async def process_callback_select_model_(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    synt_method = callback_query.data.replace("select_third_button_", "")

    RamStorage.users_data[callback_query.message.chat.id]['synt_method'] = synt_method

    select_mild_button = InlineKeyboardButton('Умеренно', callback_data="select_fourth_button_mild")
    select_strong_button = InlineKeyboardButton('Чем ниже KD, тем лучше💪', callback_data="select_fourth_button_strong")
    back = InlineKeyboardButton('↩️ Назад', callback_data="select_second_button_")
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [select_mild_button],
            [select_strong_button],
            [back]
        ]
    )
    text = 'Как будем активировать целевые рецепторы?'

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=markup,
        parse_mode=types.ParseMode.MARKDOWN,
    )


@dp.callback_query_handler(lambda query: query.data.startswith("select_fourth_button_"))
async def process_callback_select_model_(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    activation_method = callback_query.data.replace("select_fourth_button_", "")

    RamStorage.users_data[callback_query.message.chat.id]['activation_method'] = activation_method

    button_start_again = InlineKeyboardButton('Попробовать снова', callback_data="select_first")
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [button_start_again],
        ]
    )

    png_mol_path = select_molecule(callback_query.message)
    if png_mol_path is not None:
        text = 'Поздравляем! Вот и ваш кандидат в ЛС 😎'
        photo = InputFile(os.path.join('images', png_mol_path))
        await bot.send_photo(
            callback_query.message.from_user.id,
            photo,
            caption=text,
            reply_markup=markup,
            has_spoiler=False,
            parse_mode=types.ParseMode.MARKDOWN,
        )
    else:
        text = 'Такую молекулу не синтезировать, попробуйте снова 😢'
        await bot.send_message(
            chat_id=callback_query.message.from_user.id,
            text=text,
            reply_markup=markup,
            parse_mode=types.ParseMode.MARKDOWN,
        )


@dp.message_handler(commands=["help"])
async def send_help(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    save_new_user(message)
    await bot.send_message(
        chat_id=message.chat.id,
        text='щёлкните /start',
        parse_mode=types.ParseMode.MARKDOWN,
    )