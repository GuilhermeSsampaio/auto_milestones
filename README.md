# Auto Milestones GitHub

Este projeto automatiza a criação de milestones e issues (com subtarefas) em um repositório GitHub, baseado em um plano de trabalho definido em Python.

## Funcionalidades

- Cria milestones no repositório GitHub.
- Cria issues principais associadas a cada milestone.
- Cria subtarefas como issues separadas e as vincula à issue principal.
- Atualiza o corpo da issue principal com uma checklist das subtarefas.

## Como usar

1. **Configure as variáveis no `script.py`:**

   - Defina seu token de acesso pessoal do GitHub (PAT) na variável de ambiente `GITHUB_TOKEN`.
   - Informe o proprietário do repositório (`REPO_OWNER`) e o nome do repositório (`REPO_NAME`).
   - Edite o dicionário `PROJECT_PLAN` conforme seu plano de trabalho.

2. **Instale as dependências:**

   ```bash
   pip install PyGithub
   ```

3. **Execute o script:**
   ```bash
   python script.py
   ```

## Exemplo de plano de trabalho

O plano de trabalho é definido no formato:

```python
PROJECT_PLAN = {
     "Milestone 1: Estruturação Inicial": {
          "Issue #1: Configuração do projeto e ambiente": [
                "Criar estrutura de diretórios...",
                "Configurar Dockerfile...",
                # ...
          ],
          # ...
     },
     # ...
}
```

## Requisitos

- Python 3.8+
- [PyGithub](https://github.com/PyGithub/PyGithub)
- Um Personal Access Token do GitHub com permissão `repo`

## Observações

- O script evita duplicação de milestones e issues.
- As subtarefas são criadas como issues separadas e listadas na issue principal.
- Recomenda-se rodar o script apenas uma vez por milestone para evitar duplicação.

## Licença

MIT
