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


def get_week_day(day: int):
    days_of_week = {
        1: "Sunday",
        2: "Monday",
        3: "Tuesday",
        4: "Wednesday",
        5: "Thursday",
        6: "Friday",
        7: "Saturday",
    }
    return days_of_week.get(day)


def get_colors_list(n: int, color_type: str = "hsl"):
    print(color_type)
    if color_type == "hsl":
        return [f"hsl({i*137%360}, 64%, 55%)" for i in range(n)]
    elif color_type == "rgba":
        return [
            f"rgba({(i*123)%256}, {(i*211)%256}, {(i*37)%256}, {i/10})"
            for i in range(n)
        ]
    else:
        raise ValueError(f"Invalid color type: {color_type}")
