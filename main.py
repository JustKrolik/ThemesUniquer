import os
import random
import shutil
import time

import psutil as psutil

themes_path = os.path.join(os.getcwd(), "Themes")

packs_path = os.path.join(os.getcwd(), "Uniqued")

skip_extensions = ".txt"

random = random.Random()


def main():
    packs_number = int(input("Введите количество пачек: "))
    threads_limit = int(input("Введите количество потоков (Желательно устанавливать четное кол-во, не ставьте много потоков!!!): "))

    if os.listdir(packs_path):
        for file in os.listdir(packs_path):
            shutil.rmtree(file, ignore_errors=True)

    for i in range(packs_number):
        PackCreator(i, threads_limit)

    print("Done!")


def PackCreator(number, threads):
    pack_path = os.path.join(os.getcwd(), f"Uniqued\\Pack_{number}")
    if os.path.exists(pack_path):
        shutil.rmtree(pack_path, ignore_errors=True)
    os.mkdir(pack_path)

    themes = os.listdir(themes_path)
    for theme in themes:
        new_theme = os.path.join(pack_path, theme)
        os.mkdir(new_theme)

        theme_path = os.path.join(themes_path, theme)
        for filename in os.listdir(theme_path):
            file_path = os.path.join(theme_path, filename)
            if filename.lower().endswith(skip_extensions):
                shutil.copyfile(file_path, os.path.join(new_theme, filename))
                continue

            print("Check processes count...")
            processes_count = 0
            for process in psutil.process_iter():
                if process.name() == "ffmpeg.exe":
                    processes_count += 1

            while processes_count >= threads:
                print("Processes limit, waiting...")
                time.sleep(2)
                processes_count = 0
                for process in psutil.process_iter():
                    if process.name() == "ffmpeg.exe":
                        processes_count += 1

            print("Creating new process...")

            if os.path.splitext(file_path)[1] == ".mp4":
                args = [
                    f'FFMpeg\\ffmpeg.exe -i "{file_path}" -r 30 -crf {random.randint(16, 18)} -b:v 6.5M -vf eq=brightness=5 -vf eq=contrast=0.{random.randint(75, 90)} "{os.path.join(new_theme, filename)}']
                process_id = os.spawnv(os.P_NOWAIT, os.path.join(os.getcwd(), "FFMpeg\\ffmpeg.exe"), args)
            else:
                args = [
                    f'FFMpeg\\ffmpeg.exe -i "{file_path}" -vf eq=contrast=0.{random.randint(75, 99)} "{os.path.join(new_theme, filename)}']
                process_id = os.spawnv(os.P_NOWAIT, os.path.join(os.getcwd(), "FFMpeg\\ffmpeg.exe"), args)


main()
