from ._anvil_designer import ProfileFormTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ProfileForm(ProfileFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    lst_dic = anvil.server.call('get_history')
    self.repeating_panel_1.items = lst_dic     
    
  def refresh(self):
    lst_dic = anvil.server.call('get_history')
    self.repeating_panel_1.items = lst_dic     
    