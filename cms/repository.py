from datetime import datetime
from itertools import count
from cms.models import Comment, Media, Post, Site, User


class UserRepository:
    users: dict[int, User] = {}
    id_counter = count(1)

    def add_user(self, user: User) -> int:
        user_id = next(self.id_counter)
        user.id = user_id
        self.users.update({user_id: user})
        return user_id

    def validate_user(self, username: str, password: str) -> User:
        selected_user = None
        for user in self.users.values():
            if user.username == username:
                selected_user = user
                break

        if not selected_user:
            raise ValueError("Credenciais inválidas.")

        if selected_user.password != password:
            raise ValueError("Credenciais inválidas.")

        return selected_user

    def delete_user(self, user_id: int):
        self.users.pop(user_id)


class SiteRepository:
    sites: dict[int, Site] = {}
    id_counter = count(1)

    def add_site(self, site: Site) -> int:
        site_id = next(self.id_counter)
        site.id = site_id
        self.sites.update({site_id: site})
        return site_id

    def get_sites(self) -> list[Site]:
        return [site for site in self.sites.values()]

    def get_user_sites(self, user: User) -> list[Site]:
        return [site for site in self.sites.values() if site.owner.id == user.id]


class PostRepository:
    posts: dict[int, Post] = {}
    id_counter = count(1)

    def add_post(self, post: Post) -> int:
        post_id = next(self.id_counter)
        post.id = post_id
        self.posts.update({post_id: post})
        return post_id

    def get_site_posts(self, site: Site) -> list[Post]:
        posts: list[Post] = []
        now = datetime.now()
        for post in self.posts.values():
            if post.site.id == site.id and post.scheduled_to < now:
                posts.append(post)

        return posts


class CommentRepository:
    comments: dict[int, Comment] = {}
    id_counter = count(1)

    def add_comment(self, comment: Comment) -> int:
        comment_id = next(self.id_counter)
        comment.id = comment_id
        self.comments.update({comment_id: comment})
        return comment_id

    def get_post_comments(self, post: Post) -> list[Comment]:
        return [
            comment for comment in self.comments.values() if comment.post.id == post.id
        ]


class MediaRepository:
    medias: dict[int, Media] = {}
    id_counter = count(1)

    def add_midia(self, media: Media) -> int:
        media_id = next(self.id_counter)
        media.id = media_id
        self.medias.update({media_id: media})
        return media_id

    def get_site_medias(self, site: Site) -> list[Media]:
        return [media for media in self.medias.values() if media.site.id == site.id]

    def remove_media(self, media_id: int):
        self.medias.pop(media_id, None)
