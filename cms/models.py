from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class UserRole(Enum):
    ADMIN = 1
    USER = 2


@dataclass
class User:
    id: int = field(init=False)
    first_name: str
    last_name: str
    email: str
    username: str
    password: str
    role: UserRole


@dataclass
class Site:
    id: int = field(init=False)
    owner: User
    name: str


@dataclass
class Post:
    id: int = field(init=False)
    poster: User
    site: Site
    title: str
    body: str
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Comment:
    id: int = field(init=False)
    post: Post
    commenter: User
    body: str
    created_at: datetime = field(default_factory=datetime.now)
