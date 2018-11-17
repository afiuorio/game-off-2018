class DescriptionObject:

    def __init__(self, name, description="", cry=""):
        self.name = name
        self.description = description
        self.cry = cry

    def get_infos(self):
        return self.name + ": " + self.description
