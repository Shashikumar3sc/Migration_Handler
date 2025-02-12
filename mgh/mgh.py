import os
import subprocess

def run_command(command):
    """Runs a shell command and prints the output."""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    if stdout:
        print(stdout.decode())
    if stderr:
        print(stderr.decode())

def commit_init_files():
    """Commits all xyz__init__.py files to the dev branch."""
    run_command("git add */migrations/*__init__.py")
    run_command("git commit -m 'Initial commit of xyz__init__.py files'")
    run_command("git push origin dev")

def create_migrations():
    """Creates Django migration files."""
    run_command("python manage.py makemigrations")

def clone_repo(repo_url, clone_path):
    """Clones the repository to a new location."""
    run_command(f"git clone {repo_url} {clone_path}")

def delete_old_migrations(clone_path):
    """Deletes all migration files except __init__.py from the newly cloned repo."""
    for root, dirs, files in os.walk(clone_path):
        if "migrations" in root.split(os.sep):  # Ensures it's a Django migrations folder
            for file in files:
                if file != "__init__.py" and file.endswith(".py"):  # Delete all .py files except __init__.py
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")

    print("✅ Old migration files deleted successfully from the newly cloned repo.")

def apply_migrations():
    """Runs the Django migration command."""
    run_command("python manage.py migrate")

def update_pod(clone_path):
    """Pulls the latest code and applies migrations in the dev pod."""
    run_command(f"cd {clone_path} && git pull origin dev && python manage.py migrate")

if __name__ == "__main__":
    repo_url = "https://github.com/Shashikumar3sc/Migration_Handler.git"  # Change to your actual repo URL
    clone_path = "C:/Docker/MIGRATION/New"  # Change to your new clone location
    project_path = os.path.join(clone_path, "Migration_Handler")  # Adjust based on your project structure

    # Step 1: Commit only xyz__init__.py files
    commit_init_files()

    # Step 2: Create migration files in the existing project
    create_migrations()

    # Step 3: Clone the repository to a new location
    clone_repo(repo_url, clone_path)

    # Step 4: Delete old migration files ONLY from the newly cloned repo
    delete_old_migrations(clone_path)

    # Step 5: Create new migrations in the cloned repo
    create_migrations()

    # Step 6: Apply new migrations in the cloned repo
    apply_migrations()

    # Step 7: Update the pod with the latest code
    update_pod(clone_path)
