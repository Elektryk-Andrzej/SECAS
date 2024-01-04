import discord
from datetime import timedelta

wierd_string_thingie: str = "||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| _ _ _ _ _ _"


async def kissmass(msg):
    await msg.reply(
        f"literally you {wierd_string_thingie}https://cdn.discordapp.com/attachments/731637588074430512/1188442829924597780/its_beginning_to_look_a_lot_like_kissmas_boykisser_song.mp4?ex=659a8aa2&is=658815a2&hm=185ee65bb35305647b57d29704f62fb43e3accecf3456e45bf9070e9e3b75508&",
        mention_author=False
    )


async def bomb_them(msg):
    await msg.reply(
        f"{wierd_string_thingie}https://cdn.discordapp.com/attachments/958318409681104966/1162163381512450058/bomb.mov?ex=653aeffe&is=65287afe&hm=9f05e55bb0d188bc797391ab583e99b646fd8f1f349098aaf902133a4f31babc&",
        mention_author=False
    )


async def timeout_clarkson(msg: discord.Message, time: timedelta | None = None) -> bool:
    try:
        await msg.author.timeout(time)
        await msg.reply(
            f"{wierd_string_thingie}https://cdn.discordapp.com/attachments/1141640697234071632/1192559497932189706/Untitled.mov?ex=65a98494&is=65970f94&hm=7c1db6982aff4dbe9f74e24e0220ea92ecf2f70cc13125d895bd16f83fe03910&",
            mention_author=False
        )
        return True
    except:
        return False
