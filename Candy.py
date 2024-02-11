class Candy:

    def __init__(self, color, bBox):
        self.color = color
        self.x, self.y, self.w, self.h = bBox

    def is_similar(self, candy):
        return ((self.x <= candy.x <= self.x + self.w or candy.x <= self.x <= candy.x + candy.w)
                and (self.y <= candy.y <= self.y + self.h or candy.y <= self.y <= candy.y + candy.h))


    def update(self, bBox):
        self.x, self.y, self.w, self.h = bBox