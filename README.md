# Desenvolvimento da aplicação da 2ª parte do projeto

**Authors: Francisco Carqueija, Francisco Tavares, Mário Minhava**

## Tema

O trabalho foi desenvolvido no âmbito da cadeira de base de dados. O tema escolhido foram jogos de xadrez do lichess.com, existem vários endpoints, e correlações que seriam necessária para uma boa busca, caso necessária, de jogos, jogadores ou mesmo openings.

### Sumário das principais tags usadas no código da MovieStreamApp

#### Jinja

- `{{ x.attr }}` : expande para valor de atributo  `attr` para variável `x` -  [[ver documentação]](https://jinja.palletsprojects.com/en/3.0.x/templates/#variables) 
- `{% for x in items %} ... {% endfor %}`: iteração `for`sobre lista de valores `items` [[ver documentação]](https://jinja.palletsprojects.com/en/3.0.x/templates/#for)


#### HTML (com apontadores para tutorial W3 Schools)

- `<a href ...>`: [links](https://www.w3schools.com/html/html_links.asp)
- `<table> <th> <tr> <td>`: [formatação de tabelas](https://www.w3schools.com/html/html_tables.asp)
- `<ul>`, `<ol>` `<li>`: [formatação de listas](https://www.w3schools.com/html/html_lists.asp)
- `<h1>, <h2>, ...`: [cabeçalhos de nível 1, 2, ...](https://www.w3schools.com/html/html_headings.asp)
- `<p>`: [parágrafos](https://www.w3schools.com/html/html_paragraphs.asp)
- `<b>, <i>, ...`: [formatação de texto em negrito, itálico, ...](https://www.w3schools.com/html/html_formatting.asp)


## Instalação de software

Precisa de ter o Python 3 e o gestor de pacotes pip instalado.
Experimente executar `python3 --version` e `pip3 --version` para saber
se já estão instalados. Em caso negativo, pode por exemplo em Ubuntu
executar:

```
sudo apt-get install python3 python3-pip
```

Tendo Python 3 e pip instalados, deve instalar a biblioteca `Flask` executando o comando:

```
pip3 install --user Flask
``` 

## Configuração de acesso à BD

Edite o ficheiro `db.py` no que se refere à configuração da sua BD, modificando os parâmetros `DB_FILE` que indique o ficheiro da base de dados. O ficheiro SQLite para a BD deve residir na mesma pasta que o ficheiro `app.py`.

Configurados o parâmetro `DB_FILE`,  teste o acesso executando:

```
python3 test_db_connection.py NOME_DE_UMA_TABELA
```

Se a configuração do acesso à BD estiver correcto, deverá ser listado o conteúdo da tabela `NOME_DE_UMA_TABELA`, por ex. se a BD configurada fosse a dos recintos culturais e quisermos listar a tabela `atividades` obteríamos:

```
$ python3 test_db_connection.py atividades
6 results ...
[('ref', 1), ('atividade', 'cinema')]
[('ref', 2), ('atividade', 'circo')]
[('ref', 3), ('atividade', 'dança')]
[('ref', 4), ('atividade', 'música')]
[('ref', 5), ('atividade', 'tauromaquia')]
[('ref', 6), ('atividade', 'teatro')]
```

## Execução do servidor da aplicação

Depois de configurar a BD como descrito acima, pode agora iniciar o servidor da aplicação executando `python3 server.py`, ex.:

```
$ python3 server.py
2021-05-18 21:40:46 - INFO - Connected to database guest
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server.  Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
2021-12-08 21:40:46 - INFO -  * Running on http://0.0.0.0:9000/ (Press CTRL+C to quit) 
...
```

De seguida abra no seu browser __http://127.0.0.1:9000__ ou __http://localhost:9000__. Deverá ver uma página com uma mensagem __Hello World!__ da forma ilustrada na imagem a seguir.

![](static/app_screenshot.png)



