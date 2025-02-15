import os

# Define the folder structure
folders = [
    "app",
    "app/models",
    "app/schemas",
    "app/routes",
    "app/utils",
]

# Define the files to create
files = [
    "app/__init__.py",
    "app/main.py",
    "app/models/__init__.py",
    "app/models/user.py",
    "app/models/audit_log.py",
    "app/schemas/__init__.py",
    "app/schemas/user.py",
    "app/schemas/audit_log.py",
    "app/routes/__init__.py",
    "app/routes/user.py",
    "app/routes/auth.py",
    "app/utils/__init__.py",
    "app/utils/database.py",
    "app/utils/auth.py",
    "app/utils/logger.py",
    ".env",
    "requirements.txt",
    "README.md",
]

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create empty files
for file in files:
    with open(file, "w") as f:
        pass

print("Folder structure created successfully.")