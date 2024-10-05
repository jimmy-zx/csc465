class Expression:
    def copy(self) -> "Expression":
        return self

    def eval_var(self, table: dict[str, "Expression"]) -> "Expression":
        return self.copy()

    def __repr__(self) -> str:
        return str(self)
