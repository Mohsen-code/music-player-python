import Model
import View

invalid_code_status = 9

View.invalid_code_status = invalid_code_status


def is_music_file_valid(music_name):
    return music_name.lower().endswith(('.mp3', '.wav'))


def run():
    user_input = None
    section = 'main_menu'
    selected_play_list_id = None
    while user_input != 0:

        if section == 'main_menu':
            user_input = View.show_main_menu_and_get_user_input()

            if user_input == 1 :
                selected_play_list_id = View.show_play_lists_menu_and_get_user_input(Model.get_play_lists())
                section = 'play_list_menu'
            
            if user_input == 2:
                play_list = View.get_play_list_data_from_user()
                Model.add_play_list(play_list)
                print('play list added successfully.')
            
            if user_input == 3:
                play_list_title = View.get_play_list_title()
                play_lists = Model.get_play_list_by_title(play_list_title)
                View.show_full_play_lists_menu_and_get_user_input(play_lists)
                play_list_id = View.get_play_list_id()
                play_list = View.get_play_list_data_from_user()
                play_list['id'] = play_list_id
                if Model.update_play_list(play_list):
                    print('play list updated successfully.')
                else:
                    print('error occurred in update play list!')

            if user_input == 4:
                play_list_title = View.get_play_list_title()
                play_lists = Model.get_play_list_by_title(play_list_title)
                View.show_full_play_lists_menu_and_get_user_input(play_lists)
                play_list_id = View.get_play_list_id()
                if Model.remove_play_list(play_list_id):
                    print('play list removed successfully.')
                else:
                    print('error occurred in remove play list!')

        elif section == 'play_list_menu' and selected_play_list_id != None:
            user_input = View.show_play_list_menu_and_get_user_input()
            if user_input == 1:
                music_list = View.show_music_of_play_list(Model.get_music_of_play_list(selected_play_list_id))

            if user_input == 2:
                music_data = View.get_music_data_from_user(selected_play_list_id)
                if Model.add_music_to_play_list(selected_play_list_id, music_data):
                    print("music added successfully.")
                else:
                    print("error occurred in add music!")

            if user_input == 3:
                # edit music
                music_title = View.get_music_title()
                musics = Model.get_music_by_title(selected_play_list_id, music_title)
                answer = View.show_full_play_list_music_and_get_user_input(musics)
                if answer == 'music_id':
                    music_id = View.get_music_id()
                    music_data = View.get_updated_music_data_from_user()
                    music = Model.get_music_by_id(selected_play_list_id, music_id)
                    music['title'] = music_data['title']
                    music['artist'] = music_data['artist']
                    music['album'] = music_data['album']
                    if Model.update_music(selected_play_list_id, music):
                        print('music updated successfully.')
                    else:
                        print('error eccurred in update music!')

            if user_input == 4:
                # remove music
                pass

            if user_input == 5:
                # play musics in order
                pass

            if user_input == 6:
                # play music shuffel
                pass