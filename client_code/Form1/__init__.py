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
    
  def init(self, topic_id):
    dic1 = anvil.server.call("loadtitle", topic_id)
    self.repeating_panel_1.items = dic1   
    
    dlg_line = anvil.server.call("loaddialog_first", topic_id)
    self.text_area_1.text = dlg_line
    