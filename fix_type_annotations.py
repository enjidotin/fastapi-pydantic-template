#!/usr/bin/env python3
"""
Script to fix all the mypy type annotation issues in the codebase.
"""

import re

# Files that need fixing
FILES_TO_FIX = [
    "app/core/ports/repositories.py",
    "app/core/config.py",
    "app/core/ports/item_repository.py",
    "app/adapters/repositories/sqlalchemy_models.py",
    "app/tests/test_item_domain.py",
    "app/adapters/repositories/sqlalchemy_item_repository.py",
    "app/adapters/repositories/database.py",
    "app/api/routes/items.py",
    "app/main.py",
    "app/tests/conftest.py",
]


def fix_repositories():
    path = "app/core/ports/repositories.py"
    with open(path) as f:
        content = f.read()

    # Add missing type annotations
    # Look for the function at line 27
    pattern = r"def get_by_filter\((.*?)\)"
    replacement = r"def get_by_filter(self, filter_dict: Dict[str, Any])"
    content = re.sub(pattern, replacement, content)

    with open(path, "w") as f:
        f.write(content)
    print(f"✅ Fixed {path}")


def fix_config():
    path = "app/core/config.py"
    with open(path) as f:
        content = f.read()

    # Fix the return type issue at line 49
    pattern = r"def get_allowed_hosts\(.*?\).*?:\n.*?return json\.loads\((.*?)\)"
    replacement = (
        r"def get_allowed_hosts(self) -> List[str]:\n        return json.loads(\1)"
    )
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(path, "w") as f:
        f.write(content)
    print(f"✅ Fixed {path}")


def fix_item_repository():
    path = "app/core/ports/item_repository.py"
    with open(path) as f:
        content = f.read()

    # Add @abc.abstractmethod to abstract methods
    if "import abc" not in content and "from abc import" not in content:
        content = "import abc\n" + content

    # Update method definitions to include abstractmethod
    pattern1 = r"(def get_by_filter\(.*?\):)"
    replacement1 = r"@abc.abstractmethod\n    \1"
    content = re.sub(pattern1, replacement1, content)

    pattern2 = r"(def update_by_filter\(.*?\):)"
    replacement2 = r"@abc.abstractmethod\n    \1"
    content = re.sub(pattern2, replacement2, content)

    with open(path, "w") as f:
        f.write(content)
    print(f"✅ Fixed {path}")


def fix_sqlalchemy_models():
    path = "app/adapters/repositories/sqlalchemy_models.py"
    with open(path) as f:
        content = f.read()

    # Fix the Base class issue
    pattern = r"class ItemModel\((.*?)\):"
    replacement = r"class ItemModel(Base):"
    content = re.sub(pattern, replacement, content)

    with open(path, "w") as f:
        f.write(content)
    print(f"✅ Fixed {path}")


def fix_test_item_domain():
    path = "app/tests/test_item_domain.py"
    with open(path) as f:
        content = f.read()

    # Add return type annotations to all test functions
    pattern1 = r"def test_create_item\((.*?)\):"
    replacement1 = r"def test_create_item(\1) -> None:"
    content = re.sub(pattern1, replacement1, content)

    pattern2 = r"def test_update_item\((.*?)\):"
    replacement2 = r"def test_update_item(\1) -> None:"
    content = re.sub(pattern2, replacement2, content)

    pattern3 = r"def test_item_validation\((.*?)\):"
    replacement3 = r"def test_item_validation(\1) -> None:"
    content = re.sub(pattern3, replacement3, content)

    with open(path, "w") as f:
        f.write(content)
    print(f"✅ Fixed {path}")


def fix_sqlalchemy_item_repository():
    path = "app/adapters/repositories/sqlalchemy_item_repository.py"
    with open(path) as f:
        content = f.read()

    # Add missing type annotations
    # For line 39
    pattern1 = r"def exists\((.*?)\)"
    replacement1 = r"def exists(self, item_id: str)"
    content = re.sub(pattern1, replacement1, content)

    # For line 156 - fix the where clause type
    pattern2 = r"where\(False\)"
    replacement2 = r"where(ItemModel.id == None)"  # A better typed expression
    content = re.sub(pattern2, replacement2, content)

    with open(path, "w") as f:
        f.write(content)
    print(f"✅ Fixed {path}")


def fix_database():
    path = "app/adapters/repositories/database.py"
    with open(path) as f:
        content = f.read()

    # Fix the sessionmaker call at line 24
    pattern1 = r"sessionmaker\(engine, AsyncSession, expire_on_commit=False\)"
    replacement1 = (
        r"sessionmaker(class_=AsyncSession, expire_on_commit=False, bind=engine)"
    )
    content = re.sub(pattern1, replacement1, content)

    # Fix the async generator return type at line 29
    pattern2 = r"async def get_db\((.*?)\):"
    replacement2 = r"async def get_db(\1) -> AsyncGenerator[AsyncSession, None]:"
    content = re.sub(pattern2, replacement2, content)

    # Add missing return type annotation at line 42
    pattern3 = r"def get_engine\((.*?)\):"
    replacement3 = r"def get_engine(\1) -> None:"
    content = re.sub(pattern3, replacement3, content)

    with open(path, "w") as f:
        f.write(content)
    print(f"✅ Fixed {path}")


def fix_items_routes():
    path = "app/api/routes/items.py"
    with open(path) as f:
        content = f.read()

    # Add return type annotations to all route handlers
    functions = [
        (
            r"async def get_items\((.*?)\):",
            r"async def get_items(\1) -> ItemListResponse:",
        ),
        (r"async def get_item\((.*?)\):", r"async def get_item(\1) -> ItemResponse:"),
        (
            r"async def create_item\((.*?)\):",
            r"async def create_item(\1) -> ItemResponse:",
        ),
        (
            r"async def update_item\((.*?)\):",
            r"async def update_item(\1) -> ItemResponse:",
        ),
        (
            r"async def delete_item\((.*?)\):",
            r"async def delete_item(\1) -> Dict[str, str]:",
        ),
        (
            r"async def search_items\((.*?)\):",
            r"async def search_items(\1) -> ItemListResponse:",
        ),
        (
            r"async def filter_items\((.*?)\):",
            r"async def filter_items(\1) -> ItemListResponse:",
        ),
    ]

    for pattern, replacement in functions:
        content = re.sub(pattern, replacement, content)

    # Fix the items type conversion at lines 42 and 153
    patterns = [
        (
            r"return ItemListResponse\(items=items\)",
            r"return ItemListResponse(items=[ItemResponse.from_domain(item) for item in items])",
        ),
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)

    with open(path, "w") as f:
        f.write(content)
    print(f"✅ Fixed {path}")


def fix_main():
    path = "app/main.py"
    with open(path) as f:
        content = f.read()

    # Add missing return type annotations
    pattern1 = r"def startup\((.*?)\):"
    replacement1 = r"def startup(\1) -> None:"
    content = re.sub(pattern1, replacement1, content)

    pattern2 = r"def shutdown\((.*?)\):"
    replacement2 = r"def shutdown(\1) -> None:"
    content = re.sub(pattern2, replacement2, content)

    with open(path, "w") as f:
        f.write(content)
    print(f"✅ Fixed {path}")


def fix_conftest():
    path = "app/tests/conftest.py"
    with open(path) as f:
        content = f.read()

    # Add return type annotations
    pattern1 = r"def setup_test_db\((.*?)\):"
    replacement1 = r"def setup_test_db(\1) -> None:"
    content = re.sub(pattern1, replacement1, content)

    # Fix the session fixture
    pattern2 = r"def db_session\(request(.*?)\):"
    replacement2 = r"def db_session(request\1) -> AsyncSession:"
    content = re.sub(pattern2, replacement2, content)

    # Fix the session context manager - replace normal session with async session
    pattern3 = r"with SessionLocal\(\) as session:"
    replacement3 = r"async with SessionLocal() as session:"
    content = re.sub(pattern3, replacement3, content)

    with open(path, "w") as f:
        f.write(content)
    print(f"✅ Fixed {path}")


if __name__ == "__main__":
    print("Fixing type annotation issues...")
    fix_repositories()
    fix_config()
    fix_item_repository()
    fix_sqlalchemy_models()
    fix_test_item_domain()
    fix_sqlalchemy_item_repository()
    fix_database()
    fix_items_routes()
    fix_main()
    fix_conftest()
    print("\nAll type annotation issues fixed! Run mypy again to verify.")
