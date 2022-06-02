# Funcionamento
O Bash script "docker-aws-glue" instancia um container com ambiente GLUE, através de uma imagem providenciada pelo AWS em seu DockerHub.

A ambiente GLUE contém os seguintes notebooks:
- total_liquido_auto_generated
- total_liquido_s3

Cada notebook contém métodos spark diferentes para atingir o objetivo do teste:

- O primeiro notebook implementa a construção de um spark dataframe através do documento JSON contido na pasta data.
São utilizados os métodos próprios do dataframe e do pyspark para transformar os dados no total_liquido pedido no teste.

- O segundo notebook faz uma conexão com um bucket pessoal do S3 através do GLUE que contém o mesmo documento JSON, que é deserializado em um spark dataframe. É usado o spark sql para fazer uma query neste dataframe e retornar o total líquido pedido no teste.

# Como reproduzir
- Instalações necessárias:
    - AWS-CLI
    - Docker
    - Docker-compose

Rode os seguintes comandos:

```./docker-aws-glue pull```

```./docker-aws-glue run```

Abra uma página com o seguinte endereço: ```localhost:8888```

Escolha o notebook desejado e rode o código.
No notebook que utiliza a conexão com o S3, deve ser alterado o caminho do S3 para um bucket em que sua credencial registrada no CLI da AWS tenha acesso. Neste bucket deve conter o documento JSON contido na pasta docker-glue/data

# Hipóteses e escolha de arquitetura
Levou-se em conta que os arquivos JSON seguem o mesmo padrão de estrutura, vindo contido em uma lista de dicionários com registros. Também foi admitido que os valores NA nos campos de desconto podem ser interpretados como 0.

Este projeto em docker foi escolhido por ser de fácil reprodução para realizar a verificação dos testes, e também por ser semelhante a um ambiente de desenvolvimento GLUE na AWS.

# Prós e contras
- Prós:
    - Portabilidade do ambiente via docker
    - Ambiente semelhante ao utilizado em desenvolvimento com glue jobs

- Contras:
    - Não implementa nenhuma filtragem na conexão com o S3, dessa forma caso o bucket contenha muitos dados, teremos sérios problemas de performance.
    - Método de leitura do hdfs contendo os dados é fechado para um único arquivo, o que é inviável para aplicações reais.
    - Ambiente docker utilizado para desenvolvimento, está longe de ser adequado para produção. Deve ser utilizado o serviço GLUE da AWS.

# Melhorias sugeridas
Como não tenho muita experiência com spark, acredito que o código tenha problemas de performance em ambiente de big data. Com mais tempo, pesquisaria e leria mais sobre o assunto para implementar uma solução mais adequada.