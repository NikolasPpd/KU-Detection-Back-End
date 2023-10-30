class Author:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.commits = []

    def add_commit(self, commit):
        self.commits.append(commit)

    @property
    def commit_count(self):
        return len(self.commits)

    def identifier(self):
        """Current identification mechanism: combination of name and email."""
        return self.name, self.email

    def __hash__(self):
        return hash(self.identifier())

    def __eq__(self, other):
        return self.identifier() == other.identifier()

    def __str__(self):
        return f"{self.name} <{self.email}>"
