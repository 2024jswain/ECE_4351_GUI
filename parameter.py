class Parameter:

    def __init__(self, display_name, theoretical_min, default_min, default, default_max, theoretical_max, step):
        self.display_name = display_name
        self.theoretical_min = theoretical_min
        self.min = default_min
        self.value = default
        self.max = default_max
        self.theoretical_max = theoretical_max
        self.step = step


    def set_min(self, new_min):
        """ Sets a new minimum value with validation. """
        if new_min < self.theoretical_min:
            raise ValueError(f"{self.display_name} cannot be less than {self.theoretical_min}")

        if new_min > self.theoretical_max - self.step:
            raise ValueError(f"{self.display_name} cannot be equal to or greater than {self.theoretical_max}")

        if new_min > self.value:
            self.value = new_min + self.step

        self.min = new_min

    def set_max(self, new_max):
        """ Sets a new maximum value with validation. """
        if new_max > self.theoretical_max:
            raise ValueError(f"{self.display_name} cannot be greater than {self.theoretical_max}")

        if new_max < self.theoretical_min + self.step:
            raise ValueError(f"{self.display_name} cannot be equal to or less than {self.theoretical_min}")

        if new_max < self.value:
            self.value = new_max - self.step

        self.max = new_max


