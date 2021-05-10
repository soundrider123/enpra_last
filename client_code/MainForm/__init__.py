from ._anvil_designer import MainFormTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from EnPra.Form1 import Form1
from EnPra.Form2 import Form2
from EnPra.Form3 import Form3
from EnPra import Globals
from EnPra.ProfileForm import ProfileForm
from EnPra.HowtoForm import HowtoForm

class MainForm(MainFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    Globals.mainform = self
    form1_instance = Form1(param='an_argument')
    self.flow_panel_1.clear()
    self.flow_panel_1.add_component(form1_instance)
    self.button_1.tag = form1_instance
    Globals.form1 = form1_instance

    profile_instance = ProfileForm(param='an_argument')
    self.button_2.tag = profile_instance    

    howto_instance = HowtoForm(param='an_argument')
    self.button_3.tag = howto_instance   
       
    anvil.google.auth.login()
    self.userid = anvil.server.call('get_userid')
    
    form2_instance = Form2(param='an_argument')
    Globals.form2 = form2_instance

    form3_instance = Form3(param='an_argument')
    Globals.form3 = form3_instance
    
    self.audiorecord_1.init_userid(self.userid)

    self.prev = False   
    self.check_recording = False

    self.check_recording2 = False

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    form1 = self.button_1.tag
    if form1 is None:
      return
    self.flow_panel_1.clear()
    self.flow_panel_1.add_component(form1)  
    self.check_recording = False
    pass

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    form2 = self.button_2.tag
    if form2 is None:
      return    
    self.flow_panel_1.clear()
    self.flow_panel_1.add_component(form2) 
    self.check_recording = False
    pass

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    form3 = self.button_3.tag
    if form3 is None:
      return
    self.flow_panel_1.clear()
    self.flow_panel_1.add_component(form3)
    self.check_recording = False
    pass

  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    if self.check_recording == True:
      isrecording = anvil.js.call_js('get_startrecording_disabled') 
      #print(isrecording)
      if (self.prev == True and isrecording == False):
        Globals.form2.record_answer_clicked()
      
      self.prev = isrecording
      








