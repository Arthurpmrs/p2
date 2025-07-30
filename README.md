# Content Management System
Trata-se de um sistema de linha de comando em que o usuário pode criar e gerenciar sites de conteúdo. Em cada Site podem ser publicados (ou agendados) Posts. Em cada Post, pode-se fazer comentários. Cada Site também conta com uma biblioteca de Mídias que podem ser usadas para construção dos Posts. 

## Como executar
```python
python main.py
```

## Funcionalidades implementadas até o dia 26/07/2025
- [x] User Roles and Permissions
- [x] Content Creation and Editing
- [x] Comment and Review System
- [x] Media Library Management
- [x] Content Scheduling
- [x] Analytics and Reporting
- [x] Template and Design Customization
- [x] SEO Optimization Tools
- [x] Multi-Language Support
- [x] Social Media Integration

## Descrição das funcionalidades
As funcionalidades são apresentadas em mais detalhes abaixo, em função da lista de requisitos especificada.

- User Roles and Permissions
    - É possível criar um usuário, fazer login e fazer logout.
    - Usuários de diferentes Roles tem acesso a funcionalidades diferentes. Por exemplo, o usuário que é owner de um Site pode criar um Post e ver estatísticas ou um usuário admin pode ver os logs do sistema.
- Content Creation and Editing
    - O usuário dono do Site pode criar Post em seu Site. 
    - Cada Post é uma sequência de blocos de Texto ou Mídia, formando seu conteúdo.
- Comment and Review System
    - Todos os usuários podem deixar comentários em um Post.
    - Todos os usuários podem visualizar os comentários de um Post.
- Media Library Management
    - Um Site tem associado a ele uma biblioteca de Mídias (imagens e vídeos).
    - O usuário dono do Site pode fazer "upload" de mídias para a biblioteca e essas mídias podem ser incluídas em um Post.
- Content Scheduling
    - Ao criar um Post, o dono do Site tem a opção de agendar um Post para exibição.
    - Um post agendado (cuja data alvo ainda não chegou) não aparece na listagem de Posts do Site.
- Analytics and Reporting
    - É possível ver estatísticas de acesso e interação para um Site (apenas o dono pode ver), que incluem número de acessos, número de mídias importadas, número de posts criados.
    - É possível ver estatísticas de cada Post (apenas o dono pode ver), que incluem número de visualizações, número de comentários e número de compartilhamentos.
    - Também é possível ver os logs de ações no sistema (apenas admin).
- Template and Design Customization
    - É possível alterar o layout inicial da menu do site. As opções incluem: mostrar os posts mais recentes, os posts mais comentados, os posts mais vistos ou imagens dos posts mais recentes (modo galeria).
- SEO Optimization Tools
    - Foi incluída uma ferramenta de análise de SEO para verificação dos Posts. A ferramenta leva em consideração o tamanho do título (recomendado menos de 60 caracteres), número total de palavras (recomendado mais que 300 palavras), contagem de palavras (mostra quais as palavras mais relevantes do texto) e a presença de texto alternativo nas mídias.
- Multi-Language Support
    - O usuário dono do Site tem a opção de escolher a linguagem em que o Post será escrita.
    - O usuário dono do Site pode adicionar uma tradução a um Post existente.
    - Todos os usuários podem alterar qual o idioma de visualização do Post, caso exista mais de um.
- Social Media Integration
    - Todos os usuários podem "compartilhar" um Post em redes sociais (Twitter, Facebook, Instagram, Linkedin).
    - Ao compartilhar, uma versão resumida do post é gerada com um link para leitura completa no site. 