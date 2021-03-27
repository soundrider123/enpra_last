from ._anvil_designer import MainFormTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

class MainForm(MainFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    anvil.google.auth.login()
    self.userid = anvil.server.call('get_userid')
    
    self.audiorecord_1.init_userid(self.userid)
    self.prev = False

  def timer_tick(self, **event_args):    
    isrecording = anvil.js.call_js('get_startrecording_disabled') 
    #print(isrecording)
    if (self.prev == True and isrecording == False):
      transcription = anvil.server.call('get_transcription', self.userid)
      self.label_2.text = transcription
    
    self.prev = isrecording


