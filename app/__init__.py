import os
import shutil

# Estrutura de diretórios e arquivos
structure = {
    "app": [
        "__init__.py",
        "main.py",
        "models.py",
        "schemas.py",
        "services.py",
        "utils.py"
    ],
    "tests": [
        "__init__.py",
        "test_match.py"
    ],
    "": [  # Arquivos na raiz
        "requirements.txt",
        ".env",
        "README.md"
    ]
}

# Função para criar diretórios e mover/criar arquivos
def create_and_organize_structure(base_path, structure):
    for folder, files in structure.items():
        folder_path = os.path.join(base_path, folder)
        if folder:  # Cria o diretório se não for a raiz
            os.makedirs(folder_path, exist_ok=True)
            # Cria o arquivo __init__.py em cada diretório
            init_file = os.path.join(folder_path, "__init__.py")
            if not os.path.exists(init_file):
                with open(init_file, "w") as f:
                    f.write("")  # Cria um arquivo vazio
                print(f"Criado: {init_file}")
        for file in files:
            file_path = os.path.join(folder_path, file)
            existing_file_path = os.path.join(base_path, file)
            if os.path.exists(existing_file_path):  # Move arquivos existentes
                shutil.move(existing_file_path, file_path)
                print(f"Movido: {existing_file_path} -> {file_path}")
            elif not os.path.exists(file_path):  # Cria arquivos que não existem
                with open(file_path, "w") as f:
                    if file == "README.md":
                        f.write("# Talent Matching Bot Backend\n\n")
                    elif file == "requirements.txt":
                        f.write("fastapi\nuvicorn\nopenai\nsqlalchemy\nalembic\npydantic\npython-dotenv\n")
                    elif file == ".env":
                        f.write("# Add your environment variables here\n")
                    else:
                        f.write("")  # Cria arquivos vazios
                print(f"Criado: {file_path}")

# Caminho base do projeto
base_path = os.getcwd()

# Cria a estrutura e organiza os arquivos
create_and_organize_structure(base_path, structure)

print("Done!")