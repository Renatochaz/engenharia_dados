# Funcionamento
O arquivo deserializer.py implementar uma classe com métodos para deserializar documentos JSON e converter os mesmos em dois dataframes separados, conforme o pedido no teste.

A notebook transform_NFe carrega a classe do deserializer e possibilita o usuário escolher uma pasta que tem os documentos JSON que serão transformados em dataframes.

# Como reproduzir
- Ambiente e biblioteca utilizadas:
    - python 3.8.10
    - pandas 1.4.2

Abra o notebook transform_NFe e passe o caminho do diretório contendo os documentos JSON para a classe ```NFeJsonDeserializer```. O caminho passado para o notebook é o caminho absoluto de onde o notebook foi instanciado.

Após isso, siga os exemples contidos no notebook ou leia a documentação da classe deserializer.

# Hipóteses e escolha de arquitetura
A escolha do notebook como interface para o *stakeholder* foi devido a natureza do pedido que especificamente pede um objeto dataframe, que normalmente é utilizado em notebooks para realizar análises.

Quanto a estrutura do arquivo, acredita-se que o JSON sempre seguirá o mesmo formato de dicionários contidos em uma lista, com as mesmas chaves.

Foi implementada a escolha genérica do nome da coluna "NFeID" como chave primária, porém a coluna ItemList foi *harcoded* na classe e acredita-se que a mesma não virá com nomes diferentes em diferentes arquivos.

# Prós e contras
- Prós:
    - Facilidade de uso;
    - Interface amigável para analistas;
    - Classe pode ser expandida para lidar com novas necessidades de negócio;

- Contras:
    - Não segue boas práticas de governança de dados, pois requer que o usuário tenha dados presentes na sua máquina que contém o notebook;
    - Falta de flexibilização para diferentes chaves que precisam ser expandidas, que não seja o "ItemList".

# Melhorias sugeridas
Levar o código para um jupyter notebook que tem um permissionamento adequado para quem for utilizar os dados.

Mudar a classe para ler arquivos de um repositório S3 ao invés de uma pasta local, onde podem ser aplicadas boas práticas com IAM para lidar com acesso aos dados.

- Apenas se a regra de negócio for adequada:

    Flexibilizar a escolha para o usuário de qual coluna precisa ser expandida, tirando a dependência fechada da coluna "ItemList". 