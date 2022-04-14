class CorpusEntry(dict):
    id: str
    contents: str
    contents_preprocessed: str = None
    chat_noir_url: str
    spelling_errors_count: int

    # https://stackoverflow.com/questions/4014621/a-python-class-that-acts-like-dict
    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        if key == "docno":
            return self.id
        elif key == "text":
            return self.contents_preprocessed
        else:
            return self.__dict__[key]

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key]

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def get(self, k):
        return self.__dict__.get(k)

    def has_key(self, k):
        return k in self.__dict__

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def pop(self, *args):
        return self.__dict__.pop(*args)

    def __cmp__(self, dict_):
        return self.__cmp__(self.__dict__, dict_)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

    def __repr__(self) -> str:
        return f"""id: {self.id}, contents: "{self.contents}, contents_preprocessed: "{self.contents}"\n"""
