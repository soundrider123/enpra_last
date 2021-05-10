from ._anvil_designer import Form3Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from EnPra import Globals

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
    #print(title_id)
    self.lines = []
    self.cur_pos = 0
    self.dialog_id_a = 0
    self.correct = 0
    
    dlg_line = anvil.server.call('loadtalk', title_id)
    self.dlg_lines = dlg_line
    left_line = int(len(self.dlg_lines) / 2)
    self.all = left_line 
    self.label_left.text = str(left_line)
    self.label_correct.text = str(self.correct) + ' / ' + str(self.all) 
    
    self.dialog_id_a = self.dlg_lines[self.cur_pos]['dialog_id']
    
    self.lines.append({'dialog_line': self.dlg_lines[self.cur_pos]['dialog_line']})
    self.repeating_panel_2.items = self.lines
    
    ###################################
    self.ans_lines = anvil.server.call('loadanswer', title_id)
    itm_lines=[]
    for itm in self.ans_lines:
      itm_lines.append({'dialog_line': itm['dialog_line']})
    self.repeating_panel_1.items = itm_lines
    
    
  def question_voice(self):
    url1 = f'https://43.231.114.140:8080/getaudio/{self.dialog_id_a}' 
    Globals.mainform.call_js('PlaySound', url1) 
    
  def record_answer_clicked(self):
    if len(self.dlg_lines) >= self.cur_pos+2:    
      dialog_id_b = anvil.server.call('get_transcription', Globals.mainform.userid, Globals.title_id)
      itm_lines=[]
      for b_line in self.ans_lines:
        if str(b_line['dialog_id']) == str(dialog_id_b):
          self.lines.append({'dialog_line': b_line['dialog_line']})
          
          if str(self.dlg_lines[self.cur_pos+1]['dialog_id']) == str(dialog_id_b): 
            self.correct = int(self.correct) + 1
            self.label_correct.text = str(self.correct) + ' / ' + str(self.all) 
          
          if len(self.dlg_lines) > self.cur_pos+2:
            self.lines.append({'dialog_line': self.dlg_lines[self.cur_pos+2]['dialog_line']})
            self.cur_pos = self.cur_pos + 2
            self.dialog_id_a = self.dlg_lines[self.cur_pos]['dialog_id']
            self.question_voice()
            
          left_line = int(self.label_left.text)-1
          self.label_left.text = str(left_line)            
          self.repeating_panel_2.items = self.lines
          continue
          
        itm_lines.append({'dialog_line': b_line['dialog_line']})
        self.repeating_panel_1.items = itm_lines
      
      
      