from src.channel import Channel


class Video:
    def __init__(self, video_id):
        """��������� ���������������� id �����."""
        self.video_id = video_id

        channel_data: dict = self.get_video_data()

        self.title: str = channel_data['items'][0]['snippet']['title']
        self.url: str = str("https://youtu.be/" + video_id)
        self.view_count: int = channel_data['items'][0]['statistics']['viewCount']
        self.like_count: int = channel_data['items'][0]['statistics']['likeCount']

    def __str__(self):
        """����� ��� ����������� ���������� �� ������� ������ ��� �������������."""
        return f"{self.title}"

    def get_video_data(self):
        """�������� ������ � �����"""
        return Channel.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                   id=self.video_id
                                                   ).execute()


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        """��������� ���������������� id ���������."""
        super().__init__(video_id)

        self.playlist_id = playlist_id
