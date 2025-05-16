# ToDoList - Gerenciador de Tarefas

## Visão Geral

O ToDoList é uma aplicação web para gerenciamento de tarefas, desenvolvida com tecnologias front-end modernas (HTML5, CSS3 e JavaScript) com integração a uma API back-end em Flask.


## Funcionalidades Principais

- Criação e organização de tarefas com campos detalhados (nome, descrição, prioridade, categoria)
- Sistema de categorias personalizáveis
- Filtragem avançada por prioridade e categoria
- Controle de status (tarefas pendentes/concluídas)
- Interface intuitiva com navegação por abas
- Design responsivo para diferentes dispositivos

## Tecnologias Utilizadas

### Frontend
- HTML5 semântico
- CSS3 com Flexbox/Grid Layout
- JavaScript ES6+
- Font Awesome para ícones

### Backend (API)
- Flask (Python)
- Banco de dados SQLite/PostgreSQL

## Estrutura do Projeto

```
todolist/
├── index.html          # Página principal
├── styles/             # Diretório de estilos CSS
├── scripts/            # Diretório de scripts JavaScript
└── README.md           # Documentação
```

## Instalação e Execução

### Pré-requisitos
- Servidor Flask configurado na porta 5000
- Navegador moderno (Chrome, Firefox ou Edge versões recentes)

### Passos para Execução
1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/todolist.git
   ```

2. Acesse o diretório do projeto:
   ```bash
   cd todolist
   ```

3. Inicie o servidor Flask:
   ```bash
   python app.py
   ```

4. Abra o arquivo index.html no navegador ou acesse:
   ```
   http://localhost:5000
   ```

## Personalização

Para adaptar a aplicação às suas necessidades:

1. Cores: Edite as variáveis CSS na seção `:root`
2. Layout: Ajuste os grids e flexbox no arquivo CSS
3. Funcionalidade: Modifique as constantes JavaScript como `TAREFAS_POR_PAGINA`

## Contribuição

Contribuições são bem-vindas seguindo o fluxo padrão:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Distribuído sob licença MIT. Veja o arquivo `LICENSE` para mais informações.

## Contato

✉️ Contato  
Desenvolvido por Ingride - ingridesouza040@gmail.com

<div align="center">Feito com ❤️ e ☕ por IngrideSouzaDev</div>
