class MayMust():
    def __init__(self, may, must):
        self.may = may
        self.must = must


class ColumnDomain():
    def __init__(self):
        self.original = {"must": set(), "may": set()}
        self.current = {"must": set(), "may": set()}
        self.added = {"must": set(), "may": set()}
        self.removed = {"must": set(), "may": set()}

        self.copies = {}

    def __str__(self):
        return f"Original: {self.original}, Current: {self.current}, "\
               f"Added: {self.added}, Removed: {self.removed}, "\
               f"T: {self.copies}"
