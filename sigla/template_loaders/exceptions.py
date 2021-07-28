class TemplateDoesNotExistError(FileNotFoundError):
    def __init__(self, tag, *args: object) -> None:
        self.message = f"Missing template {tag}"
        super().__init__(self.message, *args)