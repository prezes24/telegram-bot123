import asyncio
from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest

# === KONFIGURACJA KONT (API i sesje)
accounts = [ 

    
 
    {
        "session": "bot1",
        "api_id": 28622498,
        "api_hash": "11e81a96d4b3e64fa345b7a899c6590e",
        "phone": "+48575861211"
    },
    {
        "session": "bot2",
        "api_id": 24969437,
        "api_hash": "e21e415a2a91f3bda7a5d42a0db79738",
        "phone": "+48575861295"
    },
    
]

# === GRUPY
source_group = 'https://t.me/ZRZUTOWNIA'

target_groups = [
     'https://t.me/gm2lmarket',
    'https://t.me/WOLUMEN24NA7',
    'https://t.me/Mefedronowe_lowe',
    'https://t.me/DRAGSPAM',
    'https://t.me/wwa420',
    'https://t.me/ryneknynek',
    'https://t.me/KrakowskiRyneczek',
    'https://t.me/GROCHOW',
    'https://t.me/PRASZKANOCA022',
    'https://t.me/top1legitni',
    'https://t.me/+EI7msagI-A4wYjI0',
    'https://t.me/+HxxNtDbL5gVhMjM0',
    'https://t.me/ogtelegrammarket',
    'https://t.me/G_MARKET8',
    'https://t.me/SklepikOsiedlowyABC',
    'https://t.me/wtswtb022',
    'https://t.me/warszawaitrawa',
    'https://t.me/polishbrighton',
    'https://t.me/warszawa_sobie_radzi',
    'https://t.me/CentrumBHP',
    'https://t.me/WTS_KRK_Warszawa',
    'https://t.me/koradubaZak',
    'https://t.me/wawawts',
    'https://t.me/warszawa_sobie_radzi',
    'https://t.me/DRAGSPAM',
    'https://t.me/halokontakcik',
    'https://t.me/polishbrighton',
    'https://t.me/GROCHOW',
    'https://t.me/zlamaczeta',


    
    # dodaj więcej grup wg potrzeb
]

delay_between_messages = 15
delay_between_rounds = 30  # np. 10 minut

# === FUNKCJA WYSYŁANIA Z JEDNEGO KONTA
async def forward_from_account(account):
    try:
        async with TelegramClient(account["session"], account["api_id"], account["api_hash"]) as client:
            await client.start(account["phone"])
            print(f"✅ Zalogowano jako {account['phone']}")

            source_entity = await client.get_entity(source_group)
            full_chat = await client(GetFullChannelRequest(source_entity))
            pinned_id = full_chat.full_chat.pinned_msg_id
            if not pinned_id:
                print(f"⚠️ Brak przypiętej wiadomości w {source_group}")
                return

            pinned_msg = await client.get_messages(source_entity, ids=pinned_id)
            print(f"📌 Pobrano wiadomość z {source_group}: {pinned_msg.id}")

            while True:
                for target in target_groups:
                    try:
                        entity = await client.get_entity(target)
                        await client.send_message(entity, pinned_msg.message)
                        print(f"[{account['phone']}] ✅ Wysłano do: {target}")
                    except Exception as e:
                        print(f"[{account['phone']}] ❌ Błąd: {target} — {e}")
                    await asyncio.sleep(delay_between_messages)
                print(f"[{account['phone']}] ⏳ Oczekiwanie {delay_between_rounds}s...")
                await asyncio.sleep(delay_between_rounds)

    except Exception as e:
        print(f"[{account['phone']}] ❌ Krytyczny błąd: {e}")

# === URUCHOMIENIE DLA WSZYSTKICH KONT
async def main():
    tasks = [forward_from_account(acc) for acc in accounts]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())