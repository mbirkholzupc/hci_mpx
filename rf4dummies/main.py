###############################################################################
# File:    main.py
# Purpose: Definitions of main app layout, navigation bar and settings
###############################################################################

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty

from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList
from kivymd.uix.list import OneLineListItem
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.menu import MDDropdownMenu

from reference import ReferencePage
from training import TrainingPage
from checklist import ChecklistPage
from alignment import AntennaAlignmentHelperPage

# Extend Kivy classes
class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()

class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class AboutPage(MDBoxLayout):
  pass

class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        '''Called when tap on a menu item.'''

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color

# Main Kivy Application
class MainApp(MDApp):
    def build(self):
        self.i = 0  # clock counter

        self.theme_cls = ThemeManager()
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Blue'
        # Can't see "Teal" in MDTabs against blue background, so commenting out (defaults to "Amber")
        #self.theme_cls.accent_palette = 'Teal'

        self.screen = Builder.load_file('appdesign.kv')
        self.theme_cls.theme_style = 'Light'    # dirty workaround for toolbar right icons

        """
        self.screen.ids.box3.add_widget(
            MDLabel(
                text='Label added programatically in build',
                halign='center',
            )
        )
        """

        Clock.schedule_interval(self.clock_callback, 1)     # call every 1 second

        # Build settings menu
        settings_menu_items = [
          {
            "viewclass": "OneLineListItem",
            "text": f"{item_name}",
            "on_release": lambda x=f"{item_name}": self.settings_menu_callback(x),
          } for item_name in ['Language', 'Settings']
        ]
        self.settings_menu = MDDropdownMenu(
          caller=self.screen.ids.settings_menu_button,
          items=settings_menu_items,
          width_mult=4,
        )

        return self.screen

    def clock_callback(self, dt):
        self.i = self.i+1
        #self.screen.ids.text2.text = 'Clock call: {}'.format(self.i)

    def settings_menu_open_callback(self,button):
      self.settings_menu.caller = button
      self.settings_menu.open()

    def switch_theme_style(self):
        self.theme_cls.theme_style = (
            'Light' if self.theme_cls.theme_style == 'Dark' else 'Dark'
        )
        
    def settings_menu_callback(self,instance_menu):
      print(f'{instance_menu}')    
      self.settings_menu.dismiss()

if __name__ == '__main__':
    MainApp().run()
