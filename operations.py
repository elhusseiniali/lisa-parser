from abc import ABC


class Operation(ABC):
    #   Need to add ID or name fields
    def __init__(self, file_name=None, column_name=None, row=None):
        self.file_name = file_name
        self.column_name = column_name
        self.row = row

    def __repr__(self):
        result = ""
        if self.file_name:
            result = f"file_name: {self.file_name}"
        if self.column_name:
            result = result + f" column_name: {self.column_name}"
        if self.row:
            result = result + f" rows: {self.row}"

        return result


class Projection(Operation):
    def __init__(self, column_name=None, row=None):
        super().__init__(file_name=None,
                         column_name=column_name,
                         row=row)


class Read(Operation):
    def __init__(self, file_name, column_name=None):
        super().__init__(file_name=file_name,
                         column_name=column_name,
                         row=None)


class Conversion(Operation):
    def __init__(self, column_name):
        super().__init__(column_name=column_name,
                         file_name=None,
                         row=None)


class Lambda(Operation):
    def __init__(self, column_name):
        super().__init__(column_name=column_name,
                         file_name=None,
                         row=None)


class Assignment(Operation):
    def __init__(self, column_name, value=None):
        super().__init__(column_name=column_name,
                         file_name=None,
                         row=None)
        self.value = value
