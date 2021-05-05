from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.list import OneLineListItem
from kivy.uix.scrollview import ScrollView

# Global data
reference_page_widgets = {}

# Extend Kivy classes
class ReferencePage(MDBoxLayout):
    pass

class ReferenceArticlePicAndText(MDBoxLayout):
    pass

class RefIndex(MDBoxLayout):
    pass

class RefTab(MDFloatLayout, MDTabsBase):
    content_text = StringProperty("")

class RefWavelengthPage(MDBoxLayout):
      pass

class RefPolarizationPage(MDBoxLayout):
    pass

# Global functions
def build_ref_index(app,index_map):
    for entry in index_map:
        # Instantiate a widget for each page and then we hook/unhook them at runtime
        reference_page_widgets[entry] = Builder.load_file(index_map[entry])

        app.screen.ids.ref_article_list.add_widget(
            OneLineListItem(text=entry, on_release=app.load_reference_page)
        )
