from atproto import Client
from typing import List, Optional

class BlueskyClient:
    def __init__(self, identifier: str, app_password: str):
        self.identifier = identifier
        self.app_password = app_password
        self.client = Client()
        self._logged_in = False

    def login(self):
        if not self._logged_in:
            self.client.login(self.identifier, self.app_password)
            self._logged_in = True

    def get_latest_posts(self, actor: str, limit: int = 5) -> List[str]:
        self.login()
        actor = actor.lstrip("@")
        try:
            feed = self.client.app.bsky.feed.get_author_feed({"actor": actor, "limit": limit})
            return [post.post.uri for post in feed.feed if post.post]
        except Exception:
            return []

    def get_likers(self, post_uri: str) -> List[str]:
        self.login()
        likes = self.client.app.bsky.feed.get_likes({"uri": post_uri})
        return [like.actor.handle for like in likes.likes]

    def follow_user(self, handle: str) -> Optional[str]:
        self.login()
        try:
            return self.client.follow(handle)
        except Exception:
            return None

    def get_following(self) -> List[str]:
        self.login()
        result = self.client.app.bsky.graph.getFollowing({'actor': self.client.me.did})
        return [entry.handle for entry in result.following]
