from ._anvil_designer import Form3Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Form3(Form3Template):
  def __init__(self, **properties):
    self.lines = []
    self.cur_pos = 0
    self.dialog_id_a = 0
    self.dialog_id_b = 0
    
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    
  def init(self, title_id):
    self.label_correct.text = ""    
    
    self.lines = []
    self.cur_pos = 0
    self.dialog_id_a = 0
    
    dlg_line = anvil.server.call('loadtalk', title_id)
    self.dlg_lines = dlg_line
    left_line = int(len(self.dlg_lines) / 2)
    self.label_left.text = str(left_line)
    
    self.dialog_id_a = self.dlg_lines[self.cur_pos]['dialog_id']
    
    self.lines.append({'dialog_line': self.dlg_lines[self.cur_pos]['dialog_line']})
    self.repeating_panel_1.items = self.lines
    
  def question_voice(self):
    url1 = f'https://43.231.114.140:8080/getaudio/{self.dialog_id_a}' 
    Globals.mainform.call_js('PlaySound', url1)  