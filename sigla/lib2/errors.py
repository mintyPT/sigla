class TemplateDoesNotExistError(Exception):
    def __init__(self, tag, from_entity, *args: object) -> None:
        self.message = f"Missing template {tag}"
        self.from_entity = from_entity
        super().__init__(self.message, *args)
