class Topic:
    number: str
    title: int
    objects: list[str]
    description: str
    narrative: str

    def __repr__(self) -> str:
        return f"""Number: {self.number}, Title: "{self.title}"\n"""