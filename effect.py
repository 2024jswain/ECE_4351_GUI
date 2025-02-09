class Effect:

    def __init__(self):

        self.parameters = self.init_parameters()
        self.display_name = self.init_display_name()

        for key, parameter in self.get_parameters().items():
            setattr(self, key, parameter.value)

    def apply(self, frame):

        setattr(self, 'frame', frame)

        return self.my_effect()

    def get_parameters(self):
        return self.parameters

    def my_effect(self):
        return None

    def init_parameters(self):
        return {}

    def init_display_name(self):
        return ''