import json
import os
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel as Label
from kivymd.uix.textfield import MDTextField as TextInput
from kivymd.uix.card import MDCard
from kivymd.theming import ThemeManager
from video_processing import check_data
from structures import Video

dir = os.path.dirname(os.path.dirname(__file__))

file_path = os.path.join(dir, 'data-test.json')

def load_videos():
    is_video_recognized = check_data()
    videos = []

    if is_video_recognized:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            i = 1

            for video_data in data:
                video = Video(
                    i,
                    video_data['video'],
                    video_data['fps'],
                    video_data['dimensions'],
                    video_data['duration'],
                    video_data['language'],
                    video_data['keywords'],
                    video_data['thumbnail']
                )
                videos.append(video)
                i += 1

    return videos

class VideoIndexerApp(MDApp):
    def build(self):
        self.theme_cls = ThemeManager()
        self.theme_cls.theme_style = "Dark"

        self.videos = load_videos()

        root = BoxLayout(orientation='vertical', spacing=dp(16), padding=dp(16))

        search_layout = BoxLayout(size_hint_y=None, height=dp(100), orientation='vertical', spacing=dp(8))

        search_input_layout = BoxLayout(size_hint=(1, None), height=dp(40), spacing=dp(16), orientation='vertical')
        self.search_input = TextInput(hint_text="Pesquisar por palavra-chave:", multiline=False, mode="rectangle", size_hint=(1, None))
        search_input_layout.add_widget(self.search_input)

        search_button = MDRaisedButton(text='Pesquisar', on_release=self.search_videos, size_hint=(1, None), height=dp(40))
        search_input_layout.add_widget(search_button)

        search_layout.add_widget(search_input_layout)
        root.add_widget(search_layout)

        self.videos_layout = ScrollView()
        self.videos_grid = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(16))
        self.videos_grid.bind(minimum_height=self.videos_grid.setter('height'))

        self.display_all_videos()

        self.videos_layout.add_widget(self.videos_grid)
        root.add_widget(self.videos_layout)

        return root

    def display_all_videos(self):
        self.videos_grid.clear_widgets()

        for video in self.videos:
            video_layout = MDCard(
                orientation='horizontal',
                size_hint=(1, None),
                size=(dp(800), dp(120)),
                padding=dp(8),
                elevation=2
            )
            
            thumbnail = AsyncImage(
                source=video.thumbnail,
                size_hint=(None, 1),
                size=(dp(120), dp(80)),
                pos_hint={'center_x': 0.3},
                fit_mode="cover"
            )
            video_layout.add_widget(thumbnail)

            info_layout = BoxLayout(orientation='vertical', size_hint_x=None, width=dp(220), padding=dp(16), spacing=dp(2))
            info_layout.add_widget(Label(text=video.name, bold=True))
            info_layout.add_widget(Label(text=f"Duração: {video.duration}"))
            info_layout.add_widget(Label(text=f"Dimensões: {video.dimensions[0]}x{video.dimensions[1]}px"))
            info_layout.add_widget(Label(text=f"Idioma: {video.language.upper()}"))

            video_layout.add_widget(info_layout)
            self.videos_grid.add_widget(video_layout)

    def search_videos(self, instance):
        search_query = self.search_input.text.strip().lower()

        if not search_query:
            self.display_all_videos()
            return

        filtered_videos = [video for video in self.videos if video.search_by_keyword(search_query)]
        self.display_filtered_videos(filtered_videos)

    def display_filtered_videos(self, filtered_videos):
        self.videos_grid.clear_widgets()

        for video in filtered_videos:
            video_layout = MDCard(
                orientation='horizontal',
                size_hint=(1, None),
                size=(dp(800), dp(120)),
                padding=dp(8),
                elevation=2
            )
            
            thumbnail = AsyncImage(
                source=video.thumbnail,
                size_hint=(None, 1),
                size=(dp(120), dp(80)),
                pos_hint={'center_x': 0.3},
                fit_mode="cover"
            )
            video_layout.add_widget(thumbnail)

            info_layout = BoxLayout(orientation='vertical', size_hint_x=None, width=dp(220), padding=dp(16), spacing=dp(2))
            info_layout.add_widget(Label(text=video.name, bold=True))
            info_layout.add_widget(Label(text=f"Duração: {video.duration}"))
            info_layout.add_widget(Label(text=f"Dimensões: {video.dimensions[0]}x{video.dimensions[1]}px"))
            info_layout.add_widget(Label(text=f"Idioma: {video.language.upper()}"))

            video_layout.add_widget(info_layout)
            self.videos_grid.add_widget(video_layout)

if __name__ == '__main__':
    VideoIndexerApp().run()
