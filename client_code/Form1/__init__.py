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

    dic1 = anvil.server.call("loadtopic")
    self.repeating_panel_1.items = dic1
    
    self.change_topic('1')
    
    self.text_area_1.width = "400px"
    
  def change_topic(self, topic_id):
    dic2 = anvil.server.call("loadtitle", topic_id)
    self.repeating_panel_2.items = dic2
    
    title_id, title_name = anvil.server.call("get_title", topic_id)
    dlg_line = anvil.server.call("loaddialog", title_id)
    self.text_area_1.text = dlg_line
    
    Globals.mainform.link_1.text =title_name+ '  [ Start ] '
    Globals.mainform.link_1.tag = title_id
    
  def change_title(self, title_name, title_id):     
    dlg_line = anvil.server.call("loaddialog", title_id)
    self.text_area_1.text = dlg_line    

    Globals.mainform.link_1.text =title_name+ '  [ Start ] '
    Globals.mainform.link_1.tag = title_id
    