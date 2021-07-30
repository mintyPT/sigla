class DataFinder:
    def __init__(self, obj):
        self.obj = obj

    def find_by_id(self, id_: int):
        if hasattr(self.obj, "id") and self.obj.get("id") == id_:
            return self.obj

        for child in self.obj:
            if found := DataFinder(child).find_by_id(id_):
                return found

        return None