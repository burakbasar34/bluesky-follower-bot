from atproto import Client

class BlueskyClient:
    def __init__(self, identifier: str, password: str):
        self.client = Client()
        self.client.login(identifier, password)

    def get_likers(self, post_uri):
        return self.client.feed.getLikes({'uri': post_uri})

    def get_following(self, handle):
        return self.client.graph.getFollowing({'actor': handle})
