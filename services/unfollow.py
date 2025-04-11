from atproto import Client
from database import SessionLocal
from models import User
from atproto.exceptions import AtProtocolException


def unfollow_nonfollowers(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return "Kullanıcı bulunamadı."

    client = Client()
    try:
        client.login(user.username, user.app_password)
    except AtProtocolException as e:
        return f"Giriş hatası: {str(e)}"

    # Takip edilen kullanıcıları al
    try:
        following_resp = client.app.bsky.graph.getFollowing({'actor': user.username, 'limit': 100})
        following_list = following_resp['follows']
    except Exception as e:
        return f"Takip edilenler alınamadı: {str(e)}"

    # Takipçileri al
    try:
        followers_resp = client.app.bsky.graph.getFollowers({'actor': user.username, 'limit': 100})
        followers_list = [f['did'] for f in followers_resp['followers']]
    except Exception as e:
        return f"Takipçiler alınamadı: {str(e)}"

    # Takip etmeyenleri unfollow et
    unfollowed = []
    for follow in following_list:
        did = follow['did']
        if did not in followers_list:
            try:
                client.app.bsky.graph.unfollow(follow['uri'])
                unfollowed.append(follow['handle'])
            except Exception as e:
                continue

    return f"Unfollow edilen kullanıcılar: {', '.join(unfollowed)}" if unfollowed else "Unfollow edilecek kullanıcı yok."
