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


from plyer import accelerometer


# Extend Kivy classes
class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()


class GyroscopeInterface(MDBoxLayout):

    x_calib = NumericProperty(0)
    y_calib = NumericProperty(0)
    z_calib = NumericProperty(0)
    x_speed = NumericProperty(0)
    y_speed = NumericProperty(0)
    z_speed = NumericProperty(0)
    x_drift = NumericProperty(0)
    y_drift = NumericProperty(0)
    z_drift = NumericProperty(0)

    facade = ObjectProperty()

    def enable(self):
        self.facade.enable()
        Clock.schedule_interval(self.get_rotation, 1 / 20.)
        Clock.schedule_interval(self.get_rotation_uncalib, 1 / 20.)

    def disable(self):
        self.facade.disable()
        Clock.unschedule(self.get_rotation)
        Clock.unschedule(self.get_rotation_uncalib)

    def get_rotation(self, dt):
        if self.facade.rotation != (None, None, None):
            self.x_calib, self.y_calib, self.z_calib = self.facade.rotation

    def get_rotation_uncalib(self, dt):
        empty = tuple([None for i in range(6)])

        if self.facade.rotation_uncalib != empty:
            self.x_speed, self.y_speed, self.z_speed, self.x_drift,\
                self.y_drift, self.z_drift = self.facade.rotation_uncalib


class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


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

        self.sensorEnabled = False

        self.screen = Builder.load_file('appdesign.kv')

        self.theme_cls = ThemeManager()
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.accent_palette = 'Teal'

        self.screen.ids.box3.add_widget(
            MDLabel(
                text='Label added programatically in build',
                halign='center',
            )
        )

        Clock.schedule_interval(self.clock_callback, 1)     # call every 1 second

        return self.screen

    def do_toggle(self):
        try:
            if not self.sensorEnabled:
                print("[debug] sensorEnabled False")
                print("[debug] accelerometer.enable()")
                accelerometer.enable()
                Clock.schedule_interval(self.get_acceleration, 1 / 20.)

                self.sensorEnabled=True
                self.screen.ids.toggle_button.text="Stop Accelerometer"
            else:
                accelerometer.disable()
                Clock.unschedule(self.get_acceleration)

                self.sensorEnabled=False
                self.screen.ids.toggle_button.text="Start Accelerometer"
        except:
            import traceback
            traceback.print_exc()
            status="Accelerometer is not implemented for your platform"
            self.screen.ids.accel_status.text=status

    def get_acceleration(self, dt):
        val=accelerometer.acceleration[:3]

        if not val == (None, None, None):
            self.screen.ids.x_label.text="X: " + str(val[0])
            self.screen.ids.y_label.text="Y: " + str(val[1])
            self.screen.ids.z_label.text="Z: " + str(val[2])

    def clock_callback(self, dt):
        self.i = self.i+1
        self.screen.ids.text2.text = 'Clock call: {}'.format(self.i)


if __name__ == '__main__':
    MainApp().run()