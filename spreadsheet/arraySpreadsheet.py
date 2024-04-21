from spreadsheet.cell import Cell
from spreadsheet.baseSpreadsheet import BaseSpreadsheet


# ------------------------------------------------------------------------
# This class is required TO BE IMPLEMENTED
# Array-based spreadsheet implementation.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2023, RMIT University'
# ------------------------------------------------------------------------

class ArraySpreadsheet(BaseSpreadsheet):

    def __init__(self):
        # TO BE IMPLEMENTED
        self.data_structure = []
        #track no. of rows
        self.no_rows = 0
        # track no. of columns
        self.no_cols = 0

    def buildSpreadsheet(self, lCells: [Cell]):
        """
        Construct the data structure to store nodes.
        @param lCells: list of cells to be stored
        """

        # TO BE IMPLEMENTED

        # get the maximum number of rows and maximum number of columns to get the size of the array
        # cell is object
        # use cell.row to access row, use cell.col to access col
        self.no_rows = max(cell.row for cell in lCells) + 1  # plus 1 since the index starts with 0
        self.no_cols = max(cell.col for cell in lCells) + 1  # plus 1 since the index starts with 0

        # create 2D spreadsheet >> create 2D array by using for-loop
        # Ref : https://www.geeksforgeeks.org/python-using-2d-arrays-lists-the-right-way

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
            self.data_structure.append(row)


    def appendRow(self) -> bool:
        """
        Appends an empty row to the spreadsheet.

        @return True if operation was successful, or False if not.
        """

        # TO BE IMPLEMENTED

        # create new array use no.of rows (#just create the array no need to plus one)
        # append row --> loop through column
        # In loop, only 1 number for row but many number for columns
        try:
            appended_row = []
            for j in range(self.no_cols):
                appended_row.append(Cell(self.no_rows, j, None))
            # append to the old array (plus 1 because append after last row)
            self.data_structure.append(appended_row)
            # add 1 to update no_rows after appending new row at the bottom
            self.no_rows += 1
            return True
        except Exception as e:
            print('Error: ', e)
            return False

    def appendCol(self) -> bool:
        """
        Appends an empty column to the spreadsheet.

        @return True if operation was successful, or False if not.
        """

        # TO BE IMPLEMENTED
        # no need to create new column just go through the old data structure and
        # add it like adding element in array
        try:
            for i in range(self.no_rows):
                self.data_structure[i].append(Cell(i, self.no_cols, None))
            # add 1 to update no_cols after appending new row at the bottom
            self.no_cols += 1
            return True
        except Exception as e:
            print('Error: ', e)
            return False

    def insertRow(self, rowIndex: int) -> bool:
        """
        Inserts an empty row into the spreadsheet.

        @param rowIndex Index of the existing row that will be after the newly inserted row.

        @return True if operation was successful, or False if not, e.g., rowIndex is invalid.
        """

        # TO BE IMPLEMENTED
        # use insert function
        if rowIndex < -1 or rowIndex >= self.no_rows:
            return False
        else:
            rowIndex += 1 # the first row will be -1+1 = 0
            inserted_row = []
            for j in range(self.no_cols):
                inserted_row.append(Cell(self.no_rows, j, None))
            # append to the old array (plus 1 because append after last row)
            self.data_structure.insert(rowIndex, inserted_row)
            # add 1 to update no_cols after inserting new row at the bottom

            for i in range(self.no_rows +1): # after inserting row +1 in self.no_rows
                # rowIndex - no need to plus 1 because insert the row after
                if i > rowIndex : # or i >= rowIndex +1 will give the same result
                    for j in range(self.no_cols):
                        #access 2d data structure and get the row to plus 1
                        self.data_structure[i][j].row += 1

            self.no_rows += 1  #
            return True

    def insertCol(self, colIndex: int) -> bool:
        """
        Inserts an empty column into the spreadsheet.

        @param colIndex Index of the existing column that will be after the newly inserted row.

        return True if operation was successful, or False if not, e.g., colIndex is invalid.
        """

        # TO BE IMPLEMENTED

        # constraints from assignment's spec
        if colIndex < -1 or colIndex >= self.no_cols:
            return False
        else:
            colIndex += 1 # the first col will be -1+1 = 0
            #insert column to each row
            for i in range(self.no_rows):
                self.data_structure[i].insert(colIndex, Cell(i, colIndex, None))
                for j in range(self.no_cols + 1): # +1  after inserting new column
                    if j > colIndex:
                        self.data_structure[i][j].col += 1


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
        # wrote

        # check if the cell existed. If it exists, update it.
        # check if rowIndex, ColIndex are out of range:
        # If out of range >> the cell does not exist >> How can you update?
        if rowIndex >= self.no_rows or \
            rowIndex < 0 or \
            colIndex >= self.no_cols or \
            colIndex < 0:
            return False
        else:
            # access 2d cell by index and update value
            self.data_structure[rowIndex][colIndex].val = value
            return True


    def rowNum(self) -> int:
        """
        @return Number of rows the spreadsheet has.
        """
        # TO BE IMPLEMENTED

        return self.no_rows

    def colNum(self) -> int:
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

        # search and append the row and column of the matching value to the list
        # loop through rows and columns to use i,j
        for i in range(self.no_rows):
            for j in range(self.no_cols):
                if self.data_structure[i][j].val is not None:
                    # check if the value matches with the value in the data structure
                    if self.data_structure[i][j].val == value:
                        # use another () to make a tuple
                        search_array.append((self.data_structure[i][j].row, self.data_structure[i][j].col))
        return search_array


    def entries(self) -> [Cell]:
        """
        @return A list of cells that have values (i.e., all non None cells).
        """

        # TO BE IMPLEMENTED
        entries = []
        for i in range(self.no_rows):
            for j in range(self.no_cols):
                if self.data_structure[i][j].val is not None:
                    entries.append(self.data_structure[i][j])

        return entries
