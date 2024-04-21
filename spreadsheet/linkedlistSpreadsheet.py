import math

from spreadsheet.baseSpreadsheet import BaseSpreadsheet
from spreadsheet.cell import Cell


# class ListNode:
#     '''
#     Define a node in the linked list
#     '''
#
#     def __init__(self, word_frequency: WordFrequency):
#         self.word_frequency = word_frequency
#         self.next = None

# ------------------------------------------------------------------------
# This class  is required TO BE IMPLEMENTED
# Linked-List-based spreadsheet implementation.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2023, RMIT University'
# ------------------------------------------------------------------------


class Node:
    '''
    A basic type in linked list
    '''

    # this is a reference of the doubly linked list code provided in Week 3 tutorial.
    # combination of getter and setter methods

    def __init__(self, value):
        self.m_value = value
        self.m_next = None
        self.m_prev = None

    def get_value(self):
        return self.m_value

    def get_next(self):
        return self.m_next

    def get_prev(self):
        return self.m_prev

    def set_value(self, value):
        self.m_value = value

    def set_next(self, next):
        self.m_next = next

    def set_prev(self, prev):
        self.m_prev = prev


class DoubleLinkedList:

    def __init__(self):
        """
        Default constructor.
        """
        self.m_head = None
        self.m_tail = None
        self.m_length = 0

    def add(self, value):
        """
        Add a new value to the end of the list.

        @param newValue Value to add to list.
        """
        new_node = Node(value)

        # If head is empty, then list is empty and head and tail references need to be initialised.
        if self.m_tail is None:
            self.m_head = new_node
            self.m_tail = new_node

        # otherwise, add node to the tail of list.
        else:
            self.m_tail.set_next(new_node)
            new_node.set_prev(self.m_tail)
            self.m_tail = new_node

        self.m_length += 1

    def insert(self, index, new_value):

        new_node = Node(new_value)

        # insert method referenced from Week 3 Tutorial.
        # traverses through the list both ways, to determine if the index is closer
        # to the head or tail of the list
        if index < math.ceil(self.m_length / 2):

            if index == -1:
                self.m_head.set_prev(new_node)
                new_node.set_next(self.m_head)
                self.m_head = new_node
            else:
                cur_node = self.m_head
                for i in range(index):
                    cur_node = cur_node.get_next()

                # nextNode is the one being shift up
                nextNode = cur_node.get_next()
                nextNode.set_prev(new_node)
                new_node.set_next(nextNode)
                new_node.set_prev(cur_node)
                cur_node.set_next(new_node)
        else:
            # if index is towards the end of the list
            cur_node = self.m_tail
            for i in range(self.m_length - 1, index, -1):
                cur_node = cur_node.get_prev()

            nextNode = cur_node.get_next()
            nextNode.set_prev(new_node)
            new_node.set_next(nextNode)
            new_node.set_prev(cur_node)
            cur_node.set_next(new_node)

        self.m_length += 1


class LinkedListSpreadsheet(BaseSpreadsheet):

    def __init__(self):
        # TO BE IMPLEMENTED
        self.data_structure = DoubleLinkedList()
        self.no_rows = 0
        self.no_cols = 0

    def buildSpreadsheet(self, lCells: [Cell]):
        """
        Construct the data structure to store nodes.
        @param lCells: list of cells to be stored
        """

        # determines the max number of rows and columns
        self.no_rows = max(c.row for c in lCells) + 1
        self.no_cols = max(c.col for c in lCells) + 1
        # loop that iterates through the rows and columns of the spreadsheet
        for i in range(self.no_rows):
            row = DoubleLinkedList()
            for j in range(self.no_cols):
                cell = Cell(i, j, None)
                for c in lCells:
                    if c.row == i and c.col == j:
                        cell = c

                row.add(cell)

            self.data_structure.add(row)

    def appendRow(self):
        """
        Appends an empty row to the spreadsheet.
        """
        # append a new empty row using the add method
        try:
            appended_row = DoubleLinkedList()
            for j in range(self.no_cols):
                appended_row.add(Cell(self.no_rows, j, None))
            self.data_structure.add(appended_row)
            self.no_rows += 1

            return True
        # raise exception when failure
        except Exception as e:
            print("Error! ", e)
            return False

    def appendCol(self):
        """
        Appends an empty column to the spreadsheet.

        @return True if operation was successful, or False if not.
        """

        # append a new column using the add method
        try:

            curr_row = self.data_structure.m_head
            for i in range(self.no_rows):
                curr_node = curr_row.get_value()
                curr_node.add(Cell(i, self.no_cols, None))
                curr_row = curr_row.get_next()
            self.no_cols += 1



            return True
        # raise exception when failure
        except Exception as e:
            print("Error! ", e)
            return False

    def insertRow(self, rowIndex: int) -> bool:
        """
        Inserts an empty row into the spreadsheet.

        @param rowIndex Index of the existing row that will be after the newly inserted row.  If inserting as first row, specify rowIndex to be 0.  If inserting a row after the last one, specify rowIndex to be rowNum()-1.

        @return True if operation was successful, or False if not, e.g., rowIndex is invalid.
        """
        # this is to make sure that the rowIndex is valid
        try:
            if rowIndex < -1 or rowIndex > self.no_rows:
                raise IndexError("Invalid")
            # rowIndex += 1
            new_row = DoubleLinkedList()
            for j in range(self.no_cols):
                new_row.add(Cell(rowIndex, j, None))

            self.data_structure.insert(rowIndex, new_row)
            self.no_rows += 1

            updated_row_index = self.data_structure.m_tail

            for i in range(self.no_rows - 1, rowIndex, -1):

                updated_node = updated_row_index.m_value.m_head

                for k in range(self.no_cols):
                    updated_node.m_value.row += 1
                    updated_node = updated_node.get_next()
                updated_row_index = updated_row_index.get_prev()

            return True
        except IndexError:
            return False



    def insertCol(self, colIndex: int) -> bool:
        """
        Inserts an empty column into the spreadsheet.

        @param colIndex Index of the existing column that will be before the newly inserted row.  If inserting as first column, specify colIndex to be -1.
        """
        try:

            if colIndex < -1 or colIndex >= self.no_cols:
                raise IndexError("Invalid")
            curr_row = self.data_structure.m_head
            for i in range(self.no_rows):
                curr_list = curr_row.m_value
                curr_list.insert(colIndex, Cell(i, colIndex + 1, None))
                updated_node = curr_list.m_tail
                for j in range(self.no_cols, colIndex + 1, -1):
                    updated_node.m_value.col += 1
                    updated_node = updated_node.get_prev()
                curr_row = curr_row.get_next()
            self.no_cols += 1
            return True

        except IndexError:
            return False

    def update(self, rowIndex: int, colIndex: int, value: float) -> bool:
        """
        Update the cell with the input/argument value.

        @param rowIndex Index of row to update.
        @param colIndex Index of column to update.
        @param value Value to update.  Can assume they are floats.

        @return True if cell can be updated.  False if cannot, e.g., row or column indices do not exist.
        """
        # this below is to make sure that the row and columns are correct, and are not less than the actual number
        if rowIndex >= self.no_rows or \
                rowIndex < 0 or \
                colIndex >= self.no_cols or \
                colIndex < 0:
            return False

        curr_node = self.data_structure.m_head
        # this is a reference to the tutorial, where the math library is used.
        # this is to check whether if rowIndex should start from the head or the tail.
        if rowIndex < math.ceil(self.no_rows / 2):
            for i in range(rowIndex):
                curr_node = curr_node.get_next()
        else:
            curr_node = self.data_structure.m_tail
            for j in range(self.no_rows - 1, rowIndex, -1):
                curr_node = curr_node.get_prev()
        # same idea according to the rowIndex
        curr_cell = curr_node.get_value().m_head
        if colIndex < math.ceil(self.no_cols / 2):
            for i in range(colIndex):
                curr_cell = curr_cell.get_next()
        else:
            curr_cell = curr_node.get_value().m_tail
            for j in range(self.no_cols - 1, colIndex, -1):
                curr_cell = curr_cell.get_prev()

        curr_cell.m_value.val = value
        return True

    def rowNum(self) -> int:
        """
        @return Number of rows the spreadsheet has.
        """
        # simply returns number of rows
        return self.no_rows

    def colNum(self) -> int:
        """
        @return Number of column the spreadsheet has.
        """
        # simply returns number of columns.
        return self.no_cols

    def find(self, value: float) -> [(int, int)]:
        """
        Find and return a list of cells that contain the value 'value'.

        @param value value to search for.

        @return List of cells (row, col) that contains the input value.
	    """

        # TO BE IMPLEMENTED
        # this list will store the list of cells of that certain value
        target_cells = []
        curr_node = self.data_structure.m_head

        # nested loop that loops through the linkedlist
        for j in range(self.no_rows):
            curr_list = curr_node.get_value()
            cell_node = curr_list.m_head
            for i in range(self.no_cols):
                cell = cell_node.get_value()
                if cell.val is not None and cell.val == value:
                    target_cells.append((cell.row, cell.col))
                cell_node = cell_node.get_next()
            curr_node = curr_node.get_next()
        return target_cells

    def entries(self) -> [Cell]:
        """
        @return A list of cells that have values (i.e., all non None cells).
        """

        # empty list to store cells that have value
        entries = []
        curr_node = self.data_structure.m_head
        # similar logic to the find method above, iterates through the linkedlist
        for j in range(self.no_rows):
            curr_list = curr_node.get_value()
            cell_node = curr_list.m_head
            for i in range(self.no_cols):
                cell = cell_node.get_value()
                if cell.val is not None:
                    entries.append(cell)
                cell_node = cell_node.get_next()
            curr_node = curr_node.get_next()

        # TO BE IMPLEMENTED
        return entries
