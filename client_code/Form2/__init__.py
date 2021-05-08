from ._anvil_designer import Form2Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from EnPra import Globals

class Form2(Form2Template):
  def __init__(self, **properties):
    self.last_line = None
    self.lines = []
    self.cur_pos = 0
    self.dialog_id = 0
    
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    self.button_match.visible = False

    
  def init(self, title_id):
    dlg_line = anvil.server.call('loadtalk', title_id)
    self.dlg_lines = dlg_line
    left_line = int(len(self.dlg_lines) / 2)
    self.label_left.text = str(left_line)
    self.text_box_line.text = self.dlg_lines[self.cur_pos+1]['dialog_line']
    cur_line = {'dialog_line': self.dlg_lines[self.cur_pos]['dialog_line']}
    self.dialog_id = self.dlg_lines[self.cur_pos]['dialog_id']
    self.lines.append(cur_line)
    self.repeating_panel_1.items = self.lines
    
  def button_match_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def button_answer_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def button_voice_click(self, **event_args):
    """This method is called when the button is clicked"""
    url1 = f'https://43.231.114.140:8080/audioplay?audioid={self.dialog_id}' 
    Globals.mainform.call_js('PlaySound', url1)



