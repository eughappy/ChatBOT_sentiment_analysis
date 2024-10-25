from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
import app.keyboards as kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import app.database.requests as req
from app.evaluation.evaluation_model import check_sentence, tokenizer, evaluate_model
router = Router()

class Registration(StatesGroup):
    name = State()
    age = State()
    number = State()

class Model(StatesGroup):
    evaluation = State()

@router.message(CommandStart())
async def bot_start(message: Message):
    await req.set_user(message.from_user.id)
    await message.answer('Bot is ON!', reply_markup = kb.start_buttons)

@router.message(Command('help'))
async def bot_help(message: Message):
    await message.answer('This is bot for NLP messages!\n If you want to start analise text - press button "Analysis"', 
                         reply_markup = kb.analysis_button)

@router.message()
async def bot_anyother(message: Message):
    await message.answer('This is bot for NLP messages!\n If you want to start analise text - press button "Analysis"\nYou can also ask for help - press "/help"', 
                         reply_markup = kb.start_buttons)

@router.callback_query(F.data == "exit")
async def callback_exit(callback: CallbackQuery, state: FSMContext):
    await callback.answer("You pressed button!")
    await callback.message.answer('Have a nice day!')
    await state.clear()

@router.message(Command('exit'))
async def message_exit(message: Message, state: FSMContext):
    await message.answer('Have a nice day!')
    await state.clear()

@router.message(Command('register'))
async def registration(message: Message, state: FSMContext):
    await state.set_state(Registration.name)
    await message.answer('Input your name.') 


@router.message(Registration.name)
async def registration_name(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(Registration.age)
    await message.answer('Input your age.') 

@router.message(Registration.age)
async def registration_age(message: Message, state: FSMContext):
    await state.update_data(age = message.text)
    await state.set_state(Registration.number)
    await message.answer('Input your number.', reply_markup = kb.get_number_button) 

@router.message(Registration.number, F.contact)
async def registration_number(message: Message, state: FSMContext):
    await state.update_data(number = message.contact.phone_number)
    await message.answer('Thank you!',reply_markup = kb.start_buttons) 
    data = await state.get_data()
    await message.answer(f'Your name: {data['name']}, your age: {data['age']}, your number: {data['number']}')
    await req.register_user(data['name'], data['age'], data['number'], message.from_user.id)
    await state.clear()


@router.message(Command('start_analysis'))
async def analysis(message: Message, state: FSMContext):
    await state.set_state(Model.evaluation)
    await message.answer('Input your text or tap "exit" if u want to exit analysis.') 

@router.callback_query(F.data == "analysis")
async def callback_analysis(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Model.evaluation)
    await callback.answer("You pressed button!")
    await callback.message.answer('Input your text or tap "exit" if u want to exit analysis.') 

@router.message(Model.evaluation)
async def evaluate_text(message: Message, state: FSMContext):
    await state.update_data(evaluation = message.text)
    data = await state.get_data()
    await message.answer(f'Your text is {check_sentence(data['evaluation'], evaluate_model, tokenizer)}')
    await message.answer('Input your text or tap "exit" if u want to exit analysis.') 