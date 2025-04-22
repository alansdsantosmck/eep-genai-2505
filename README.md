# Sistema de Correspondência de Talentos

Um sistema completo para encontrar candidatos adequados com base em descrições de trabalho, utilizando um algoritmo de pontuação para classificar os candidatos.

## 📋 Visão Geral

O Sistema de Correspondência de Talentos é uma aplicação web que ajuda equipes de serviços a cliente a encontrar candidatos ideais para suas posições. O sistema utiliza um algoritmo de pontuação para comparar as habilidades, experiência e localização dos candidatos com os requisitos da vaga, apresentando os melhores candidatos classificados com explicações detalhadas.

## 🚀 Tecnologias Utilizadas

### Backend
- **FastAPI**: Framework moderno e de alto desempenho para construção de APIs
- **Pydantic**: Validação de dados e configurações
- **SQLAlchemy**: ORM para interação com banco de dados
- **Alembic**: Gerenciamento de migrações de banco de dados

### Frontend
- **React**: Biblioteca JavaScript para construir interfaces de usuário
- **TypeScript**: Superset tipado de JavaScript para melhor desenvolvimento
- **Material UI**: Componentes React para um design elegante e responsivo
- **Axios**: Cliente HTTP para fazer requisições ao backend

## 🏗️ Estrutura do Projeto

```
alembic.ini               # Configuração do Alembic para migrações
README.md                 # Documentação do projeto
requirements.txt          # Dependências Python
alembic/                  # Scripts de migração do banco de dados
app/                      # Código principal do backend
  ├─ __init__.py
  ├─ main.py              # Ponto de entrada da API FastAPI
  ├─ db_models.py         # Modelos do banco de dados SQLAlchemy
  ├─ models.py            # Modelos de dados Pydantic
  ├─ services.py          # Lógica de negócios
  ├─ schemas.py           # Esquemas de dados
  ├─ utils.py             # Utilitários
  └─ data/                # Dados do sistema
      └─ candidates.json  # Banco de dados JSON de candidatos
frontend/                 # Código do frontend React
  ├─ public/              # Arquivos públicos estáticos
  └─ src/                 # Código fonte React
      ├─ components/      # Componentes React reutilizáveis
      ├─ services/        # Serviços para comunicação com backend
      └─ types/           # Definições de tipos TypeScript
tests/                    # Testes automatizados
```

## 🔧 Instalação e Configuração

### Pré-requisitos
- Python 3.9+
- Node.js 14+
- npm 6+

### Backend (FastAPI)

1. Clone o repositório:
```bash
git clone [URL-do-repositório]
cd [nome-do-repositório]
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Linux/Mac
venv\Scripts\activate     # No Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Inicie o servidor FastAPI:
```bash
uvicorn app.main:app --reload
```

O servidor backend estará disponível em http://localhost:8000.

### Frontend (React)

1. Navegue até a pasta do frontend:
```bash
cd frontend
```

2. Instale as dependências:
```bash
npm install
```

3. Inicie o servidor de desenvolvimento:
```bash
npm start
```

O frontend estará disponível em http://localhost:3000.

## 🖥️ Como Usar

1. Acesse o frontend em http://localhost:3000 (ou http://localhost:3001, dependendo da disponibilidade da porta)

2. Preencha o formulário de descrição de vaga com os seguintes detalhes:
   - **Nome do Cliente**: O nome da empresa ou cliente
   - **Declaração do Problema**: Descrição do problema que o cliente está enfrentando
   - **Título da Vaga**: O título do cargo desejado
   - **Localização**: A localização desejada para o candidato
   - **Indústria**: O setor ou indústria de atuação
   - **Habilidades Requeridas**: Lista de habilidades necessárias (separadas por vírgula)
   - **Anos de Experiência**: Quantidade desejada de anos de experiência

3. Clique em "Find Matching Candidates" para ver os candidatos correspondentes.

4. O sistema mostrará os três melhores candidatos classificados por pontuação, com explicações sobre por que cada candidato é adequado para a vaga.

## 🧮 Algoritmo de Pontuação

O sistema utiliza um algoritmo de pontuação para classificar candidatos com base em vários fatores:

1. **Correspondência de Título**: Os candidatos recebem pontos se seu título atual corresponde ao título da vaga.
2. **Habilidades Correspondentes**: Pontos são atribuídos com base em quantas habilidades requeridas o candidato possui.
3. **Correspondência de Localização**: Candidatos na mesma localização recebem pontos adicionais.
4. **Experiência na Indústria**: Candidatos com experiência na indústria específica recebem pontos.
5. **Anos de Experiência**: Candidatos com anos de experiência próximos ao requisito recebem pontos com base na proximidade.

Cada critério recebe uma pontuação específica, e a pontuação total é normalizada para uma escala de 0-10.

## 🛠️ API Endpoints

- **POST /match**: Recebe uma descrição de vaga e retorna os candidatos mais adequados.
  - Corpo da requisição: Objeto JSON contendo os detalhes da vaga
  - Resposta: Array de objetos de candidatos com pontuações e explicações

## 🧪 Testes

Execute os testes automatizados usando pytest:

```bash
pytest tests/
```

## 📚 Recursos Adicionais

- [Documentação FastAPI](https://fastapi.tiangolo.com/)
- [Documentação React](https://reactjs.org/docs/getting-started.html)
- [Documentação Material UI](https://mui.com/getting-started/usage/)

## 👥 Contribuição

1. Faça um fork do projeto
2. Crie sua feature branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.
