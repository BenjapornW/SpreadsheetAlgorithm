from spreadsheet.baseSpreadsheet import BaseSpreadsheet
from spreadsheet.cell import Cell

# ------------------------------------------------------------------------
# This class is required TO BE IMPLEMENTED
# Trie-based dictionary implementation.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2023, RMIT University'
# ------------------------------------------------------------------------


class CSRSpreadsheet(BaseSpreadsheet):

    def __init__(self):
        # TO BE IMPLEMENTED

        # track no. of rows
        self.no_rows = 0
        # track no. of columns
        self.no_cols = 0
        # track column no.
        self.colA = []
        # track value
        self.valA = []
        # track sum # default: cumulative sum up to row 0 (not including row 0)
        self.sumA = [0]



    def buildSpreadsheet(self, lCells: [Cell]):
        """
        Construct the data structure to store nodes.
        @param lCells: list of cells to be stored
        """

        # TO BE IMPLEMENTED

        self.no_rows = max(cell.row for cell in lCells) + 1  # plus 1 since the index starts with 0
        self.no_cols = max(cell.col for cell in lCells) + 1  # plus 1 since the index starts with 0
        temp_container = []

        for i in range(self.no_rows):
            row = []
            for j in range(self.no_cols):
                # create cell object
                cell = Cell(i, j, None) # set val = None since there is no value now
                # loop through the sample data and assign value when the row(i), and column (j) matches
                for c in lCells:
                    if i == c.row and j == c.col:
                        cell.val = c.val # assign the value
                row.append(cell)
            temp_container.append(row)

        # after this different from arraySpreadsheet
        # fill the value of colA, valA, sumA
        sum = 0
        for i in range(self.no_rows):
            for j in range(self.no_cols):
                if temp_container[i][j].val is not None:
                    self.colA.append(temp_container[i][j].col)
                    self.valA.append(temp_container[i][j].val)
                    sum += temp_container[i][j].val #self.data_structure[i][j] or cell.val
        # need to append sum under row for loop because each row for loop, we will get 1 sum to add in sumA
        # if append sum to sumA outside row for loop, we will get only 1 sum to add in SumA for the whole spreadsheet
            self.sumA.append(sum)


    def appendRow(self):
        """
        Appends an empty row to the spreadsheet.

        @return True if operation was successful, or False if not.
        """

        # TO BE IMPLEMENTED
        try:
            self.sumA.append(self.sumA[-1])
            # add 1 to update no_rows after appending new row at the bottom
            self.no_rows += 1
            return True

        except Exception as e:
            print('Error: ', e)
            return False

    def appendCol(self):
        """
        Appends an empty column to the spreadsheet.

        @return True if operation was successful, or False if not.
        """

        # TO BE IMPLEMENTED
        try:
            # add 1 to update no_cols after appending new row at the bottom
            self.no_cols += 1
            return True

        except Exception as e:
            print('Error: ', e)
            return False

    def insertRow(self, rowIndex: int)->bool:
        """
        Inserts an empty row into the spreadsheet.

        @param rowIndex Index of the existing row that will be after the newly inserted row.  If inserting as first row, specify rowIndex to be 0.  If inserting a row after the last one, specify rowIndex to be rowNum()-1.

        @return True if operation was successful, or False if not, e.g., rowIndex is invalid.
        """

        if rowIndex < -1 or rowIndex >= self.no_rows:
            return False
        else:
            rowIndex += 1  # the first row will be -1+1 = 0
            self.sumA.insert(rowIndex + 1, self.sumA[rowIndex])
            # add 1 to update no_rows after appending new row at the bottom
            self.no_rows += 1
            return True


    def insertCol(self, colIndex: int)->bool:
        """
        Inserts an empty column into the spreadsheet.

        @param colIndex Index of the existing column that will be after the newly inserted row.  If inserting as first column, specify colIndex to be 0.  If inserting a column after the last one, specify colIndex to be colNum()-1.

        return True if operation was successful, or False if not, e.g., colIndex is invalid.
        """


        if colIndex < -1 or colIndex >= self.no_cols:  # constraints from assignment's spec
            return False
        else:
            colIndex += 1  # the first col will be -1+1 = 0
            for i in range(0, len(self.colA)):
                if self.colA[i] >= colIndex:
                    self.colA[i] += 1
            self.no_cols += 1
            return True


    def update(self, rowIndex: int, colIndex: int, value: float) -> bool:
        """
        Update the cell with the input/argument value.

        @param rowIndex Index of row to update.
        @param colIndex Index of column to update.
        @param value Value to update.  Can assume they are floats.

        @return True if cell can be updated.  False if cannot, e.g., row or column indices do not exist.
        """

        # TO BE IMPLEMENTED
        if rowIndex >= self.no_rows or \
            rowIndex < 0 or \
            colIndex >= self.no_cols or \
            colIndex < 0:
            return False
        else:

            boolean_exist = False
            j = 0
            row_sum = self.sumA[rowIndex]
            temp_dif = round(self.sumA[rowIndex + 1] - row_sum, 2)
            #loop row
            while row_sum != 0:
                row_sum = round(row_sum - self.valA[j], 2)
                j += 1
            # got j
            sum_dif = value
            #loop column
            while temp_dif != 0:
                temp_dif = round(temp_dif - self.valA[j], 2)
                #check whether the column exist
                if self.colA[j] == colIndex:
                    boolean_exist = True
                    sum_dif = round(sum_dif - self.valA[j], 2)
                    # case I: update the value that is already existed
                    self.valA[j] = value
                    #after update value break the loop
                    break
                j += 1
            # if the value is not existed
            if not boolean_exist:
                # case II: insert the value that does not exist
                self.valA.insert(j, value)
                self.colA.insert(j, colIndex)
                #loop though sum
            for i in range(rowIndex+1, len(self.sumA)):
                self.sumA[i] = round(self.sumA[i] + sum_dif, 2)
            return True

    def rowNum(self)->int:
        """
        @return Number of rows the spreadsheet has.
        """
        # TO BE IMPLEMENTED
        return self.no_rows


    def colNum(self)->int:
        """
        @return Number of column the spreadsheet has.
        """
        # TO BE IMPLEMENTED
        return self.no_cols



    def find(self, value: float) -> [(int, int)]:
        """
        Find and return a list of cells that contain the value 'value'.

        @param value value to search for.

        @return List of cells (row, col) that contains the input value.
	    """

        # TO BE IMPLEMENTED
        # create empty list to store research result
        search_array = []
        j = 0
        for i in range(1, len(self.sumA)):
            sum_dif = round(self.sumA[i] - self.sumA[i-1], 2)
            while sum_dif != 0:
                sum_dif = round(sum_dif - self.valA[j], 2)
                if self.valA[j] == value:
                    search_array.append((i-1, self.colA[j]))
                j += 1
        return search_array


    def entries(self) -> [Cell]:
        """
        return a list of cells that have values (i.e., all non None cells).
        """

        # create empty list to store research result
        entries = []
        j = 0
        for i in range(1, len(self.sumA)):
            sum_dif = round(self.sumA[i] - self.sumA[i-1], 2)
            while sum_dif != 0:
                sum_dif = round(sum_dif - self.valA[j], 2)
                entries.append(Cell(i-1, self.colA[j], self.valA[j]))
                j += 1
        return entries

