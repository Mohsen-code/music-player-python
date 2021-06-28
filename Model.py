import json

FILE_NAME = "play_lists.json"
MUSIC_FILE_NAME = "music_of_play_lists.json"


def get_play_lists():
    play_lists_json_content = []

    try:
        play_lists_content = open(FILE_NAME, "r")
        play_lists_json_content = json.loads(play_lists_content.read())
    except Exception:
        file = open(FILE_NAME, "w")
        file.write("[]")
        file.close()

    return play_lists_json_content


def is_play_list_exist(play_list_id):
    play_lists = get_play_lists()
    for (index, play_list) in enumerate(play_lists):
        if play_list['id'] == play_list_id:
            return True
    
    return False

def add_play_list(play_list_object):
    play_lists = get_play_lists()
    play_lists.append(play_list_object)
    file = open(FILE_NAME, "w")
    file.write(json.dumps(play_lists))
    file.close()


def get_play_list_by_title(title):
    play_lists = get_play_lists()
    filtered_play_lists = list(filter(lambda paly_list: paly_list['title'] == title, play_lists))
    return filtered_play_lists


def update_play_list(updated_play_list):
    play_lists = get_play_lists()

    play_list_index = None

    for (index, play_list) in enumerate(play_lists):
        if play_list['id'] == updated_play_list['id']:
            play_list_index = index
            break

    if play_list_index == None:
        return False

    play_lists[play_list_index] = updated_play_list

    file = open(FILE_NAME, "w")
    file.write(json.dumps(play_lists))
    file.close()
    return True


def remove_play_list(play_list_id):
    if is_play_list_exist(play_list_id):
        play_lists = get_play_lists()
        filtered_play_list = list(filter(lambda play_list: play_list['id'] != play_list_id, play_lists))
        file = open(FILE_NAME, "w")
        file.write(json.dumps(filtered_play_list))
        file.close()
        return True
    
    return False

def get_music_of_play_list(play_list_id):
    if is_play_list_exist(play_list_id):
        music_json_content = []
        try:
            music_content = open(MUSIC_FILE_NAME, "r")
            music_json_content = json.loads(music_content.read())
        except Exception:
            file = open(MUSIC_FILE_NAME, "w")
            file.write("[]")
            file.close()
        return music_json_content
        
    return None

def add_music_to_play_list(play_list_id, music_data):
    musics = get_music_of_play_list(play_list_id)
    if musics != None:
        musics.append(music_data)
        file = open(MUSIC_FILE_NAME, "w")
        file.write(json.dumps(musics))
        file.close()
        return True
    
    return False


def get_music_base_on_title(play_list_id, title):
    musics = get_music_of_play_list(play_list_id)
    filtered_musics = []
    if musics != None:
        filtered_musics = list(filter(lambda music: music['title'] == title, musics))
    
    return filtered_musics

def update_music(play_list_id, music_data):
    musics = get_music_of_play_list(play_list_id)
    if musics != None:
        music_index = None
        for (index, music) in enumerate(musics): 
            if music['id'] == music_data['id']:
                music_index = index
                break
        
        musics[music_index] = music_data
        file = open(MUSIC_FILE_NAME, "w")
        file.write(json.dumps(musics))
        file.close()
        return True
    
    return False

def remove_music(play_list_id, music_id):
    musics = get_music_of_play_list(play_list_id)
    if musics != None:
        filtered_musics = list(filter(lambda music: music['id'] != music_id, musics))
        file = open(MUSIC_FILE_NAME, "w")
        file.write(json.dumps(filtered_musics))
        file.close()
        return True
    
    return False
