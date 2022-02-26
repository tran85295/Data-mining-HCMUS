class Column:
    def __init__(self, name):
        self.name = name
        self.data = []
        self.dtype = 'numeric'
        self.length = 0
        self.missing_value_indexes = []

    def add_data(self, value):
        try:
            value = (float)(value)
        except ValueError:
            if len(value) == 0:
                value = None
                self.missing_value_indexes.append(self.length)
            else: self.dtype = 'categorical'

        self.length += 1
        self.data.append(value)

    # get mean or median or mode, based on method and data type
    def get_mmm(self, method):
        # create a new list from self.data without None type elements
        filtered = []
        for value in self.data:
            if value is not None:
                filtered.append(value)
        if len(filtered) == 0:
            return 0

        if self.dtype == 'numeric':
            if method is None or method == 'mean':
                # calculate mean by default or by specified method
                return sum(filtered)/len(filtered)
            # calculate median
            filtered.sort()
            half = len(filtered)//2
            if len(filtered) % 2 == 0:
                return (filtered[half]+filtered[half-1])/2
            return filtered[half]
        # calculate modes for catgorical data type
        counter = dict()
        for key in filtered:
            counter[key] =  counter.get(key, 0) + 1

        max_value = max(counter.values())
        keys = []
        for key, value in counter.items():
            if value == max_value:
                keys.append(key)
        return keys

    def normalize(self, method):
        # remove None type elements and store to a temp list
        tmp = [val for val in self.data if val is not None]
        if len(tmp) == 0:
            #do nothing with column with full of Nones
            return

        if method == 'min-max':
            m, M = min(tmp), max(tmp)
            if m != M:
                for ind, val in enumerate(self.data):
                    if val is not None:
                        self.data[ind] = (val-m)/(M-m)
            return 

        mean = sum(tmp)/len(tmp)
        tmp_sum = sum((value - mean)**2 for value in tmp)
        stdev = (tmp_sum/(len(tmp)-1))**0.5

        if stdev != 0:
            for ind, val in enumerate(self.data):
                if val is not None:
                    self.data[ind] = (val - mean)/stdev
        return

    # define operators between columns
    # e.g. column = column+column as below
    def __add__(self, other):
        result = Column('')
        for i in range(self.length):
            if self.data[i] is None or other.data[i] is None:
                result.add_data('')
            else: result.add_data(self.data[i]+other.data[i])
        return result

    def __sub__(self, other):
        result = Column('')
        for i in range(self.length):
            if self.data[i] is None or other.data[i] is None:
                result.add_data('')
            else: result.add_data(self.data[i]-other.data[i])
        return result

    def __mul__(self, other):
        result = Column('')
        for i in range(self.length):
            if self.data[i] is None or other.data[i] is None:
                result.add_data('')
            else: result.add_data(self.data[i]*other.data[i])
        return result
    
    def __truediv__(self, other):
        result = Column('')
        for i in range(self.length):
            try:
                result.add_data(self.data[i]/other.data[i])
            except: result.add_data('')
        return result

    def __neg__(self):
        result = Column('')
        for val in self.data:
            if val is None:
                result.add_data('')
            else: result.add_data(-val)
        return result