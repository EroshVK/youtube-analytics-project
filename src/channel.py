import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

        channel_data = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()

        self.__channel_id = channel_data["items"][0]["id"]
        self.title = channel_data["items"][0]["snippet"]["title"]
        self.description = channel_data["items"][0]["snippet"]["description"]
        self.url = f"https://www.youtube.com/channel/{channel_id}"
        self.subscribers_count = int(channel_data["items"][0]["statistics"]["subscriberCount"])
        self.video_count = int(channel_data["items"][0]["statistics"]["videoCount"])
        self.view_count = int(channel_data["items"][0]["statistics"]["viewCount"])

    def __str__(self) -> str:
        """
        Метод для отображения информации об объекте класса для пользователей
        """
        return f"{self.title} ({self.url})"

    def __add__(self, other) -> int:
        """
        Метод для сложения количества подписчиков двух экземпляров класса
        """
        return self.subscribers_count + other.subscribers_count

    def __sub__(self, other) -> int:
        """
        Метод для вычитания количества подписчиков двух экземпляров класса
        """
        return self.subscribers_count - other.subscribers_count

    def __gt__(self, other) -> bool:
        """
        Метод для сравнения (>) количества подписчиков двух экземпляров класса
        """
        return self.subscribers_count > other.subscribers_count

    def __ge__(self, other) -> bool:
        """
        Метод для сравнения (>=) количества подписчиков двух экземпляров класса
        """
        return self.subscribers_count >= other.subscribers_count

    def __lt__(self, other) -> bool:
        """
        Метод для сравнения (<) количества подписчиков двух экземпляров класса
        """
        return self.subscribers_count < other.subscribers_count

    def __le__(self, other) -> bool:
        """
        Метод для сравнения (<=) количества подписчиков двух экземпляров класса
        """
        return self.subscribers_count <= other.subscribers_count

    def __eq__(self, other) -> bool:
        """
        Метод для сравнения (=) количества подписчиков двух экземпляров класса
        """
        return self.subscribers_count == other.subscribers_count

    @property
    def channel_id(self) -> str:
        """
        Возвращает id канала
        """
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API.
        """
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, file_name) -> None:
        """Сохраняет данные о канале в файл json"""
        json_data = {
            "channel_id": self.__channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscribers_count": self.subscribers_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }
        with open(file_name, "w") as file:
            json.dump(json_data, file, indent=2, ensure_ascii=False)
