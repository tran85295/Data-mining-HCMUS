import csv
from Column import Column

# this dataframe is based on a list of columns
class DataFrame:
    def __init__(self, filename):
        self.filename = filename
        csv_file = open(filename,"r")
        reader = csv.reader(csv_file)

        # read header row as column names
        self.names = reader.__next__()
        self.width = len(self.names)
        # store data by a list of columns
        self.cols = list()
        for i in range(self.width):
            col = Column(self.names[i])
            self.cols.append(col)
        # read data by lines
        for line in reader:
            for index, value in enumerate(line):
                self.cols[index].add_data(value)

        self.height = reader.line_num - 1
        csv_file.close()

    # function 1
    def list_missing(self, args):
        print("There are missing values in these following columns: ")
        for col in self.cols:
            if len(col.missing_value_indexes) != 0:
                print(col.name)

    # function 2
    def count_missing(self, args):
        indexes = set()
        for col in self.cols:
            for row_index in col.missing_value_indexes:
                indexes.add(row_index)
        print('Number of rows with missing value:', len(indexes))

    # check valid names and return corresponding column objects
    def get_valid(self, names):
        if names is None:                     
            return self.cols
        valid_columns = list()
        for name in names:
            try:
                index = self.names.index(name)
            except: continue
            valid_columns.append(self.cols[index])
        return valid_columns

    # save to file
    def save(self, filename):
        if filename is None:
            # modify the opened file by default
            filename = self.filename

        csv_file = open(filename,"w")
        writer = csv.writer(csv_file)
        writer.writerow(self.names) # write header of csv file

        for row in range(self.height):
            line = []
            for column in self.cols:
                line.append(column.data[row])
            writer.writerow(line)
        csv_file.close()
        print('Saved result in', filename)

    #function 3
    def impute(self, args):
        # guarantee the validity of the arguments
        if args.method not in [None, 'median', 'mean']:
            print("Invalid method")
            return
        valid_columns = self.get_valid(args.columns)
        # impute
        for column in valid_columns:
            impute_value = column.get_mmm(args.method)
            if isinstance(impute_value, list):
                # list of modes returned by categorical attribute
                step = 0
                for position in column.missing_value_indexes:
                    column.data[position] = impute_value[step]
                    # alternate between the modes
                    step += 1
                    step = step % len(impute_value)
            else:
                # the impute value can be mean or median here
                for position in column.missing_value_indexes:
                    column.data[position] = impute_value
            column.missing_value_indexes = []

        self.save(args.outfile)

    # a helper function that removes a specific row by given index
    def remove_a_row(self, index):
        for col in self.cols:
            del col.data[index]
            try:
                col.missing_value_indexes.remove(index)
            except: pass
        self.height -= 1

    #function 4
    def remove_row(self, args):
        threshold = (float)(args.threshold)/100
        counter = dict()        # count missing values by row index
        for col in self.cols:
            for index in col.missing_value_indexes:
                counter[index] = counter.get(index, 0) + 1

        for row_index in range(self.height-1, -1, -1):
            if counter[row_index]/self.width > threshold:
                self.remove_a_row(row_index)
                
        self.save(args.outfile)

    #function 5
    def remove_col(self, args):
        threshold = (float)(args.threshold)/100
        for col_index in range(self.width -1, -1, -1):
            if len(self.cols[col_index].missing_value_indexes)/self.height > threshold:
                del self.cols[col_index]
                del self.names[col_index]

        self.width = len(self.names)
        self.save(args.outfile)

    # helper function for checking if ith row and jth row are the same
    def are_same(self, i, j):
        for col in self.cols:
            if col.data[i] != col.data[j]:
                return False
        return True

    #function 6
    def remove_duplicate(self, args):
        for i in range(self.height-1, -1, -1):
            for j in range(i-1, -1, -1):
                if self.are_same(i, j):
                    self.remove_a_row(i)
                    break
        self.save(args.outfile)

    #function 7
    def normalize(self, args):
        if args.method not in [None, 'min-max', 'Z-score']:
            print('Invalid method')
            return
        if args.method is None:
            method = 'min-max'  #default method if not provided
        else: method = args.method
        valid_columns = self.get_valid(args.columns)

        for column in valid_columns:
            if column.dtype == 'numeric':
                column.normalize(method)
        self.save(args.outfile)

    #function 8
    def calculate(self, args):
        new_col, formula = args.formula.split('=')
        # list attribute names from expression
        attrs = list()
        attr = ''
        for char in formula:
            if char in '()+-*/':
                if attr != '':
                    attrs.append(attr)
                attr = ''
            else: attr += char
        if attr != '':
            attrs.append(attr)
        # get the corresponding column object
        cols = self.get_valid(attrs)
        # check the validity
        if len(cols) != len(attrs):
            print('There are invalid attributes in the expression')
            return
        for col in cols:
            if col.dtype == 'categorical':
                print('There are categorical attributes in the expression')
                return
        # calulate
        for ind, entry in enumerate(attrs):
            formula = formula.replace(entry, 'cols['+str(ind)+']')
        result = eval(formula)
        # add new returned column to dataframe and save
        self.names.append(new_col)
        self.cols.append(result)
        self.width += 1

        self.save(args.outfile)
        


            




        




        



    









    



        






    




