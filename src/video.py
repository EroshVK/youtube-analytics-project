from src.channel import Channel


class Video:
    video_id = None
    title = None
    url = None
    view_count = None
    like_count = None

    def __init__(self, video_id):
        """Экземпляр инициализируется id видео."""
        self.video_id = video_id

        try:
            channel_data: dict = self.get_video_data()

            self.title: str = channel_data['items'][0]['snippet']['title']
            self.url: str = str("https://youtu.be/" + video_id)
            self.view_count: int = channel_data['items'][0]['statistics']['viewCount']
            self.like_count: int = channel_data['items'][0]['statistics']['likeCount']
        except VideoNotFound:
            VideoNotFound('Видео не найдено')

    def __str__(self):
        """Метод для отображения информации об объекте класса для пользователей."""
        return f"{self.title}"

    def get_video_data(self):
        """Получает данные о видео"""
        return Channel.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                   id=self.video_id
                                                   ).execute()


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        """Экземпляр инициализируется id плейлиста."""
        super().__init__(video_id)

        self.playlist_id = playlist_id


class VideoNotFound(Exception):
    """
    Базовый класс исключения VideoNotFound
    """
    pass
