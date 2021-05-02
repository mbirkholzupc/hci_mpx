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

        self.screen = Builder.load_file('appdesign.kv')

        self.theme_cls = ThemeManager()
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.accent_palette = 'Teal'

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
        # TODO: I can't get the callbacks to work when clicking on a menu item.
        # Online, there seems to be two different API versions that are referenced in
        # various forums. Unfortunately, if I install the latest KivyMD from master, which
        # is one of the solutions to the callback problem, it breaks the NavigationLayout.
        # So, sticking with 0.104.1 for now
        # The new API version associates the on_release callback with the menu instead of each
        # menu item
        settings_menu_items = [
          {
            "viewclass": "OneLineListItem",
            "text": f"{item_name}",
            "on_release": lambda x=f"{item_name}": self.settings_menu_callback(x),
          } for item_name in ['Language', 'Day/Night Mode', 'Other Thing']
        ]
        self.settings_menu = MDDropdownMenu(
          caller=self.screen.ids.settings_menu_button,
          items=settings_menu_items,
          width_mult=4,
        )
        # This is sort of in the new API style. We can delete it once callbacks work
        #self.settings_menu.bind(on_release=self.settings_menu_callback)

        return self.screen

    def clock_callback(self, dt):
        self.i = self.i+1
        #self.screen.ids.text2.text = 'Clock call: {}'.format(self.i)

    def settings_menu_open_callback(self,button):
      self.settings_menu.caller = button
      self.settings_menu.open()

    def settings_menu_callback(self,instance_menu,instance_menu_items):
      # text_item should contain the item that was clicked in case we should handle it here
      # TODO: This doesn't seem to be getting called. WHY????
      print('CLOSE')
      print(f'{instance_menu_item}')
      self.settings_menu.dismiss()
      print('close cb')

if __name__ == '__main__':
    MainApp().run()
