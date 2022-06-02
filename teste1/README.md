# Funcionamento
Bash script que instancia um ambiente com SQLserver, cria a amostra necessária no banco de dados e providencia um ambiente python com as dependências necessárias para rodar o script que calcula o lucro total da empresa.

- O comando build instancia a imagem que cria todo o ambiente.
- O comando create-sample utiliza o ```sqlcmd``` do SQLserver dentro do container para rodar a query que cria a amostra.
- O comando get-profit roda o script python compute_profit que utiliza o SQLalchemy como ORM manager para rodar a query compute_profit.sql, que retorna o lucro total por cliente. O script imprime o resultado na shell e retorna um csv que é enviado para o ambiente local do usuário através do bash chamado no comando get-profit.

# Como reproduzir
- Instalações necessárias:
    - Docker
    - Docker-compose

Rode os seguintes comandos:

```./docker-compute build```

```./docker-compute create-sample```

```./docker-compute get-profit```

O container irá retornar o ganho total da empresa para os clientes da amostra no shell e salvará um arquivo nomeado results.csv com estes resultados na pasta principal que rodou o docker-compute.

# Hipóteses e escolha de arquitetura
Quanto as hipóteses do SQL, levou-se em consideração que valores *null* nos campos de desconto podem ser interpretados como 0. Além disso, levou-se em consideração que o campo cliente_id pode ser interpretado como uma PK que está bem dimensionada entre as tabelas cliente e contrato, por isso foi escolhido o uso de um inner join entre as mesmas.

Quanto a escolha da arquitetura, escolheu-se um docker que pode ser fácilmente reproduzido e instanciado em recursos AWS como o EC2. Além disso, foi utilizado o ORM SQLalchemy para melhorar a segurança da conexão com o DB e flexibilizar o uso de conexões diferentes.

Foi feita a escolha de retornar um .CSV pois este tipo de dado costuma ser utilizado por analistas financeiros em planilhas para balizar decisões ou demonstrativos da empresa.


# Prós e contras
- Prós:
    - Portabilidade e fácil reprodução;
    - Facilidade de retorno de dados utilizados por analistas financeiros.

- Contras:
    - Baixa segurança do container, que está longe de ser adequado para produção;
    - Baixa segurança da conexão, que instancia o usuário e senha *hardcoded* no bash script;
    - Dificuldade de uso por pessoas com pouca habilidade técnica (docker);
    - Pode não ser adequado para *compliance*, pois retorna um conjunto de dados para o ambiente local do usuário.

# Melhorias sugeridas
Esta aplicação deveria ser escrita em uma Lambda, onde a requisição de conexão com o banco de dados pode ser feita dentro de uma VPN e com as credenciais gerenciadas pelo serviço Secret Manager da AWS. 

Além disso, utilizar um ambiente Lambda resolve os problemas de segurança do container e permite uma maior facilidade de integração com outros serviços, como um webserver (ex: django dentro de uma ec2) onde o analista entra por meio de uma vpc e faz a requisição para a lambda de forma simples, por intermédio de botões que criam o payload para a Lambda.

Por fim, o SQLAlchemy pode ser melhor utilizado se a requisição não for feita por um RAW sql, mas pelo uso da capacidade do ORM de abstrair o DB como classes e objetos. Desta forma, fica mais flexível e mais fácil retornar resultados adequados para as regras de negócio, como o lucro de um único cliente em específico.