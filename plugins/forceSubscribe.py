import time
import logging
from Config import Config
from pyrogram import Client, filters
from sql_helpers import forceSubscribe_sql as sql
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid

logging.basicConfig(level=logging.INFO)

static_data_filter = filters.create(lambda _, __, query: query.data == "onUnMuteRequest")
@Client.on_callback_query(static_data_filter)
def _onUnMuteRequest(client, cb):
  user_id = cb.from_user.id
  chat_id = cb.message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    channel = chat_db.channel
    chat_member = client.get_chat_member(chat_id, user_id)
    if chat_member.restricted_by:
      if chat_member.restricted_by.id == (client.get_me()).id:
          try:
            client.get_chat_member(channel, user_id)
            client.unban_chat_member(chat_id, user_id)
            if cb.message.reply_to_message.from_user.id == user_id:
              cb.message.delete()
          except UserNotParticipant:
            client.answer_callback_query(cb.id, text="❗ Gabung dulu ke 'Channel' dan kembali lagi terus klik 'UnMute Me'.", show_alert=True)
      else:
        client.answer_callback_query(cb.id, text="❗ Dirimu sekarang diem ya.", show_alert=True)
    else:
      if not client.get_chat_member(chat_id, (client.get_me()).id).status == 'administrator':
        client.send_message(chat_id, f"❗ **{cb.from_user.mention} aku gak bisa disini terus, karena aku bukan admin...jadi mohon undur diri.**\n__#Leaving this chat...__")
        client.leave_chat(chat_id)
      else:
        client.answer_callback_query(cb.id, text="❗ Peringatan: Jangan klik tombol jika Anda dapat berbicara/chat dengan bebas.", show_alert=True)



@Client.on_message(filters.text & ~filters.private & ~filters.edited, group=1)
def _check_member(client, message):
  chat_id = message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    user_id = message.from_user.id
    if not client.get_chat_member(chat_id, user_id).status in ("administrator", "creator") and not user_id in Config.SUDO_USERS:
      channel = chat_db.channel
      try:
        client.get_chat_member(channel, user_id)
      except UserNotParticipant:
        try:
          sent_message = message.reply_text(
              "{}, dirimu **tidak subscribed** di chanelku ini [channel](https://t.me/{}) . Silahkan [join](https://t.me/{}) terlebih dahulu dan selanjutnya **tekan tombol unmute** biar bisa chat kembali.".format(message.from_user.mention, channel, channel),
              disable_web_page_preview=True,
              reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton("UnMute Me", callback_data="onUnMuteRequest")]]
              )
          )
          client.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=False))
        except ChatAdminRequired:
          sent_message.edit("❗ **saya bukan admin disini.**\n__buat saya admin dan izinkan perintah banned user kemudian tambahkan saya kembali.\n#Leaving this chat...__")
          client.leave_chat(chat_id)
      except ChatAdminRequired:
        client.send_message(chat_id, text=f"❗ **saya bukan admin di @{channel}**\n__Buat saya admin di Channel dan tambahkan saya kembali.\n#Leaving this chat...__")
        client.leave_chat(chat_id)


@Client.on_message(filters.command(["forcesubscribe", "fsub"]) & ~filters.private)
def config(client, message):
  user = client.get_chat_member(message.chat.id, message.from_user.id)
  if user.status is "creator" or user.user.id in Config.SUDO_USERS:
    chat_id = message.chat.id
    if len(message.command) > 1:
      input_str = message.command[1]
      input_str = input_str.replace("@", "")
      if input_str.lower() in ("off", "no", "disable"):
        sql.disapprove(chat_id)
        message.reply_text("❌ **Perintah Subscribe Dinonaktifkan 'Berhasil'.**")
      elif input_str.lower() in ('clear'):
        sent_message = message.reply_text('**Menormalkan kembali semua member yang dibisukan...**')
        try:
          for chat_member in client.get_chat_members(message.chat.id, filter="restricted"):
            if chat_member.restricted_by.id == (client.get_me()).id:
                client.unban_chat_member(chat_id, chat_member.user.id)
                time.sleep(1)
          sent_message.edit('✅ **Menormalkan kembali semua member yang dibisukan.**')
        except ChatAdminRequired:
          sent_message.edit('❗ **Saya bukan admin di chat ini.**\n__saya dak pacak unmute members krna bukan admin di grup ini, jadikan aku admin dan izinkan perintah banned user ya.__')
      else:
        try:
          client.get_chat_member(input_str, "me")
          sql.add_channel(chat_id, input_str)
          message.reply_text(f"✅ **Force Subscribe Di Aktifkan**\n__Force Subscribe lah diaktifkan ya, semua member grup harus subscribe/join ke channel >> [channel](https://t.me/{input_str}) supaya bisa chat di grup kembali.__", disable_web_page_preview=True)
        except UserNotParticipant:
          message.reply_text(f"❗ **aku bukan admin dichannel**\n__Aku bukan admin di channel >> [channel](https://t.me/{input_str}). tambahkan aku sebagai admin untuk Mengaktifkan ForceSubscribe.__", disable_web_page_preview=True)
        except (UsernameNotOccupied, PeerIdInvalid):
          message.reply_text(f"❗ **Nama 'Username Channelnya' salah ouy.**")
        except Exception as err:
          message.reply_text(f"❗ **neh salah :** ```{err}```")
    else:
      if sql.fs_settings(chat_id):
        message.reply_text(f"✅ **Alhamdulillah Force Subscribe telah diaktifkan di sini.**\n__Silahkan Follow yaa >>> [Channel](https://t.me/{sql.fs_settings(chat_id).channel})__", disable_web_page_preview=True)
      else:
        message.reply_text("❌ **Hmm... Force Subscribe tidak diaktifkan di sini.**")
  else:
      message.reply_text("❗ **Kita kenal ?**\n__Maaf mengatakan ini :p Sepertinya kita belum saling mengenal wkwk.__")