class ChoiceText:
    def __init__(self, text, choices=[], results=[]):
        self.text = text
        # useless outside of demoing the functionality
        if len(results) is 0:
            results = [lambda: None] * len(choices)
        self.choices = list(zip(choices, results))

    def select(self, index):
        return self.choices[index]()
