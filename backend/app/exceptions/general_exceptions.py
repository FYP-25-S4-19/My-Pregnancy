class RoleNotFound(Exception):
    def __init__(self, role_label: str):
        self.message = f"Role '{role_label}' not found"
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message


class MetricCategoryNotFound(Exception):
    def __init__(self, category_label: str):
        self.message = f"Metric Category'{category_label}' not found"
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message
