# Forms-Flask

Este repositório contém uma aplicação Flask de um formulário para o uso de uma IA de previsão para saber se o usuário recomendaria ou não utilizando Flask e Machine Learning.

## Estrutura do Projeto

- `app.py`: O arquivo principal da aplicação Flask e a lógica de registro no banco sql.
- `requirements.txt`: Lista todas as dependências necessárias para rodar o projeto.
- `static/`: Diretório para arquivos estáticos como CSS e algumas imagens.
- `templates/`: Diretório que contém templates HTML para a interface do usuário.
- `modelo_com_preprocessador.joblib`: Um modelo pré-treinado (com pré-processador) para uso na aplicação.
- `.github/workflows/`: Contém workflows de GitHub Actions para automação.
- `pull_request_template.md`: Template para criação de pull requests.

## Funcionalidade

  1. **Renderização do Formulário**: Apresenta ao usuário um formulário HTML para ser preenchido, acessível através de uma interface web.
  2. **Coleta de Dados do Formulário**: Recebe os dados enviados pelo usuário através do formulário.
  3. **Processamento de Dados**: Os dados são transformados em um DataFrame usando o Pandas.
  4. **Aplicação do Modelo de Machine Learning**: O DataFrame é utilizado como entrada em um modelo de machine learning previamente treinado, carregado do sistema de arquivos, para fazer uma previsão.
  5. **Inserção no Banco de Dados**: Baseado na previsão, os resultados são inseridos no banco de dados associando a previsão ao nome do usuário.
  6. **Resposta ao Usuário**: Dependendo da previsão do modelo (positiva ou negativa), uma imagem correspondente é exibida.


## Configuração Inicial

1. Clone o repositório:
git clone https://github.com/Systeam-Viajou/Forms-Flask.git

2. Instale as dependências:
pip install -r requirements.txt

3. Execute a aplicação:
python app.py

#### Desenvolvido com ❤ e carinho pela equipe de análise de dados *Viajou*:

- [Gabriel Costa](https://github.com/gbrlscosta)
- [Gabrieli Oliveira](https://github.com/gabrieliolveira)
