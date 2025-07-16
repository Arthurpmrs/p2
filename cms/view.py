import os
from typing import Callable, TypedDict

from cms.models import Comment, Post, Site, User, UserRole
from cms.repository import (
    CommentRepository,
    PostRepository,
    SiteRepository,
    UserRepository,
)


MenuOptions = TypedDict(
    "MenuOptions", {"message": str, "function": Callable[..., None]}
)


class Menu:
    logged_user: User | None
    logged_options: list[MenuOptions]
    not_logged_options: list[MenuOptions]

    def __init__(self):
        self.not_logged_options = [
            {"message": "Criar um usuário", "function": self.create_user},
            {"message": "Fazer Login", "function": self.login},
            {"message": "Listar sites", "function": self.show_available_sites},
        ]

        self.logged_options = [
            {"message": "Exibir dados de perfil", "function": self.show_profile},
            {"message": "Criar um site", "function": self.create_site},
            {"message": "Listar sites", "function": self.show_available_sites},
            {"message": "Listar sites do usuário", "function": self.show_user_sites},
            {"message": "Selecionar um site", "function": self.select_site},
            {"message": "Fazer logout", "function": self.logout},
        ]
        self.user_repo = UserRepository()
        self.site_repo = SiteRepository()
        self.post_repo = PostRepository()
        self.comment_repo = CommentRepository()
        self._populate()
        self.logged_user = None
        self.selected_site = None
        self.selected_post = None

    def show(self):
        while True:
            os.system("clear")
            print("CMS\n")

            if self.logged_user:
                print(f"User logged in: {self.logged_user.username}")
                options = self.logged_options
            else:
                options = self.not_logged_options

            for i, option in enumerate(options):
                print(f"{i + 1}. {option['message']}")
            print("0. Sair")

            try:
                selected_option = int(
                    input("Digite o número da opção para selecioná-la: ")
                )
            except ValueError:
                print("Opção inválida.\n")
                continue

            if selected_option == 0:
                break

            if selected_option < 0 or selected_option > len(options):
                print("Opção inválida.\n")
                continue

            os.system("clear")
            options[selected_option - 1]["function"]()
            print(" ")
            input("Clique enter para voltar ao menu.")

    def show_site(self, selected_site: Site):
        if not self.logged_user:
            return

        self.selected_site = selected_site

        options: list[MenuOptions] = [
            {"message": "Listar posts do site", "function": self.show_site_posts},
            {"message": "Selecionar um post", "function": self.select_post},
        ]

        if self.logged_user.username == selected_site.owner.username:
            options.append(
                {"message": "Criar post no site", "function": self.create_site_post},
            )

        while True:
            os.system("clear")
            print(f"Opções para o site '{selected_site.name}'")
            for i, option in enumerate(options):
                print(f"{i + 1}. {option['message']}")
            print("0. Sair")

            try:
                selected_option = int(
                    input("Digite o número da opção para selecioná-la: ")
                )
            except ValueError:
                print("Opção inválida.\n")
                continue

            if selected_option == 0:
                return

            if selected_option < 0 or selected_option > len(options):
                print("Opção inválida.\n")
                continue

            os.system("clear")
            options[selected_option - 1]["function"]()
            print(" ")
            input("Clique enter para voltar ao menu.")

    def show_post(self, selected_post: Post):
        if not self.logged_user:
            return
        self.selected_post = selected_post

        options: list[MenuOptions] = [
            {
                "message": "Listar comentários do post",
                "function": self.show_post_comments,
            },
            {"message": "Comentar no post", "function": self.comment_on_post},
        ]

        while True:
            os.system("clear")
            print(selected_post.title)
            print(f"Data de criação: {selected_post.created_at}")
            print(" ")
            print(selected_post.body)
            print(" ")
            print(f"Criado por: {selected_post.poster.username}")
            print(" ")
            print(" ")

            print("Opções para o post ")
            for i, option in enumerate(options):
                print(f"{i + 1}. {option['message']}")
            print("0. Sair")

            try:
                selected_option = int(
                    input("Digite o número da opção para selecioná-la: ")
                )
            except ValueError:
                print("Opção inválida.\n")
                continue

            if selected_option == 0:
                return

            if selected_option < 0 or selected_option > len(options):
                print("Opção inválida.\n")
                continue

            os.system("clear")
            options[selected_option - 1]["function"]()
            print(" ")
            input("Clique enter para voltar ao menu.")

    def create_user(self):
        first_name = input("Digite seu primeiro nome: ")
        last_name = input("Digite seu último nome: ")
        email = input("Digite seu email: ")
        username = input("Digite um username: ")
        password = input("Digite uma senha: ")

        user = User(first_name, last_name, email, username, password, UserRole.USER)
        self.user_repo.add_user(user)

    def login(self):
        username = input("Username: ")
        password = input("Senha: ")

        try:
            user = self.user_repo.validate_user(username, password)
        except ValueError:
            print("Credenciais Inválidas")
            return

        self.logged_user = user

    def logout(self):
        self.logged_user = None

    def show_profile(self):
        if self.logged_user:
            print(f"Nome: {self.logged_user.first_name} {self.logged_user.last_name}")
            print(f"E-mail: {self.logged_user.email}")
            print(f"Role: {self.logged_user.role}")

    def create_site(self):
        if not self.logged_user:
            print("Usuário não está logado.")
            return

        site_name = input("Diga o nome do seu site: ")
        site = Site(owner=self.logged_user, name=site_name)
        self.site_repo.add_site(site)

    def show_available_sites(self):
        sites: list[Site] = self.site_repo.get_sites()
        for i, site in enumerate(sites):
            print(f"{i + 1}. {site.name}")

    def show_user_sites(self):
        if not self.logged_user:
            return

        user_sites: list[Site] = self.site_repo.get_user_sites(self.logged_user)
        for i, site in enumerate(user_sites):
            print(f"{i + 1}. {site.name}")

    def select_site(self):
        sites: list[Site] = self.site_repo.get_sites()
        for i, site in enumerate(sites):
            print(f"{i + 1}. {site.name}")

        while True:
            try:
                selected_option = int(
                    input("Digite o número do site para selecioná-lo: ")
                )
            except ValueError:
                print("Opção inválida.\n")
                continue

            if selected_option == 0:
                return

            if selected_option < 0 or selected_option > len(sites):
                print("Opção inválida.\n")
                continue

            self.show_site(sites[selected_option - 1])

    def create_site_post(self):
        if not self.selected_site:
            return

        title = input("Digite o título do post: ")
        body = input("Digite o conteúdo do post: ")

        post = Post(
            poster=self.selected_site.owner,
            site=self.selected_site,
            title=title,
            body=body,
        )
        self.post_repo.add_post(post)

    def show_site_posts(self):
        if not self.selected_site:
            return

        posts: list[Post] = self.post_repo.get_site_posts(self.selected_site)
        for i, post in enumerate(posts):
            print(f"{i + 1}. {post.title}")

    def select_post(self):
        if not self.selected_site:
            return

        posts: list[Post] = self.post_repo.get_site_posts(self.selected_site)
        for i, post in enumerate(posts):
            print(f"{i + 1}. {post.title}")

        while True:
            try:
                selected_option = int(
                    input("Digite o número do site para selecioná-lo: ")
                )
            except ValueError:
                print("Opção inválida.\n")
                continue

            if selected_option == 0:
                return

            if selected_option < 0 or selected_option > len(posts):
                print("Opção inválida.\n")
                continue

            self.show_post(posts[selected_option - 1])

    def comment_on_post(self):
        if not self.selected_post or not self.logged_user:
            return

        body = input("Digite seu comentário: ")

        comment = Comment(
            post=self.selected_post, commenter=self.logged_user, body=body
        )
        self.comment_repo.add_comment(comment)

    def show_post_comments(self):
        if not self.selected_post:
            return

        post_comments: list[Comment] = self.comment_repo.get_post_comments(
            self.selected_post
        )

        for comment in post_comments:
            print(comment.body)
            print(f"{comment.commenter.username} @ {comment.created_at}")
            print(" ")

    def _populate(self):
        admin = User(
            first_name="Admin",
            last_name="Admin",
            email="admin@admin.com",
            username="admin",
            password="Admin123",
            role=UserRole.ADMIN,
        )
        self.user_repo.add_user(admin)
        user1 = User(
            first_name="User1",
            last_name="User1",
            email="user1@user.com",
            username="user1",
            password="User123",
            role=UserRole.USER,
        )
        self.user_repo.add_user(user1)
        user2 = User(
            first_name="User2",
            last_name="User2",
            email="user2@user.com",
            username="user2",
            password="User123",
            role=UserRole.USER,
        )
        self.user_repo.add_user(user2)
        site = Site(owner=admin, name="Meu blog")
        self.site_repo.add_site(site)

        post1 = Post(
            poster=admin,
            site=site,
            title="Título do meu post",
            body="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
        )
        post2 = Post(
            poster=admin,
            site=site,
            title="Título do meu segundo post",
            body="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
        )
        self.post_repo.add_post(post1)
        self.post_repo.add_post(post2)

        comment1_post1 = Comment(post=post1, commenter=user1, body="Nice post bro.")
        comment2_post1 = Comment(post=post1, commenter=user2, body="Thanks!")
        comment3_post1 = Comment(post=post1, commenter=user2, body="A second comment!")
        self.comment_repo.add_comment(comment1_post1)
        self.comment_repo.add_comment(comment2_post1)
        self.comment_repo.add_comment(comment3_post1)
