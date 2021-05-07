from ._anvil_designer import Form2Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Form2(Form2Template):
  def __init__(self, **properties):
    self.last_event = None
    self.events = []
    
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    self.button_match.visible = False

    
  def init(self, title_id):
    pass

  def button_match_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def button_answer_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def button_voice_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass



