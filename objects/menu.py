from textwrap import wrap
from interface.gui import ConsoleWrapper


class Menu:
    def __init__(self, choice_text, width, game_screen_width, game_screen_height):
        # three characters as left\right margins
        self.text_lines = wrap(choice_text.text, width - 6)
        self.choices = choice_text.choices
        self.choice_lines = list()
        # we assume choices won't wrap, it would make the height calculations uglier for little benefit
        for tuple in self.choices:
            self.choice_lines += [tuple[0]]
        self.width = width
        # three lines for top margin + frame title, one line between text and choices and two lines for bottom margin
        self.height = len(self.text_lines) + len(self.choice_lines) + 6
        self.cursor_position = 0
        self.x = 3
        x = int((game_screen_width - self.width) / 2)
        y = int((game_screen_height - self.height) / 2)
        self.console_wrapper = ConsoleWrapper(x, y, self.width, self.height)

    def move_cursor(self, direction):
        if self.choices:
            self.cursor_position += direction
            if self.cursor_position > len(self.choice_lines) - 1:
                self.cursor_position = 0
            if self.cursor_position < 0:
                self.cursor_position = len(self.choice_lines) -1

    def select_choice(self):
        if self.choices:
            self.choices[self.cursor_position][1]()

