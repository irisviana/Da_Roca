![Cabeçalho do Da Roça](https://github.com/irisviana/Da_Roca/blob/main/artefatos/wiki-header.png)
Uma plataforma fácil e intuitiva de usar até para os mais leigos, onde os produtores poderão co
mercializar seus produtos, recebendo pedidos de clientes da região e realizando a entrega deles.
Já os clientes dos produtos poderão acessar a vitrine de produtos disponíveis, pesquisar por
produtos, realizar a compra e aguardar receber sem sair de casa.

[![Build Status](https://app.travis-ci.com/irisviana/Da_Roca.svg?branch=main)](https://app.travis-ci.com/irisviana/Da_Roca)

## Equipe
- [Amanda Colatino](https://github.com/amandacl)
- [Íris Viana](https://github.com/irisviana)
- [Matheus Noronha](https://github.com/matheusnoronha)
- [Raquel Vieira](https://github.com/RaquelVieiraa)
- [Vinícius Santos](https://github.com/vinesnts)

> Acesse a nossa [Wiki](https://github.com/irisviana/Da_Roca/wiki) para mais informações e detalhes do projeto.

## Como testar o DaRoça na sua máquina?
O DaRoça é desenvolvido utilizando o framework Django, que utiliza a linguagem de programação
a linguagem de programação Python, além disso, o banco de dados usado no desenvolvimento é o
pgSQL, mas você pode usar o banco que desejar. Sabendo disso, é necessário ter as seguintes 
tecnologias instaladas na máquina:
- Python3
- pgSQL (Opcional)

Após instalar as tecnologias acima e clonar o projeto para a sua máquina, siga os passos abaixo pa
ra configurar o projeto no seu ambiente:
1- A partir do diretório do projeto, abra o terminal na pasta e navegue até a pasta `projeto_da_roca`:
```sh
cd projeto_da_roca/
```
2- Crie o ambiente virtual para o projeto:
```sh
python -m venv env/
```
3- Selecione o ambiente virtual criado:
No Linux:
```sh
source env/bin/activate
```
No Windows:
```sh
{caminho_do_projeto}\projeto_da_roca\env\Scripts\Activate
```
4- Instale as dependencias do projeto:
```sh
pip install -r requirements.txt
```
5- Copie o arquivo `.env.example` para um arquivo chamada `.env`.
6- Abra o arquivo `.env` e preencha as informações de conexão ao banco de dados local.
7- Rode as migrações para que as tabelas sejam geradas no banco:
```sh
python manage.py migrate
```
8- E por último, rode o projeto:
```sh
python manage.py runserver
```
9- Abra o navegador no link indicado no console.

## Como rodar os testes?
Para rodar os testes de unidade do projeto é necessário apenas rodar o comando abaixo:
```sh
python manage.py test tests
```

> Projeto desenvolvido na disciplina de Projetão 2020.1
> Universidade Federal do Agreste de Pernambuco

![Rodapé do Da Roça](https://github.com/irisviana/Da_Roca/blob/main/artefatos/wiki-footer.png)
