import os
from github import Github, GithubException
import json
from dotenv import load_dotenv
load_dotenv()
# --- Configurações ---
# Substitua 'SEU_GITHUB_TOKEN' pelo seu Personal Access Token do GitHub.
# É altamente recomendável carregar isso de variáveis de ambiente para segurança.
# Ex: export GITHUB_TOKEN="ghp_..."
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "SEU_GITHUB_TOKEN")

# Substitua 'SEU_USUARIO_OU_ORGANIZACAO' pelo nome de usuário ou organização do repositório.
# REPO_OWNER = "your-username-or-organization"
REPO_OWNER = os.getenv("REPO_OWNER", "SEU_USUARIO_OU_ORGANIZACAO")
# Substitua 'SEU_NOME_DO_REPOSITORIO' pelo nome do seu repositório.
REPO_NAME = os.getenv("REPO_NAME", "SEU_NOME_DO_REPOSITORIO")

# --- Definição das Milestones e Issues (Baseado no seu Plano de Trabalho) ---
# Estrutura: { "Nome da Milestone": ["Issue 1", "Issue 2", ...] }
# Você pode adicionar mais detalhes para as issues aqui se quiser,
# como descrições ou labels, mas para simplicidade, estamos usando apenas o título.
with open('project_plan.json', 'r') as f:
    PROJECT_PLAN = json.load(f)


def create_github_milestones_and_issues():
    """
    Cria milestones e issues no repositório GitHub especificado,
    baseado no dicionário PROJECT_PLAN.
    """
    try:
        # Autentica no GitHub
        g = Github(GITHUB_TOKEN)
        print("Conectado ao GitHub com sucesso.")

        # Obtém o repositório
        repo = g.get_user(REPO_OWNER).get_repo(REPO_NAME)
        print(f"Repositório '{REPO_OWNER}/{REPO_NAME}' encontrado.")

        # Itera sobre as milestones definidas no plano
        for milestone_title, issue_titles in PROJECT_PLAN.items():
            milestone = None
            # Verifica se a milestone já existe
            existing_milestones = repo.get_milestones(state='open')
            for m in existing_milestones:
                if m.title == milestone_title:
                    milestone = m
                    print(f"Milestone '{milestone_title}' já existe. Usando existente.")
                    break

            if not milestone:
                # Cria a milestone se não existir
                milestone = repo.create_milestone(title=milestone_title)
                print(f"Milestone '{milestone_title}' criada com sucesso.")

            # Itera sobre as issues para a milestone atual
            # for issue_title in issue_titles:
            #     issue = None
            #     # Verifica se a issue já existe na milestone
            #     # Nota: A API do GitHub não permite filtrar issues por milestone diretamente na busca global.
            #     # A abordagem mais robusta seria buscar todas as issues abertas e filtrar localmente,
            #     # ou confiar que o título da issue é único o suficiente para evitar duplicação.
            #     # Para este script, vamos simplificar e verificar se a issue existe no repositório.
            #     existing_issues = repo.get_issues(state='open', milestone=milestone)
            #     for i in existing_issues:
            #         if i.title == issue_title:
            #             issue = i
            #             print(f"Issue '{issue_title}' já existe na milestone '{milestone_title}'.")
            #             break

            #     if not issue:
            #         # Cria a issue e a associa à milestone
            #         issue = repo.create_issue(
            #             title=issue_title,
            #             milestone=milestone,
            #             body=f"Esta issue faz parte da milestone '{milestone_title}' do plano de trabalho."
            #         )
            #         print(f"Issue '{issue_title}' criada e associada à milestone '{milestone_title}'.")
            #     # Itera sobre as issues para a milestone atual
            for issue_title, subtasks in issue_titles.items():
                issue = None

                # Verifica se a issue já existe na milestone
                existing_issues = repo.get_issues(state='open', milestone=milestone)
                for i in existing_issues:
                    if i.title == issue_title:
                        issue = i
                        print(f"Issue '{issue_title}' já existe na milestone '{milestone_title}'.")
                        break

                if not issue:
                    # Cria a issue principal
                    issue = repo.create_issue(
                        title=issue_title,
                        milestone=milestone,
                        body=f"Esta issue faz parte da milestone '{milestone_title}' do plano de trabalho.\n\n"
                    )
                    print(f"Issue '{issue_title}' criada e associada à milestone '{milestone_title}'.")

                # Agora cria as subtasks e adiciona no corpo da issue principal
                subtask_links = []
                for sub in subtasks:
                    sub_issue = repo.create_issue(
                        title=sub,
                        milestone=milestone,
                        body=f"Subtarefa de **{issue_title}**. Relacionada a #{issue.number}."
                    )
                    subtask_links.append(f"- [ ] #{sub_issue.number} {sub}")

                # Atualiza o corpo da issue principal com as subtarefas
                if subtask_links:
                    new_body = issue.body + "\n### Subtarefas\n" + "\n".join(subtask_links)
                    issue.edit(body=new_body)
                    print(f"Subtarefas adicionadas à issue '{issue_title}'.")


    except GithubException as e:
        print(f"Erro ao interagir com o GitHub: {e}")
        if e.status == 401:
            print("Verifique seu Personal Access Token. Pode ser inválido ou não ter as permissões necessárias.")
        elif e.status == 404:
            print("Verifique o nome do proprietário do repositório ou o nome do repositório.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    # Verifica se o token foi configurado
    if GITHUB_TOKEN == "SEU_GITHUB_TOKEN" or not GITHUB_TOKEN:
        print("ERRO: Por favor, configure seu Personal Access Token do GitHub na variável GITHUB_TOKEN ou como variável de ambiente.")
        print("Você pode obter um PAT em: https://github.com/settings/tokens")
        print("Certifique-se de que o PAT tenha permissões de 'repo'.")
    elif REPO_OWNER == "SEU_USUARIO_OU_ORGANIZACAO" or REPO_NAME == "SEU_NOME_DO_REPOSITORIO":
        print("ERRO: Por favor, configure o proprietário do repositório (REPO_OWNER) e o nome do repositório (REPO_NAME).")
    else:
        create_github_milestones_and_issues()