import Model
import View
from pynput import keyboard
import time
from pygame import mixer
import threading
import random

global_is_shiffeled = False
global_selected_play_list_id = None
global_selected_play_list = None
global_shuffeled_play_list = None
global_current_music = None
global_current_music_play = None
global_current_music_pause = False
global_play_single_music = False

global_thread = None
global_break_thread = False




def is_music_file_valid(music_name):
    return music_name.lower().endswith((".mp3", ".wav"))


def on_press_keyboard(key):
    global global_current_music_pause
    global global_current_music_play
    global global_thread
    global global_break_thread
    global global_is_shiffeled
    global global_selected_play_list
    global global_shuffeled_play_list
    global global_play_single_music

    if key == keyboard.Key.right and (not global_play_single_music):
        global_break_thread = True
        global_thread.join()
        musics = global_shuffeled_play_list if global_is_shiffeled else global_selected_play_list
        go_to_next_music(musics)

    if key == keyboard.Key.left and (not global_play_single_music):
        global_break_thread = True
        global_thread.join()
        musics = global_shuffeled_play_list if global_is_shiffeled else global_selected_play_list
        go_to_previous_music(musics)

    if key == keyboard.Key.space:
        if global_current_music_pause:
            global_current_music_play.unpause()
            global_current_music_pause = False
        else:
            global_current_music_play.pause()
            global_current_music_pause = True

    if key == keyboard.Key.esc:
        global_break_thread = True
        global_thread.join()
        global_current_music_play.stop()
        return False


def play_music(music):
    global global_current_music_play
    mixer.init()
    global_current_music_play = mixer.music
    global_current_music_play.load(music["path"])
    global_current_music_play.play()


def go_to_next_music(play_list):
    global global_current_music_play, global_current_music
    global_current_music_play.stop()
    play_list_length = len(play_list)
    current_music_index = None
    for (index, music) in enumerate(play_list):
        if music["id"] == global_current_music["id"]:
            current_music_index = index
            break
    next_music_index = current_music_index + 1
    if current_music_index == (play_list_length - 1):
        next_music_index = 0

    global_current_music = play_list[next_music_index]
    play_music(global_current_music)
    go_to_next_music_after_finish()


def go_to_previous_music(play_list):
    global global_current_music_play, global_current_music
    global_current_music_play.stop()
    play_list_length = len(play_list)
    current_music_index = None
    for (index, music) in enumerate(play_list):
        if music["id"] == global_current_music["id"]:
            current_music_index = index
            break
    prev_music_index = current_music_index - 1
    if current_music_index == 0:
        prev_music_index = play_list_length - 1

    global_current_music = play_list[prev_music_index]
    play_music(global_current_music)
    go_to_next_music_after_finish()


def thread_func(music_duration):
    global global_break_thread, global_selected_play_list_id
    global global_is_shiffeled
    global global_selected_play_list
    global global_shuffeled_play_list

    for _ in range(int(music_duration)):
        time.sleep(1)
        if global_break_thread:
            break

    musics = global_shuffeled_play_list if global_is_shiffeled else global_selected_play_list
    if not global_break_thread:
        go_to_next_music(musics)


def go_to_next_music_after_finish():
    global global_current_music, global_thread, global_break_thread
    global_break_thread = False
    global_thread = threading.Thread(
        target=thread_func, args=(global_current_music["duration"],)
    )
    global_thread.start()


def run():
    user_input = None
    section = "main_menu"
    global global_selected_play_list_id
    global global_current_music
    global global_selected_play_list 
    global global_shuffeled_play_list
    global global_is_shiffeled
    global global_play_single_music

    while user_input != 0:

        if section == "main_menu":
            user_input = View.show_main_menu_and_get_user_input()

            if user_input == 1:
                selected_play_list_id = View.show_play_lists_menu_and_get_user_input(
                    Model.get_play_lists()
                )
                if selected_play_list_id == 'back_main_menu':
                    continue
                elif selected_play_list_id == 'exit':
                    exit()
                
                else:
                    section = "play_list_menu"
                    global_selected_play_list_id = selected_play_list_id

            if user_input == 2:
                play_list = View.get_play_list_data_from_user()
                Model.add_play_list(play_list)
                print("play list added successfully.")

            if user_input == 3:
                play_list_title = View.get_play_list_title()
                play_lists = Model.get_play_list_by_title(play_list_title)
                View.show_full_play_lists_menu_and_get_user_input(play_lists)
                play_list_id = View.get_play_list_id()
                play_list = View.get_play_list_data_from_user()
                play_list["id"] = play_list_id
                if Model.update_play_list(play_list):
                    print("play list updated successfully.")
                else:
                    print("error occurred in update play list!")

            if user_input == 4:
                play_list_title = View.get_play_list_title()
                play_lists = Model.get_play_list_by_title(play_list_title)
                View.show_full_play_lists_menu_and_get_user_input(play_lists)
                play_list_id = View.get_play_list_id()
                if Model.remove_play_list(play_list_id):
                    print("play list removed successfully.")
                else:
                    print("error occurred in remove play list!")

        elif section == "play_list_menu" and global_selected_play_list_id != None:
            global_play_single_music = False
            user_input = View.show_play_list_menu_and_get_user_input()
            if user_input == 1:
                music_list = View.show_music_of_play_list(
                    Model.get_music_of_play_list(global_selected_play_list_id)
                )
                if music_list == 'back_to_play_list_menu':
                    continue
                elif music_list == 'exit':
                    exit()
                else:
                    listener = keyboard.Listener(on_press=on_press_keyboard)
                    listener.start()
                    global_play_single_music = True
                    global_current_music = Model.get_music_by_id(global_selected_play_list_id, music_list)
                    play_music(global_current_music)
                    go_to_next_music_after_finish()

            if user_input == 2:
                music_data = View.get_music_data_from_user(global_selected_play_list_id)
                if Model.add_music_to_play_list(global_selected_play_list_id, music_data):
                    print("music added successfully.")
                else:
                    print("error occurred in add music!")

            if user_input == 3:
                # edit music
                music_title = View.get_music_title()
                musics = Model.get_music_by_title(global_selected_play_list_id, music_title)
                answer = View.show_full_play_list_music_and_get_user_input(musics)
                if answer == "music_id":
                    music_id = View.get_music_id()
                    music_data = View.get_updated_music_data_from_user()
                    music = Model.get_music_by_id(global_selected_play_list_id, music_id)
                    music["title"] = music_data["title"]
                    music["artist"] = music_data["artist"]
                    music["album"] = music_data["album"]
                    if Model.update_music(global_selected_play_list_id, music):
                        print("music updated successfully.")
                    else:
                        print("error eccurred in update music!")

            if user_input == 4:
                # remove music
                music_title = View.get_music_title()
                musics = Model.get_music_by_title(global_selected_play_list_id, music_title)
                answer = View.show_full_play_list_music_and_get_user_input(musics)
                if answer == "music_id":
                    music_id = View.get_music_id()
                    if Model.remove_music(global_selected_play_list_id, music_id):
                        print("music removed successfully.")
                    else:
                        print("error occurred in remove music!")

            if user_input == 5 or user_input == 6:
                # play musics in order
                listener = keyboard.Listener(on_press=on_press_keyboard)
                listener.start()

                global_selected_play_list = Model.get_music_of_play_list(global_selected_play_list_id)
                if global_selected_play_list != None:
                    global_shuffeled_play_list = random.sample(global_selected_play_list, len(global_selected_play_list))

                    global_is_shiffeled = True if user_input == 6 else False

                    global_current_music = global_shuffeled_play_list[0] if global_is_shiffeled else global_selected_play_list[0]
                    play_music(global_current_music)
                    go_to_next_music_after_finish()

            if user_input == 7:
                section = "main_menu"
