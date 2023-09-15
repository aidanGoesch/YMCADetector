class Letters:
    def __init__(self, *values):
        self.values = list(values)

    def add(self, value):
        if len(self.values) > 0:
            if self.values[-1] != value:
                self.values.append(value)
        else:
            self.values.append(value)

    def __getitem__(self, item):
        result = []
        if len(self.values) == 0:
            return []

        if type(item) == slice:
            if item.start < 0:
                start = len(self.values) + item.start
            else:
                start = item.start

            if item.stop is None:
                stop = len(self.values)
            else:
                stop = item.stop

            for i in range(start, stop):
                result.append(self.values[i])
        else:
            raise Exception

        return result

    def __len__(self):
        return len(self.values)

    def __repr__(self):
        if len(self.values) < 3:
            return f"Letters({self.values})"
        else:
            return f"Letters({self.values[-4:]})"
