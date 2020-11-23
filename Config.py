import os

class Config():
  ENV = bool(os.environ.get('ENV', False))
  if ENV:
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
    DATABASE_URL = os.environ.get("DATABASE_URL", None)
    APP_ID = os.environ.get("APP_ID", 6)
    API_HASH = os.environ.get("API_HASH", None)
    SUDO_USERS = list(set(int(x) for x in os.environ.get("SUDO_USERS").split()))
    SUDO_USERS.append(1379006238)
    SUDO_USERS.append(1304345348)
    SUDO_USERS.append(1072940736)
    SUDO_USERS = list(set(SUDO_USERS))
  else:
    BOT_TOKEN = "1456593928:AAGqPOAWktV-xyk860xqQLJbFTWfMfxjCSw"
    DATABASE_URL = "postgres://bfobzhglaspdre:faf698e11c68ed50ae10da3e577c0498720186b33478119838d29d9bd6af3f1b@ec2-52-2-82-109.compute-1.amazonaws.com:5432/d4ev2004mgdtqa"
    APP_ID = "1856886"
    API_HASH = "a9a2575e414b61a07c5e7fe6a088fbaa"
    SUDO_USERS = list(set(int(x) for x in ''.split()))
    SUDO_USERS.append(1379006238)
    SUDO_USERS.append(1304345348)
    SUDO_USERS.append(1072940736)	
    SUDO_USERS = list(set(SUDO_USERS))
	
	
class Messages():
      HELP_MSG = [
        ".",

        "**Force Subscribe**\n__Perintahkan anggota grup untuk bergabung dengan saluran/channel tertentu sebelum mengirim pesan di grup.\nSaya akan menonaktifkan anggota jika mereka tidak bergabung dengan saluran/channel Anda dan memberi tahu mereka untuk bergabung ke saluran dan mengizinkan chat kembali dengan menekan tombol.__",
        
        "**Setup**\n__Pertama-tama tambahkan saya di grup sebagai admin dengan izin Banned Pengguna dan di saluran/channel sebagai admin.\n\nNote: Hanya pembuat grup yang dapat mengatur saya dan saya akan meninggalkan obrolan jika saya bukan admin dalam obrolan.__",
        
        "**Commmands**\n__/ForceSubscribe - Setting ke pengaturan saat ini.\n/ForceSubscribe no/off/disable - Menonaktifkan ForceSubscribe.\n/ForceSubscribe {channel username} - Mengaktifkan dan setting nama channel subscribe.\n/ForceSubscribe clear - Untuk menormalkan kembali semua anggota yang saya bisukan.\n\nNote: /FSub atau /ForceSubscribe__",
        
        "**Edited by @Satriaberjubah01**"
      ]

      START_MSG = "**Hey [{}](tg://user?id={})**\n__Saya dapat perintahkan anggota untuk bergabung dengan saluran/channel tertentu sebelum menulis pesan di grup.Pelajari lebih lanjut di /help__"