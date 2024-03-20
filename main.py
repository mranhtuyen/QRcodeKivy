from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from pyzbar.pyzbar import decode
from PIL import Image as PilImage
import requests
import json
import cv2

class MyApp(App):
    def build(self):
        self.icon = "icon.png"
        self.title = "Latafe QR Code Scan Menu"
        self.layout = BoxLayout(orientation='vertical')
        self.button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        self.textbox1 = TextInput(hint_text='Nhập mã QR hoặc quét mã QR')
        self.layout.add_widget(self.textbox1)
        self.button1 = Button(text='Quét mã QR')
        self.button1.bind(on_press=self.scan_qr_code)
        self.button_layout.add_widget(self.button1)
        self.button2 = Button(text='Chọn File ảnh')
        self.button2.bind(on_press=self.select_image_file)
        self.button_layout.add_widget(self.button2)
        self.button3 = Button(text='Tìm kiếm')
        self.button3.bind(on_press=self.search_product)
        self.button_layout.add_widget(self.button3)
        self.layout.add_widget(self.button_layout)
        self.result_layout = GridLayout(cols=2)
        self.layout.add_widget(self.result_layout)
        return self.layout

    def scan_qr_code(self, instance):
        
        if not cv2.VideoCapture(0).isOpened():
            print('Bạn không có camera')
            return
       
        cap = cv2.VideoCapture(0)
        while True:
            _, frame = cap.read()
            decoded_objects = decode(frame)
            for obj in decoded_objects:
                self.textbox1.text = obj.data.decode('utf-8')
                break
            if decoded_objects:
                break
        cap.release()
        cv2.destroyAllWindows()

    def select_image_file(self, instance):
        content = FileChooserIconView(path='.')
        popup = Popup(title="Chọn một file ảnh", content=content, size_hint=(0.9, 0.9))
        content.bind(on_submit=lambda instance: self.scan_image_file(content.selection[0]))
        popup.open()

    def select_image_file(self, instance):
        content = FileChooserIconView(path='.')
        popup = Popup(title="Chọn một file ảnh", content=content, size_hint=(0.9, 0.9))
        content.bind(on_submit=lambda instance, selection, touch: self.scan_image_file(selection[0]))
        popup.open()

    def search_product(self, instance):
        term = self.textbox1.text
        self.textbox1.text = '' 
        response = requests.get(f'http://tuyenkat.mywire.org:8484/appcreated/search_product_app.php?term={term}')
        data = json.loads(response.text)
        # Xóa kết quả tìm kiếm cũ
        self.result_layout.clear_widgets()
        for product in data:
            name_label = Label(text=f"Name: {product['Name']}", size_hint_y=None)
            qr_label = Label(text=f"QRcode: {product['QRcode']}", size_hint_y=None)
            image = AsyncImage(source=product['Image'], size_hint=(None, None), size=(300, 200), allow_stretch=True)
            desc_label = Label(text=f"Description: {product['Description']}", text_size=(400, None), size_hint_y=None)
            self.result_layout.add_widget(name_label)
            self.result_layout.add_widget(qr_label)
            self.result_layout.add_widget(image)
            self.result_layout.add_widget(desc_label)

if __name__ == '__main__':
    MyApp().run()