import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

BOT_TOKEN = "8333608600:AAEVECVuKvn0BSnv8ZEqkme_XsFPCv1R4_4"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class UserState(StatesGroup):
    language = State()

lang_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🇰🇬 Кыргызча"), KeyboardButton(text="🇷🇺 Русский")]],
    resize_keyboard=True
)

main_keyboard_kg = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📜 ЧУА базасы"), KeyboardButton(text="⚠️ Кызыкчылыктар кагылышы")],
        [KeyboardButton(text="🎁 Белектер жана Жыйымдар"), KeyboardButton(text="🏆 Спорттогу коррупция")],
        [KeyboardButton(text="📞 Мыйзам бузууну кабарлоо"), KeyboardButton(text="🌐 Тилди өзгөртүү")]
    ],
    resize_keyboard=True
)

main_keyboard_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📜 База НПА"), KeyboardButton(text="⚠️ Конфликт интересов")],
        [KeyboardButton(text="🎁 Подарки и Сборы"), KeyboardButton(text="🏆 Коррупция в спорте")],
        [KeyboardButton(text="📞 Сообщить о нарушении"), KeyboardButton(text="🌐 Сменить язык")]
    ],
    resize_keyboard=True
)

sport_kb_kg = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Макулдашылган оюндар жана калыстык", callback_data="match_fixing")],
        [InlineKeyboardButton(text="Жабдууларды сатып алуу жана ОМЖ", callback_data="procurement_uts")],
        [InlineKeyboardButton(text="Спорттук наамдарды жана разряддарды ыйгаруу", callback_data="titles_ranks")]
    ]
)

sport_kb_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Договорные матчи и судейство", callback_data="match_fixing")],
        [InlineKeyboardButton(text="Закупки инвентаря и учебно-тренировочные сборы", callback_data="procurement_uts")],
        [InlineKeyboardButton(text="Присвоение званий и разрядов", callback_data="titles_ranks")]
    ]
)

@dp.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(UserState.language)
    text = "Саламатсызбы! Тилди тандаңыз / Здравствуйте! Выберите язык:\n\n🇰🇬 **Кыргыз тили**\n🇷🇺 **Русский язык**"
    await message.answer(text, parse_mode="Markdown", reply_markup=lang_keyboard)

@dp.message(F.text.in_(["🌐 Тилди өзгөртүү", "🌐 Сменить язык"]))
async def change_language(message: types.Message, state: FSMContext):
    await state.set_state(UserState.language)
    await message.answer("Тилди тандаңыз / Выберите язык:", reply_markup=lang_keyboard)

@dp.message(UserState.language, F.text == "🇰🇬 Кыргызча")
async def set_lang_kg(message: types.Message, state: FSMContext):
    await state.update_data(language="kg")
    await state.set_state(None)
    welcome_text = f"Саламатсызбы, {message.from_user.first_name}!\n\nМен **Кыргыз Республикасынын Дене тарбия жана спорт чөйрөсүндө коррупцияга каршы аракеттенүү** маселелери боюнча маалыматтык чат-ботмун.\n\nТөмөндөгү менюдан сизди кызыктырган бөлүмдү тандаңыз:"
    await message.answer(welcome_text, parse_mode="Markdown", reply_markup=main_keyboard_kg)

@dp.message(UserState.language, F.text == "🇷🇺 Русский")
async def set_lang_ru(message: types.Message, state: FSMContext):
    await state.update_data(language="ru")
    await state.set_state(None)
    welcome_text = f"Саламатсызбы, {message.from_user.first_name}!\n\nЯ информационный бот по вопросам **противодействия коррупции в сфере физической культуры и спорта Кыргызской Республики**.\n\nВыберите интересующий вас раздел в меню ниже:"
    await message.answer(welcome_text, parse_mode="Markdown", reply_markup=main_keyboard_ru)

@dp.message(F.text.in_(["📜 ЧУА базасы", "📜 База НПА"]))
async def show_npa(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "ru")
    if lang == "kg":
        text = "📚 **Кыргыз Республикасынын коррупцияга каршы негизги мыйзамдары:**\n\n1. **КР «Коррупцияга каршы аракеттенүү жөнүндө» Мыйзамы**\n2. **КР «Кызыкчылыктардын кагылышуусу жөнүндө» Мыйзамы**\n3. **КР «Мамлекеттик жарандык кызмат жана муниципалдык кызмат жөнүндө» Мыйзамы**\n4. **КР Кылмыш-жаза кодекси (42-глава)**\n5. **Мамлекеттик жана муниципалдык кызматчылардын этика кодекси**."
    else:
        text = "📚 **Основное антикоррупционное законодательство Кыргызской Республики:**\n\n1. **Закон КР «О противодействии коррупции»**\n2. **Закон КР «О конфликте интересов»**\n3. **Закон КР «О государственной гражданской службе и муниципальной службе»**\n4. **Уголовный кодекс КР (Глава 42)**\n5. **Кодекс этики государственных и муниципальных служащих КР**."
    await message.answer(text, parse_mode="Markdown")

@dp.message(F.text.in_(["⚠️ Кызыкчылыктар кагылышы", "⚠️️ Конфликт интересов"]))
async def show_conflict(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "ru")
    if lang == "kg":
        text = "⚠️ **Кызыкчылыктардын кагылышуусу** — кызматчынын жеке кызыкчылыгы анын кызматтык милдеттерин калыс аткаруусуна таасир эткен кырдаал.\n\n**Спорт чөйрөсүндөгү мисалдар:**\n• Жакын туугандарын нормативсиз эле ОМЖга же делегацияга кошуу.\n• Кызматчы же анын тууганы уюштуруучу болгон спорттук уюмду каржылоо.\n\n**Эмне кылуу керек?**\nКызматчы чечим кабыл алганга чейин жетекчисине келип чыккан кызыкчылыктардын кагылышуусу жөнүндө жазуу жүзүндө билдирүүгө милдеттүү."
    else:
        text = "⚠️ **Конфликт интересов** — ситуация, при которой личная заинтересованность служащего влияет на исполнение обязанностей.\n\n**Примеры в спортивной сфере:**\n• Включение близких родственников в состав сборных или делегаций на УТС без выполнения нормативов.\n• Финансирование спортивной организации, где служащий или его родственник является учредителем.\n\n**Что делать?**\nСлужащий обязан в письменной форме уведомить своего руководителя до принятия любого решения."
    await message.answer(text, parse_mode="Markdown")

@dp.message(F.text.in_(["🎁 Белектер жана Жыйымдар", "🎁 Подарки и Сборы"]))
async def show_gifts(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "ru")
    if lang == "kg":
        text = "🎁 **Белектерди жана акча каражаттарын алуу боюнча чектөөлөр:**\n\n1. **Белектерге тыюу салуу:** Кызматчыларга белектерди, акчаларды алууга тыюу салынат.\n2. **Протоколдук белектер:** Расмий иш-чараларда алынган белектер мамлекеттик менчикке өткөрүлөт.\n3. **ОМЖ каржылоо:** Бардык колдоо расмий эсептер аркылуу өтүшү керек. Накталай акча чогултуу мыйзам бузуу болуп саналат."
    else:
        text = "🎁 **Ограничения по получению подарков и денежных средств:**\n\n1. **Запрет на подарки:** Служащим запрещается принимать подарки, деньги или услуги.\n2. **Протокольные мероприятия:** Подарки, полученные на официальных мероприятиях, передаются в госорган.\n3. **Финансирование УТС:** Вся поддержка должна проходить строго через официальные счета. Взимание наличных средств «на руки» запрещено."
    await message.answer(text, parse_mode="Markdown")

@dp.message(F.text.in_(["🏆 Спорттогу коррупция", "🏆 Коррупция в спорте"]))
async def show_sport_corruption(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "ru")
    if lang == "kg":
        await message.answer("Спорт тармагынын өзгөчөлүктөрү боюнча кеңири маалымат алуу үчүн ички бөлүмдү тандаңыз:", reply_markup=sport_kb_kg)
    else:
        await message.answer("Выберите подкатегорию для получения подробной информации по спортивной отрасли:", reply_markup=sport_kb_ru)

@dp.callback_query(F.data == "match_fixing")
async def cb_match_fixing(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "ru")
    text = "⚽ **Макулдашылган оюндар:** Расмий спорттук мелдештердин жыйынтыктарына мыйзамсыз таасир этүү кылмыш жоопкерчилигине алып келет." if lang == "kg" else "⚽ **Договорные матчи:** Противоправное влияние на результаты официальных спортивных соревнований влечет уголовную ответственность."
    await callback.message.answer(text, parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "procurement_uts")
async def cb_procurement(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "ru")
    text = "🏋️ **Закупкалар жана ОМЖ:** Инвентарь сатып алуу портал аркылуу өтүшү керек. Жыйындарга катышпаган адамдарды тизмеге кошуу — бюджетти коротуу болуп саналат." if lang == "kg" else "🏋️ **Закупки и УТС:** Закупка инвентаря должна производиться через госпортал. «Призрачные» участники сборов квалифицируются как растрата средств."
    await callback.message.answer(text, parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "titles_ranks")
async def cb_titles(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "ru")
    text = "🏅 **Спорттук наамдар:** Наамдарды мыйзамсыз ыйгаруу үчүн пара талап кылуу кылмыш жоопкерчилигине туура келет." if lang == "kg" else "🏅 **Присвоение званий:** Вымогательство или подкуп за присвоение званий подпадает под статьи УК КР."
    await callback.message.answer(text, parse_mode="Markdown")
    await callback.answer()

@dp.message(F.text.in_(["📞 Мыйзам бузууну кабарлоо", "📞 Сообщить о нарушении"]))
async def show_report_info(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "ru")
    if lang == "kg":
        text = "📞 **Коррупциялык фактылар боюнча кайда кайрылуу керек:**\n\n• **КР Башкы прокуратурасы:** +996 (312) 54-28-18\n• **КР УКМК:** +996 (312) 66-04-75\n• **КР ИИМ:** 102\n\n*Кабарлаган адамдарды коргоого мыйзам тарабынан кепилдик берилет.*"
    else:
        text = "📞 **Куда обращаться при фактах коррупции:**\n\n• **Генеральная прокуратура КР:** +996 (312) 54-28-18\n• **ГКНБ КР:** +996 (312) 66-04-75\n• **МВД КР:** 102\n\n*Законодательством КР гарантируется защита лиц, сообщивших о фактах коррупции.*"
    await message.answer(text, parse_mode="Markdown")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
