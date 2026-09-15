# Banco de Dados 2 🗄️​

Aplicação web desenvolvida em Flask com integração a banco de dados relacional (SQLite) utilizando Flask-SQLAlchemy, persistência de registros de usuários e associação com funções (`Role`).

---

## 🚀 Principais Funcionalidades

- **Persistência Relacional:** Modelagem de dados dividida entre tabelas de usuários (`User`) e funções (`Role`), garantindo o armazenamento permanente dos dados.

  
- **Associação de Registros:** Cada usuário cadastrado via formulário é associado automaticamente a uma função padrão no banco de dados.

  
- **Listagem Dinâmica:** Consulta e exibição em tempo real de todos os usuários cadastrados diretamente na interface web.


---

## ⚙️ O que foi necessário implementar? 

- **Configuração do Object-Relational Mapping (ORM):** Inicialização do Flask-SQLAlchemy conectada a um banco SQLite local (`data.sqlite`).

  
- **Modelos de Dados:** Definição das classes `User` e `Role` mapeadas via ORM, estabelecendo chaves estrangeiras e relacionamentos bidirecionais.

  
- **Contexto de Shell:** Configuração do `@app.shell_context_processor` para facilitar testes e manipulações de dados via terminal (`flask shell`).
