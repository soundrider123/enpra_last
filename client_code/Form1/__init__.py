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
    
    self.label_title.text =title_name
    self.button_start.tag = title_id
    
    Globals.title_id = title_id
    Globals.title_name = title_name
    
  def change_title(self, title_name, title_id):     
    dlg_line = anvil.server.call("loaddialog", title_id)
    self.text_area_1.text = dlg_line    

    self.label_title.text =title_name
    self.button_start.tag = title_id
    
    Globals.title_id = title_id
    Globals.title_name = title_name

  def button_start_click(self, **event_args):
    """This method is called when the button is clicked"""
    title_id = self.button_start.tag
       
    Globals.form2.init(title_id)
    Globals.form2.label_title.text = self.label_title.text
    Globals.mainform.flow_panel_1.clear()
    Globals.form2.xy_panel_1.remove_from_parent()
    Globals.mainform.flow_panel_1.add_component(Globals.form2.xy_panel_1)
    Globals.mainform.check_recording = True
    
    Globals.form2.question_voice()

  def button_startmatch_click(self, **event_args):
    """This method is called when the button is clicked"""
    Globals.form3.init(Globals.title_id)
    Globals.form3.label_title.text = Globals.title_name
    Globals.mainform.flow_panel_1.clear()
    Globals.form3.xy_panel_1.remove_from_parent()
    Globals.mainform.flow_panel_1.add_component(Globals.form3.xy_panel_1)
    Globals.mainform.check_recording2 = True
    
    Globals.form3.question_voice()
    


