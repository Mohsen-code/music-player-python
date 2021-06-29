import inquirer
import uuid
import datetime
from pathlib import Path
# from mutagen import File, mp3
from tinytag import TinyTag


def show_main_menu_and_get_user_input():
    questions = [
        inquirer.List(
            "main_menu",
            message="Main Menu",
            choices=[
                ("Play Lists", 1), 
                ("Add Play List", 2), 
                ("Edit Play List", 3), 
                ("Remove Play List", 4), 
                ("exit", 0)
                ],
        ),
    ]

    answers = inquirer.prompt(questions)
    return answers['main_menu']


def show_play_lists_menu_and_get_user_input(play_lists):

    if len(play_lists) == 0:
        print('there is no play list!!')

    mapped_paly_list = list(map(lambda paly_list: (paly_list['title'], paly_list['id']), play_lists))
    mapped_paly_list.append(('back to main menu', 'back_main_menu'))
    mapped_paly_list.append(('exit', 'exit'))
    
    questions = [
        inquirer.List(
            "paly_lists_menu",
            message="Play Lists Menu",
            choices= mapped_paly_list,
        ),
    ]

    answers = inquirer.prompt(questions)
    return answers['paly_lists_menu']


def show_full_play_lists_menu_and_get_user_input(play_lists):

    if len(play_lists) == 0:
        print('there is no play list!!')
    else:
        for (index, play_list) in enumerate(play_lists):
            print(f"{index + 1}: \n   id: {play_list['id']}\n   title: {play_list['title']}\n   description: {play_list['description']}\n ")


    mapped_paly_list = [('enter play list id', 'play_list_id'), ('back to main menu', 'back_main_menu'), ('exit', 'exit')]

    questions = [
        inquirer.List(
            "paly_lists_menu",
            message="Play Lists Menu",
            choices= mapped_paly_list,
        ),
    ]

    answers = inquirer.prompt(questions)
    return answers['paly_lists_menu']


def get_play_list_id():
    questions = [
        inquirer.Text('id', message='Please enter play list id')
    ]

    answer = inquirer.prompt(questions)
    return answer['id']

def get_play_list_data_from_user():
    questions = [
        inquirer.Text('title', message='Please enter title'),
        inquirer.Text('description', message='Please enter description'),
    ]

    answer = inquirer.prompt(questions)
    answer["id"] = uuid.uuid4().hex
    answer["date"] = int(datetime.datetime.now().timestamp())

    return answer

def get_play_list_title():
    questions = [
        inquirer.Text('title', message='Please enter play list title')
    ]
    answer = inquirer.prompt(questions)

    return answer['title']

def show_play_list_menu_and_get_user_input():
    questions = [
        inquirer.List(
            "main_menu",
            message="Play List Menu",
            choices=[
                ("Show Musics", 1), 
                ("Add Music", 2), 
                ("Edit Music", 3), 
                ("Remove Music", 4), 
                ("Play", 5), 
                ("Shuffel Play", 6), 
                ("Back To Play Lists", 7), 
                ("exit", 0)
                ],
        ),
    ]

    answers = inquirer.prompt(questions)
    return answers['main_menu']


def show_play_lists(play_lists):
    if len(play_lists) > 0:
        for (index, play_list) in enumerate(play_lists):
            print(f"\n{index + 1} - {play_list['title']}\n description: {play_list['description']} \n Create Date: {datetime.datetime.fromtimestamp(play_list['date'])} \n")
    else:
        print("Play lists is empty")


def is_path_valid(path):
    file = Path(path)
    return file.is_file()

def get_audio_data(audio_path):
    audio = TinyTag.get(audio_path)
    return {
        "title": audio.title if audio.title != '' else Path(audio_path).stem,
        "duration": audio.duration,
        "album": audio.album,
        "artist": audio.artist,
    }

def get_music_data_from_user(play_list_id):
    questions = [
        inquirer.Text('path', message='Please enter music path')
    ]
    answer = inquirer.prompt(questions)

    clear_path = answer['path'].replace('"', '')
    clear_path = clear_path.replace('\\', '/')

    if not is_path_valid(clear_path):
        return None

    audio_data = get_audio_data(clear_path)

    music = {
        'id': uuid.uuid4().hex,
        'play_list_id': play_list_id,
        "path": clear_path,
        'create_date': int(datetime.datetime.now().timestamp()),
        'title': audio_data['title'],
        'album': audio_data['album'],
        'artist': audio_data['artist'],
        'duration': audio_data['duration'],
    }

    return music

def get_updated_music_data_from_user():
    questions = [
        inquirer.Text('title', message='Please enter music title'),
        inquirer.Text('artist', message='Please enter music artist'),
        inquirer.Text('album', message='Please enter music album'),
    ]

    answer = inquirer.prompt(questions)
    return answer


def show_music_of_play_list(music_list):
    musics = []
    if len(music_list) == 0:
        print('there is no music!')
    else:
        for (index, music) in enumerate(music_list):
           musics.append((music['title'], music['id']))

    musics.append(('back to play list menu', 'back_to_play_list_menu'))
    musics.append(('exit', 'exit'))

    questions = [
        inquirer.List(
            "paly_list_music_menu",
            message="Select music to play",
            choices= musics,
        ),
    ]

    answers = inquirer.prompt(questions)
    return answers['paly_list_music_menu']

def get_music_title():
    questions = [
        inquirer.Text('title', message='Please enter music title')
    ]
    answer = inquirer.prompt(questions)

    return answer['title']

def show_full_play_list_music_and_get_user_input(music_list):

    if len(music_list) == 0:
        print('there is no play list!!')
    else:
        for (index, music) in enumerate(music_list):
            print(f"{index + 1}: \n   id: {music['id']}\n   title: {music['title']}\n   artist: {music['artist']}\n   create date: {datetime.datetime.fromtimestamp(music['create_date'])}\n")


    mapped_music_list = [('enter music id', 'music_id'), ('back to play list menu', 'back_play_list_menu'), ('exit', 'exit')]

    questions = [
        inquirer.List(
            "music_menu",
            message="Music Menu",
            choices= mapped_music_list,
        ),
    ]

    answers = inquirer.prompt(questions)
    return answers['music_menu']

def get_music_id():
    questions = [
        inquirer.Text('music_id', message='Please enter music id')
    ]
    answer = inquirer.prompt(questions)

    return answer['music_id']