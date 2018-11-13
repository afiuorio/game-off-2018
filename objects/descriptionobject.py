class DescriptionObject:

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def get_infos(self):
        return self.name + ": " + self.description
