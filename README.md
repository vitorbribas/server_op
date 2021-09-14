# server_op

Repositorio destinado ao processamento de dados obtidos a partir da ferramenta feature-trace. 

Para executar o servidor, basta executar:

pip install -r requirements.txt

### Testes:
Para executar os testes em conjunto com o output de cobertura, use o comando:
```shell
pytest --cov
```

Para visualizar a cobertura dos testes em uma página HTML, execute:
```shell
pytest --cov-report=html
```
E abra o arquivo index.html do diretório `htmlcov`