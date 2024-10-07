from transaction.models import Category


def insert_categories():
    # Define the categories to insert
    categories = [
        {
            "name": "Housing",
            "category_type": Category.CategoryTypes.DEBIT,
            "icon_id": 1,
        },  # Assuming icon ID exists
        {
            "name": "Transportation",
            "category_type": Category.CategoryTypes.DEBIT,
            "icon_id": 1,
        },
        {"name": "Food", "category_type": Category.CategoryTypes.DEBIT, "icon_id": 1},
        {"name": "Health", "category_type": Category.CategoryTypes.DEBIT, "icon_id": 1},
        {
            "name": "Salary",
            "category_type": Category.CategoryTypes.CREDIT,
            "icon_id": 1,
        },
    ]

    for cat in categories:
        # Use get_or_create to avoid duplicates
        category, created = Category.objects.get_or_create(
            name=cat["name"],
            category_type=cat["category_type"],
            defaults={"icon_id": cat["icon_id"]},
        )
        if created:
            print(f"Inserted category: {category.name}")
        else:
            print(f"Category already exists: {category.name}")
