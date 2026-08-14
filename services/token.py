class Token:

    def __init__(self, token_type, value, position=None):
        self.type = token_type
        self.value = value
        self.position = position

    def __repr__(self):

        return (
            f"Token("
            f"{self.type}, "
            f"{self.value}"
            f")"
        )

    def to_dict(self):
        return {
            "type": self.type,
            "value": self.value,
            "position": self.position
        }