import datetime

import isodate

from src.channel import Channel


class PlayList:
    def __init__(self, playlist_id):
        """Экземпляр инициализируется id плейлиста."""
        self.playlist_id = playlist_id
        self.title = self.get_playlist_title()
        self.url = "https://www.youtube.com/playlist?list=" + playlist_id

    def get_playlist_title(self) -> str:
        """
        Функция получения названия плейлиста
        """
        channel_id: str = self.get_playlist_data()["items"][0]["snippet"]["channelId"]
        channel_playlists_data: dict = Channel.get_service().playlists().list(channelId=channel_id,
                                                                        part='contentDetails,snippet',
                                                                        maxResults=50,
                                                                        ).execute()
        for playlist in channel_playlists_data["items"]:
            if self.playlist_id == playlist["id"]:
                playlist_title = playlist["snippet"]["title"]
                return playlist_title

    def get_playlist_data(self) -> dict:
        """
        Метод получения данных плейлиста
        """
        youtube: object = Channel.get_service()
        playlist_data: dict = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                     part='contentDetails, id, snippet, status',
                                                     maxResults=50,
                                                     ).execute()
        return playlist_data

    def get_video_ids(self) -> list:
        """
        Метод получения списка id видео в плейлисте
        """
        videos: dict = self.get_playlist_data()
        video_ids: list[str] = []
        for video in videos['items']:
            video_ids.append(video['contentDetails']['videoId'])

        return video_ids

    def get_videos_from_playlist(self) -> dict:
        """
        Метод получения данных о видео в плейлисте
        """
        video_ids: list[str] = self.get_video_ids()
        youtube: object = Channel.get_service()
        videos_in_playlist: dict = youtube.videos().list(part='contentDetails,statistics',
                                                   id=','.join(video_ids)
                                                   ).execute()
        return videos_in_playlist

    def get_videos_duration(self) -> list:
        """
        Метод получения длины каждого видео из плейлиста
        """
        videos_duration: list = self.get_videos_from_playlist()["items"]
        video_duration_list = []
        for video in videos_duration:
            iso_8601_duration = video['contentDetails']['duration']
            video_duration_list.append(isodate.parse_duration(iso_8601_duration))
        return video_duration_list

    @property
    def total_duration(self) -> object:
        """
        Метод получения общей длины всех видео в плейлисте

        """
        total_duration: object = sum(self.get_videos_duration(), datetime.timedelta())
        return total_duration

    def show_best_video(self) -> str:
        """
        Метод получения ссылки на видео с наибольшим кол-вом лайков в плейлисте
        """
        playlist_videos: dict = self.get_videos_from_playlist()
        most_liked_video = 0

        for video in playlist_videos["items"]:
            if most_liked_video < int(video["statistics"]["likeCount"]):
                most_liked_video = int(video["statistics"]["likeCount"])
                most_liked_video_id = video["id"]

        return f"https://youtu.be/{most_liked_video_id}"