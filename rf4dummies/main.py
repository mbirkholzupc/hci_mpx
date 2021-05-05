#!/usr/bin/env python

# coding: utf-8


###############################################################################
# File:    main.py
# Purpose: Definitions of main app layout, navigation bar and settings
###############################################################################

import gettext
from os.path import dirname, join

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
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import OneLineAvatarIconListItem

from kivy.lang import Observable
from kivy.properties import StringProperty

from reference import ReferencePage, reference_page_widgets
from training import TrainingPage
from checklist import ChecklistPage
from alignment import AntennaAlignmentHelperPage

from reference import build_ref_index

# https://github.com/tito/kivy-gettext-example/blob/master/main.py
class Lang(Observable):
    observers = []
    lang = None

    def __init__(self, defaultlang):
        super(Lang, self).__init__()
        self.ugettext = None
        self.lang = defaultlang
        self.switch_lang(self.lang)

    def _(self, text):
        return self.ugettext(text)

    def fbind(self, name, func, args, **kwargs):
        if name == "_":
            self.observers.append((func, args, kwargs))
        else:
            return super(Lang, self).fbind(name, func, *args, **kwargs)

    def funbind(self, name, func, args, **kwargs):
        if name == "_":
            key = (func, args, kwargs)
            if key in self.observers:
                self.observers.remove(key)
        else:
            return super(Lang, self).funbind(name, func, *args, **kwargs)

    def switch_lang(self, lang):
        # get the right locales directory, and instanciate a gettext
        locales = gettext.translation('base', 'locales', languages=[lang])
        self.ugettext = locales.gettext
        self.lang = lang

        # update all the kv rules attached to this text
        for func, largs, kwargs in self.observers:
            func(largs, None, None)
            
# Default language
tr = Lang("en")

# Reference page index/content map - should really go in reference file, but would require
# turning Lang into a singleton, so let's just shove it here
reference_index_map = {
        tr._('Wavelength'): 'ref_wavelength.kv',
        tr._('Polarization'): 'ref_polarization.kv',
    }


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

class ItemConfirm(OneLineAvatarIconListItem):
    divider = None
    
    lang_dict = {'English': 'en', 'Català': 'ca', 'Français': 'fr', 'Español': 'es'}

    def set_icon(self, instance_check):
        tr.switch_lang(self.lang_dict[self.text])
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False
                
# Main Kivy Application
class MainApp(MDApp):
    def build(self):
        self.i = 0  # clock counter
        
        self.lang_dialog = None
        self.settings_dialog = None
        
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
        settings_dict = {'lang': tr._('Language'), 'settings': tr._('Settings')}
        settings_menu_items = [
          {
            "viewclass": "OneLineListItem",
            "text": f"{settings_dict[item_id]}",
            "on_release": lambda x=f"{item_id}": self.settings_menu_callback(x),
          } for item_id in settings_dict
        ]
        self.settings_menu = MDDropdownMenu(
          caller=self.screen.ids.settings_menu_button,
          items=settings_menu_items,
          width_mult=4,
        )

        # Build index on reference page
        build_ref_index(self,reference_index_map)

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
      if instance_menu == 'lang':
        self.settings_menu.dismiss()
        self.show_confirmation_dialog()
        
    def close_lang_dialog(self, obj):
      self.lang_dialog.dismiss()
        
    def close_settings_dialog(self, obj):
      self.settings_dialog.dismiss()
        
    def show_confirmation_dialog(self):
        ok_button = MDFlatButton(text=tr._('Ok'), on_release=self.close_lang_dialog)
        if not self.lang_dialog:
            self.lang_dialog = MDDialog(
                auto_dismiss=True,
                title=tr._('Select language'),
                type="confirmation",
                #events_callback = self.close_lang_select,
                items=[
                    ItemConfirm(text='English'),
                    ItemConfirm(text='Català'),
                    ItemConfirm(text='Français'),
                    ItemConfirm(text='Español'),
                ],
                buttons=[ok_button],
            )
        self.lang_dialog.open()
        
    def show_settings_dialog(self):
      ok_button = MDFlatButton(text=tr._('Ok'), on_release=self.close_settings_dialog)
      if not self.settings_dialog:
          self.settings_dialog = MDDialog(
              auto_dismiss=True,
              title=tr._('Settings'),
              #type="confirmation",
              #events_callback = self.close_lang_select,
              buttons=[ok_button],
          )
      self.settings_dialog.open()

    def load_reference_page(self,pagename):
        # Unload the current article
        for w in self.screen.ids.article_container.children:
            self.screen.ids.article_container.remove_widget(w)

        # Load the new one
        newarticle = reference_page_widgets[pagename.text]
        self.screen.ids.article_container.add_widget(newarticle)

        # Move to the content tab automatically
        #self.screen.ids.ref_tabs.switch_tab('\n'+tr._(Content))
        print(self.screen.ids.ref_tabs.get_tab_list())
        print(self.screen.ids.ref_tabs.get_tab_list()[0].__dict__)
        print(self.screen.ids.content_tab)
        print(self.screen.ids.content_tab.__dict__)
        #TODO: No idea how to do this. Everything seems to fail, but leaving my attempts
        #      around for the future when trying this again.
        #self.screen.ids.ref_tabs.switch_tab(self.screen.ids.content_tab)
        #self.screen.ids.ref_tabs.switch_tab(self.screen.ids.content_tab,'ContentTab',search_by='text')
        #self.screen.ids.ref_tabs.switch_tab(self.screen.ids.content_tab)

if __name__ == '__main__':
    MainApp().run()
