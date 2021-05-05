from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.repeating_panel_1.width = "500px"
    self.column_panel_1.height = "400px"

    # Any code you write here will run when the form opens.
    dic1 = anvil.server.call("loadtopic")
    self.repeating_panel_1.items = dic1    
    
    dic2 = anvil.server.call("loadtitle", '1')
    self.repeating_panel_2.items = dic2        