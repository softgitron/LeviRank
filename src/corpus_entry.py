class CorpusEntry(dict):
    id: str
    contents: str
    chat_noir_url: str

    def __init__(self,*arg,**kw):
      super(CorpusEntry, self).__init__(*arg, **kw)
      self.__dict__ = self

    def __repr__(self) -> str:
        return f"""id: {self.id}, contents: "{self.contents}"\n"""