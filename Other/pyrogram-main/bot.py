import os
import sys
from pyrogram import Client, filters
import time
import asyncio, subprocess, shutil, glob
from pathlib import Path
import time

api_id = 1220895
api_hash = "04807758f21bf166fdc7cf8d610b5daa"
bot_token = "1671260104:AAFmPdxbLq17telf5AaTlupk9ToONgbpnYM"
chat_id = 754321334

client = Client("my_account", api_id, api_hash, bot_token=bot_token)

dir_path = f"{os.path.dirname(os.path.realpath(__file__))}/urls"


@client.on_message(filters.command("start") & filters.user(chat_id))
def start(client, message):
    client.send_message(chat_id=chat_id, text="Hello! I'm Working!")


@client.on_message(filters.command("cleanup") & filters.user(chat_id))
def cleanup(client, message):
    try:
        shutil.rmtree("downloads")
        shutil.rmtree("ytdl")
        message.reply("Server cleaned!")
    except:
        message.reply("Folders not found!")


@client.on_message(filters.document & filters.user(chat_id))
async def geturls(client, message):
    chat_id = message.chat.id
    try:
        os.mkdir(dir_path)
    except:
        pass
    await client.download_media(message.document, F"{dir_path}/urls.txt")
    down_msg = await message.reply("Downloading multiple files")

    cmd = []
    cmd.append("wget")
    cmd.append("--progress=bar:force:noscroll")
    cmd.append("-P")
    cmd.append("downloads/")
    cmd.append("-i")
    cmd.append(f"{dir_path}/urls.txt")
    subprocess.run(cmd)

    files_num = 0
    for n in glob.iglob(os.path.join("downloads", "*.*")):
        files_num += 1
    print(files_num)

    await down_msg.edit(f"Downloading Completed!\n{files_num} files found.")

    try:
        for file in glob.iglob(os.path.join("downloads", "*.*")):
            filename = str(Path(file)).replace("downloads/", "")
            filesize = os.path.getsize(file)
            if filesize < 2000000000:
                upload_msg = await client.send_message(
                    chat_id=chat_id, text="Uploading...")

                async def progress(current, total):
                    print(f"{filename}\n{current * 100 / total:.1f}%")

                await client.send_document(
                    chat_id=chat_id, document=file, caption=filename, progress=progress)
                os.remove(file)
                await upload_msg.delete()

            else:
                client.send_message(
                    chat_id=chat_id, text=f"Found a file larger than Telegram API's limits.\nFilename : {filename}\nSize : {filesize} ")
    except Exception as e:
        client.send_message(
            chat_id=chat_id, text=str(e))


@ client.on_message(filters.command("ytdl") & filters.user(chat_id))
async def ytdl(client, message):
    url = message.text.replace("/ytdl ", "")
    cmd = ["youtube-dl", "-o", "ytdl/%(title)s.%(ext)s", "--restrict-filenames", "-f",
           "bestvideo[height<=720]+bestaudio", url, "--yes-playlist", "--merge-output-format", "mp4", "--all-subs", "--sub-format", "srt", "--embed-subs"]
    subprocess.call(cmd)

    try:
        for file in glob.iglob(os.path.join("ytdl", "*.*")):
            filename = str(Path(file)).replace("ytdl/", "")
            filesize = os.path.getsize(file)
            if filesize < 2000000000:
                upload_msg = await client.send_message(
                    chat_id=chat_id, text="Uploading...")

                def progress(current, total):
                    print(f"{filename}\n{current * 100 / total:.1f}%")

                await client.send_document(
                    chat_id=chat_id, document=file, caption=filename, progress=progress)
                os.remove(file)
                await upload_msg.delete()
    except Exception as e:
        client.send_message(
            chat_id=chat_id, text=str(e))


@ client.on_message(filters.command("wget") & filters.user(chat_id))
async def wgetlink(client, message):
    url = message.text.replace("/wget ", "")
    chat_id = message.chat.id
    down_msg = await message.reply("Downloading file...")

    cmd = ["wget", "--progress=bar:force:noscroll",
           "-P", "downloads/", "-i", url]
    subprocess.run(cmd)

    await down_msg.edit(f"Downloading Completed!")

    try:
        for file in glob.iglob(os.path.join("downloads", "*.*")):
            filename = str(Path(file)).replace("downloads/", "")
            filesize = os.path.getsize(file)
            if filesize < 2000000000:
                upload_msg = await client.send_message(
                    chat_id=chat_id, text="Uploading...")

                async def progress(current, total):
                    print(f"{filename}\n{current * 100 / total:.1f}%")

                await client.send_document(
                    chat_id=chat_id, document=file, caption=filename, progress=progress)
                os.remove(file)
                await upload_msg.delete()

            else:
                client.send_message(
                    chat_id=chat_id, text=f"Found a file larger than Telegram API's limits.\nFilename : {filename}\nSize : {filesize} ")
    except Exception as e:
        client.send_message(
            chat_id=chat_id, text=str(e))


if __name__ == "__main__":
    client.run()
