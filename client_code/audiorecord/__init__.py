from ._anvil_designer import audiorecordTemplate
from anvil import *

class audiorecord(audiorecordTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.