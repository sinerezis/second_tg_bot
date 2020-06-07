import config
import logging
import asyncio
from datetime import datetime

from sqlighter import SQLighter
from aiogram import Bot, Dispatcher, executor, types
from stopgame import StopGame




logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

db = SQLighter('db.db')

sg = StopGame('lastkey.txt')

@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if (not db.subscriber_exist(message.from_user.id)):
        db.add_subscriber(message.from_user.id)
    else:
        db.update_subscriptions(message.from_user.id, True)

    await message.answer('U are welcome, hbro!')


@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):  
    if (not db.subscriber_exist(message.from_user.id)):
        db.add_subscriber(message.from_user.id, False)
        await message.answer('Huy sosi!')
    else:
        db.update_subscriptions(message.from_user.id, False)
        await message.answer('poka!')

async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        new_games = sg.new_games()

        if (new_games):
            new_games.reverse()
            for ng in new_games:
                nfo = sg.game_info(ng)
                subscriptions = db.get_subscriptions()
                with open(sg.download_image(nfo['image']), 'rb') as photo:
                    for s in subscriptions:
                        await bot.send_photo(
                                s[1],
                                photo,
                                caption=nfo['title'] + '\n' + 'оценка ' + nfo['score'] + '\n',
                                disable_notification= True
                                )
                sg.update_lastkey(nfo['id'])

def main():
    
    executor.start_polling(dp, skip_updates=True)
    

if __name__ == '__main__':
    main()
