from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.textinput import TextInput



store = JsonStore("todo_data.json")


class Custombtn(Button):
    key_name = StringProperty()


class Interface(ScreenManager):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        Clock.schedule_once(self.fetching_data)

    def truncate_title(self, input_title, max_len):
        str_end = "...."
        length = len(input_title)

        if length > max_len:
            return input_title[:max_len - len(str_end)] + str_end
        else:
            return input_title

    def delete_todo(self,del_obj):
        id = del_obj.key_name
        self.ids.gridLayout.remove_widget(self.ids[id])
        store.delete(id)


    def fetching_data(self,dt):
        try:
            keys = store.keys()
            for key in keys:
                layout = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(10))
                self.ids[key]=layout
                title = Custombtn(background_normal="images/purple.png",key_name=key,text=self.truncate_title(key,16),font_size="22sp",font_name="kivy_fonts/chrustyrock.ttf")
                delete = Custombtn(key_name=key,on_press=self.delete_todo,background_normal="images/del.jpg", size_hint=(None, None), size=(dp(60), dp(60)))
                title.bind(on_press=self.detail_screen)
                layout.add_widget(title)
                layout.add_widget(delete)
                self.ids.gridLayout.add_widget(layout)

        except:
            print("Storage is empty")


    def back_btn(self):
        self.current = "Main Screen"
        store.put(self.ids.todoTitle.text, data=self.ids.taskData.text)

    def detail_screen(self,obj):
        self.ids.todoTitle.text = obj.key_name
        self.current = "Details Screen"
        self.ids.taskData.text = store.get(obj.key_name)["data"]

    def addItem(self,obj):
        self.popup.dismiss()
        layout = BoxLayout(size_hint_y=None, height=dp(60),spacing=dp(10))
        title = Custombtn(background_normal="images/purple.png",key_name =self.textInput.text ,text=self.truncate_title(self.textInput.text,16),font_size="22sp",font_name="kivy_fonts/chrustyrock.ttf")
        delete = Custombtn(key_name =self.textInput.text ,on_press=self.delete_todo,background_normal="images/del.jpg", size_hint=(None,None), size=(dp(60),dp(60)))
        title.bind(on_press=self.detail_screen)
        self.ids[self.textInput.text] = layout
        layout.add_widget(title)
        layout.add_widget(delete)
        self.ids.gridLayout.add_widget(layout)
        store.put(self.textInput.text, data="")

    def show_popup(self):
        layout=BoxLayout(orientation="vertical", padding=dp(16),spacing=dp(10))
        btn=Button(background_normal="images/blue.png",text="Submit",font_name="kivy_fonts/chrustyrock.ttf",size_hint=(0.6,None),height=dp(40),pos_hint={"center_x": 0.5})
        btn.bind(on_press=self.addItem)
        self.textInput = TextInput(multiline=False,font_size="18sp",font_name="kivy_fonts/chrustyrock.ttf", height=dp(25))
        layout.add_widget(self.textInput)
        layout.add_widget(btn)
        self.popup=Popup(title="To Do Title", title_font="kivy_fonts/shortbaby.ttf" ,size_hint=(0.8,None), height=dp(180), content=layout)
        self.popup.open()
class TodoApp(App):
    pass

TodoApp().run()