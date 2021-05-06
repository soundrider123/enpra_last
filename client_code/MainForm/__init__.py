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
from EnPra import Globals

class MainForm(MainFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    dic1 = anvil.server.call("loadtopic")
    self.repeating_panel_1.items = dic1
    Globals.mainform = self

  def change_content(self, topic_id):
    form1_instance = Form1(param='an_argument')
    form1_instance.init(topic_id)
    self.flow_panel_1.clear()
    self.flow_panel_1.add_component(form1_instance)
    