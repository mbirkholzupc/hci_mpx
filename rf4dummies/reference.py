from kivy.properties import StringProperty

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase


# Extend Kivy classes
class ReferencePage(MDBoxLayout):
  pass


class RefTab(MDFloatLayout, MDTabsBase):
  content_text = StringProperty("")
