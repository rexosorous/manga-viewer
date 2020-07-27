# dependencies
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import pyqtSignal



class ListItem(QListWidgetItem):
    """ListWidgetItems used to populate the various metadata lists

    This class allows us to store additional information (namely id) to be used in conjunction with the dbhandler to avoid string matching

    Args:
        id_ (int): id of the metadata
        name (str): name of the metadata and what is displayed in the list
        table (str): one of ['artists', 'series', 'genres', 'tags']

    Attributes:
        id_ (int)
        table (str)
    """
    def __init__(self, id_: int, name: str, table: str):
        super().__init__()
        self.id_ = id_
        self.table = table
        self.setText(name)



class Data():
    """Stores and keeps updated all the ListItem objects.

    This is used as the master reference for updating lists.

    Args:
        db (database.DBHandler)
        signals (signals.Signals)

    Attributes:
        db (database.DBHandler)
        signals (signals.Signals)
        mdata ([ListItem]): the master list of all metadata
    """
    def __init__(self, db, signals):
        self.db = db
        self.signals = signals
        self.mdata = list()
        self.generate_metadata()



    def generate_metadata(self):
        """Generates the MetadataListItems to be used for populating lists
        """
        self.mdata = list()
        for table in (data:=self.db.get_metadata()):
            for value in data[table]:
                self.mdata.append(ListItem(value['id'], value['name'], table))
        self.signals.update_metadata.emit()



    def create(self, table: str, name: str):
        self.db.create_entry(table, name)
        self.generate_metadata()



    def delete(self, item):
        self.db.delete_entry(item.table, item.id_)
        self.generate_metadata()