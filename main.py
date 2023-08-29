import asyncio
import telegram


async def main():
    bot = telegram.Bot("TOKEN")

    async with bot:
        print((await bot.get_updates()))
    
    async with bot:
        await bot.send_message(text="TEST", chat_id=701329596)


if __name__ == "__main__":
    asyncio.run(main())
