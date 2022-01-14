# Desafio de Programação do PubFuture

### Desenvolvido por Victor William Hostert
<br>

---
## 🧪 Tecnologias utilizadas no projeto

Esse projeto foi desenvolvido com as seguintes tecnologias:

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [HTML](https://developer.mozilla.org/pt-BR/docs/Web/HTML)
- [CSS](https://developer.mozilla.org/pt-BR/docs/Web/CSS)

## ❓ O que é este projeto?

Este projeto é baseado neste [desafio de programação](https://www.proway.com.br/desafiopubfuture), onde deve-se criar um aplicativo para gerenciar finanças pessoais

## 🚀 Como executar

O primeiro passo é possuir o Git instalado em seu computador. Caso não possua, pode baixá-lo [por aqui](https://git-scm.com/downloads). Para verificar se possui o git instalado, abra um terminal e execute o comando:

```bash
$ git --version # Caso possua git instalado, aparecerá na tela o número da versão
```

Clone o projeto utilizando a url HTTPS, em uma pasta de sua preferência, clicando em clone na [página do repositório do projeto](https://github.com/victorhostert/DesafioPubFuture), selecionando a opção para copiar o repositório por HTTPS, copiando a url e utilizando o seguinte comando:

```bash
$ git clone <URL HTTPS>
```

Alternativamente, pode-se usar apenas baixar o repositório em .zip

Após clonar o repositório e acessar o diretório, o repositório já deve estar na sua máquina.

Tendo o repositório em seu ambiente local, garanta que possui o [PIP (instalador de bibliotecas do Python)](https://pip.pypa.io/en/stable/installation/) funcionando, e instale as bibliotecas e frameworks especificadas em ```requirements.txt```

Agora para acessar de fato o site, como o material ainda está disponível apenas em ambiente de produção, deve-se realizar os seguintes comandos em um terminal:

```bash
$ python manage.py migrate # Realiza as migrações, para fazer o arquivo do banco de dados
$ python manage.py runserver # Sobe um servidor local na porta 8000
```

Se tudo der certo, ao acessar [esta url](http://localhost:8000) você deve de ver o servidor funcionando

