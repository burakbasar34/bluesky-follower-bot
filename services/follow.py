from core.bluesky_client import BlueskyClient
from models import FollowLog
from sqlalchemy.orm import Session
import time

def follow_likers(db: Session, user, delay: int = 5) -> int:
    client = BlueskyClient(user.username, user.app_password)
    client.login()

    followed_count = 0
    target_users = user.targets

    for target in target_users:
        try:
            posts = client.get_latest_posts(target.handle, limit=5)
            for post_uri in posts:
                likers = client.get_likers(post_uri)
                for liker in likers:
                    if liker == user.username:
                        continue
                    if liker not in client.getFollowing():
                        result = client.follow_user(liker)
                        if result:
                            db.add(FollowLog(user_id=user.id, message=f"{liker} takip edildi."))
                            db.commit()
                            followed_count += 1
                            time.sleep(delay)
        except Exception as e:
            db.add(FollowLog(user_id=user.id, message=f"{target.handle} için hata: {e}"))
            db.commit()
            continue

    return followed_count
