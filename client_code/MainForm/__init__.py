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
    userid = anvil.server.call('get_userid')
    print(userid)
    self.audiorecord_1.init_userid(userid)

