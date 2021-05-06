from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from EnPra import Globals

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
  def init(self, topic_id):
    dic1 = anvil.server.call("loadtitle", topic_id, '1')
    self.repeating_panel_1.items = dic1   
    Globals.dic1 = dic1

    dic2 = anvil.server.call("loadtitle", topic_id, '2')
    self.repeating_panel_2.items = dic2
    Globals.dic2 = dic2

    dic3 = anvil.server.call("loadtitle", topic_id, '3')
    self.repeating_panel_3.items = dic3
    Globals.dic3 = dic3
    
    title_id, title_name = anvil.server.call("get_title", topic_id)
    dlg_line = anvil.server.call("loaddialog", title_id)
    self.text_area_1.text = dlg_line
    
    return title_id, title_name
    
  def init_bytitle(self, title_id): 
    self.repeating_panel_1.items = Globals.dic1
    self.repeating_panel_2.items = Globals.dic2
    self.repeating_panel_3.items = Globals.dic3
    
    dlg_line = anvil.server.call("loaddialog", title_id)
    self.text_area_1.text = dlg_line    
    