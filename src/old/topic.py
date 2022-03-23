class Topic:
    number: str
    title: int

    def __repr__(self) -> str:
        return f"""Number: {self.number}, Title: "{self.title}"\n"""