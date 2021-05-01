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
from kivymd.uix.list import OneLineIconListItem

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

        return self.screen

    def clock_callback(self, dt):
        self.i = self.i+1
        #self.screen.ids.text2.text = 'Clock call: {}'.format(self.i)


if __name__ == '__main__':
    MainApp().run()
