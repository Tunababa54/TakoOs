# coding: utf-8
# -*- coding: utf-8 -*-

# Gerekli Kivy modüllerini içe aktarıyoruz reis
import kivy
# Kivy versiyonunu kontrol et (Termux'ta kurulu olana göre ayarlanabilir)
# kivy.require('2.1.0') # Bu satırı Termux'taki Kivy versiyonuna göre ayarlaman gerekebilir

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.utils import platform # Hangi platformda çalıştığını anlamak için
from kivy.clock import Clock # Zamanlanmış görevler için

import os # Sistem komutları için
import subprocess # Harici komut çalıştırmak için
import sys # Sistem bilgileri için
import time # Zaman fonksiyonları için
import threading # Arka planda işlem yapmak için (UI'ı bloklamamak adına)


# Pencere boyutunu responsive yapmak için (Termux'ta tam ekran olur genelde)
# Amaç farklı cihazlarda da uyumlu olması
# Window.size = (360, 640) # Varsayılan küçük boyut, Termux tam ekran yapar
# Termux'ta tam ekran için aşağıdaki satırları kullanabilirsin:
# from jnius import autoclass
# PythonActivity = autoclass('org.kivy.android.PythonActivity')
# activity = PythonActivity.mActivity
# Window.size = (activity.getWindowManager().getDefaultDisplay().getWidth(), activity.getWindowManager().getDefaultDisplay().getHeight())


# Sistem renkleri (isteğe bağlı, KivyMD kullanıyorsan tema daha iyi olur)
BG_COLOR = (0.1, 0.1, 0.1, 1) # Koyu arka plan
PRIMARY_COLOR = (0.0, 0.6, 0.8, 1) # Mavi/Turkuaz vurgu
ACCENT_COLOR = (0.8, 0.5, 0.0, 1) # Turuncu vurgu
TEXT_COLOR = (1, 1, 1, 1) # Beyaz yazı
ERROR_COLOR = (1, 0, 0, 1) # Kırmızı hata rengi
SUCCESS_COLOR = (0, 1, 0, 1) # Yeşil başarı rengi


# Ana ScreenManager sınıfı, ekranlar arası geçişi yönetecek reis
class TakoOSScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ekranları buraya ekleyeceğiz sırayla

# Boot Splash Ekranı
class BootSplash(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ekranın arka plan rengini ayarla
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))
        self.bind(size=self._update_bg, pos=self._update_bg)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10,
                           halign='center', valign='middle') # Ortala reis
        # layout.bind(size=layout.setter('pos')) # Boyut değiştikçe pozisyonu güncelle

        # Logo (varsa)
        try:
            # Logo dosyasının varlığını kontrol et
            if os.path.exists('data/logo.png'):
                logo = Image(source='data/logo.png', size_hint=(0.5, 0.5),
                             pos_hint={'center_x': 0.5, 'center_y': 0.6}) # Ortaya koy
                layout.add_widget(logo)
            else:
                 # Logo bulunamazsa sadece yazı göster
                print("Logo dosyası bulunamadı: data/logo.png")
                logo_label = Label(text='[b]TakoOS PyCore™[/b]', font_size='30sp',
                                   markup=True, size_hint_y=None, height=50, color=TEXT_COLOR)
                layout.add_widget(logo_label)
        except Exception as e:
            # Logo yüklenirken hata olursa
            print(f"Logo yüklenemedi: {e}")
            logo_label = Label(text='[b]TakoOS PyCore™[/b]', font_size='30sp',
                               markup=True, size_hint_y=None, height=50, color=TEXT_COLOR)
            layout.add_widget(logo_label)


        # Yükleniyor yazısı
        loading_label = Label(text='Sistem Başlatılıyor...', size_hint_y=None, height=40, color=TEXT_COLOR)
        layout.add_widget(loading_label)

        self.add_widget(layout)

        # Bir süre sonra ana menüye geç
        # Termux'ta delay vermek için threading veya Clock kullanmak daha doğru
        Clock.schedule_once(self.go_to_main, 3) # 3 saniye sonra geç

    # Arka planı güncelleme fonksiyonu
    def _update_bg(self, instance, value):
        self.canvas.before.clear()
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))


    # Ana menüye geçiş fonksiyonu
    def go_to_main(self, dt):
        self.manager.current = 'main' # Ana menü ekranına geç


# Ana Menü Ekranı
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ekranın arka plan rengini ayarla
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))
        self.bind(size=self._update_bg, pos=self._update_bg)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Başlık
        title_label = Label(text='[b]TakoOS PyCore™[/b]\nAna Menü', font_size='24sp',
                            halign='center', valign='middle', markup=True,
                            size_hint_y=None, height=80, color=TEXT_COLOR)
        layout.add_widget(title_label)

        # Butonlar için grid layout
        button_grid = GridLayout(cols=2, spacing=10, size_hint_y=1) # Ekranın geri kalanını kapla

        # Butonları ekle
        btn_app_launcher = Button(text='Uygulama Başlatıcı', on_press=self.go_to_app_launcher)
        btn_file_manager = Button(text='Dosya Yöneticisi', on_press=self.go_to_file_manager)
        btn_terminal = Button(text='Terminal', on_press=self.go_to_terminal)
        btn_pentest = Button(text='Siber Güvenlik Araçları', on_press=self.go_to_pentest_menu)
        btn_power_menu = Button(text='Güç Seçenekleri', on_press=self.go_to_power_menu)
        btn_exit = Button(text='Çıkış', on_press=self.confirm_exit) # Çıkış onayı

        button_grid.add_widget(btn_app_launcher)
        button_grid.add_widget(btn_file_manager)
        button_grid.add_widget(btn_terminal)
        button_grid.add_widget(btn_pentest)
        button_grid.add_widget(btn_power_menu)
        button_grid.add_widget(btn_exit)

        layout.add_widget(button_grid)
        self.add_widget(layout)

    # Arka planı güncelleme fonksiyonu
    def _update_bg(self, instance, value):
        self.canvas.before.clear()
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))

    # Uygulama Başlatıcı ekranına geçiş
    def go_to_app_launcher(self, instance):
        print("Uygulama Başlatıcıya gidiliyor...")
        self.manager.current = 'app_launcher'

    # Dosya Yöneticisi ekranına geçiş
    def go_to_file_manager(self, instance):
        print("Dosya Yöneticisine gidiliyor...")
        self.manager.current = 'file_manager'

    # Terminal ekranına geçiş
    def go_to_terminal(self, instance):
        print("Terminale gidiliyor...")
        self.manager.current = 'terminal'

    # Siber Güvenlik Araçları menüsüne geçiş
    def go_to_pentest_menu(self, instance):
        print("Siber Güvenlik Araçları menüsüne gidiliyor...")
        self.manager.current = 'pentest_menu'

    # Güç Seçenekleri menüsüne geçiş
    def go_to_power_menu(self, instance):
        print("Güç Seçenekleri menüsüne gidiliyor...")
        self.manager.current = 'power_menu'

    # Çıkış onayı popup'ını göster
    def confirm_exit(self, instance):
        App.get_running_app().show_exit_popup()


# Uygulama Başlatıcı Ekranı (Yer Tutucu)
class AppLauncherScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ekranın arka plan rengini ayarla
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))
        self.bind(size=self._update_bg, pos=self._update_bg)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Başlık
        title_label = Label(text='[b]Uygulama Başlatıcı[/b]', font_size='24sp',
                            halign='center', valign='middle', markup=True,
                            size_hint_y=None, height=60, color=TEXT_COLOR)
        layout.add_widget(title_label)

        # Açıklama yazısı
        info_label = Label(text='Bu bölüm Termux içindeki uygulamaları/scriptleri başlatmak için tasarlanmıştır.\nŞu an geliştirme aşamasındadır reis.',
                           halign='center', valign='middle', size_hint_y=None, height=100, color=TEXT_COLOR)
        layout.add_widget(info_label)

        # Ana Menüye Dön butonu
        btn_back = Button(text='Ana Menüye Dön', size_hint_y=None, height=50, on_press=self.go_back)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    # Arka planı güncelleme fonksiyonu
    def _update_bg(self, instance, value):
        self.canvas.before.clear()
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))

    # Ana menüye geri dönüş fonksiyonu
    def go_back(self, instance):
        self.manager.current = 'main'


# Dosya Yöneticisi Ekranı
class FileManagerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ekranın arka plan rengini ayarla
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))
        self.bind(size=self._update_bg, pos=self._update_bg)

        self.current_path = '/' # Başlangıç dizini kök dizin olsun reis
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Başlık ve geçerli yol göstergesi
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        self.path_label = Label(text=f'Yol: {self.current_path}', size_hint_x=1, color=TEXT_COLOR)
        btn_up_dir = Button(text='Yukarı', size_hint_x=None, width=100, on_press=self.go_up_directory)
        header_layout.add_widget(self.path_label)
        header_layout.add_widget(btn_up_dir)
        self.layout.add_widget(header_layout)

        # Dosya ve Klasör Listesi için ScrollView
        self.file_list_layout = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)
        self.file_list_layout.bind(minimum_height=self.file_list_layout.setter('height')) # İçerik değiştikçe yüksekliği ayarla

        self.scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        self.scroll_view.add_widget(self.file_list_layout)
        self.layout.add_widget(self.scroll_view)

        # Ana Menüye Dön butonu
        btn_back = Button(text='Ana Menüye Dön', size_hint_y=None, height=50, on_press=self.go_back)
        self.layout.add_widget(btn_back)

        self.add_widget(self.layout)

        # Ekran ilk açıldığında dizini listele
        self.list_directory(self.current_path)

    # Arka planı güncelleme fonksiyonu
    def _update_bg(self, instance, value):
        self.canvas.before.clear()
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))

    # Belirtilen dizini listeleme fonksiyonu
    def list_directory(self, path):
        self.file_list_layout.clear_widgets() # Önceki listeyi temizle
        self.current_path = path
        self.path_label.text = f'Yol: {self.current_path}' # Yol etiketini güncelle

        # Dizindeki öğeleri listele (root yetkisi gerekebilir)
        try:
            # Root erişimi için 'tsu' veya 'sudo' kullanabiliriz.
            # Termux'ta 'tsu' daha yaygın.
            # Güvenlik açısından doğrudan os.listdir kullanmak daha iyidir eğer Termux'un kendisi rootluysa.
            # Eğer Termux tsu ile root yetkisi almışsa, dosyalara normalde erişebilir.
            # Riskli komut çalıştırmamak adına doğrudan Python'ın dosya sistemini kullanıyoruz.
            items = sorted(os.listdir(path)) # Öğeleri alfabetik sırala

            # Klasörleri önce listele
            directories = [d for d in items if os.path.isdir(os.path.join(path, d))]
            files = [f for f in items if os.path.isfile(os.path.join(path, f))]

            for item in directories:
                btn = Button(text=f'Klasör: {item}', size_hint_y=None, height=50,
                             on_press=lambda instance, p=os.path.join(path, item): self.list_directory(p)) # Klasöre tıklayınca içine gir
                self.file_list_layout.add_widget(btn)

            for item in files:
                btn = Button(text=f'Dosya: {item}', size_hint_y=None, height=50,
                             on_press=lambda instance, p=os.path.join(path, item): self.view_file_content(p)) # Dosyaya tıklayınca içeriğini göster
                self.file_list_layout.add_widget(btn)

        except PermissionError:
            # İzin hatası olursa bilgilendir
            error_label = Label(text='İzin reddedildi reis! Bu dizine erişmek için root yetkisi gerekebilir.', color=ERROR_COLOR)
            self.file_list_layout.add_widget(error_label)
        except FileNotFoundError:
             # Dizin bulunamazsa
            error_label = Label(text='Dizin bulunamadı reis!', color=ERROR_COLOR)
            self.file_list_layout.add_widget(error_label)
            # Güvenlik için bir üst dizine dönmeye çalışabiliriz
            self.go_up_directory(None)
        except Exception as e:
            # Diğer hatalar
            error_label = Label(text=f'Bir hata oluştu reis: {e}', color=ERROR_COLOR)
            self.file_list_layout.add_widget(error_label)


    # Bir üst dizine gitme fonksiyonu
    def go_up_directory(self, instance):
        parent_dir = os.path.dirname(self.current_path)
        if parent_dir != self.current_path: # Kök dizinde değilsek
            self.list_directory(parent_dir)

    # Dosya içeriğini görüntüleme fonksiyonu
    def view_file_content(self, filepath):
        try:
            # Büyük dosyalar veya ikili dosyalar sorun yaratabilir, okuma boyutunu sınırlayalım
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(2048) # İlk 2KB'ı oku reis
                if len(content) == 2048:
                    content += "\n\n[... Dosyanın tamamı görüntülenemedi, çok büyük olabilir veya ikili dosya olabilir reis ...]"

            # Popup ile içeriği göster
            content_label = Label(text=content, size_hint_y=None, size_hint_x=1,
                                  text_size=(Window.width * 0.9 - 20, None), # Popup genişliğine göre ayarla
                                  valign='top', halign='left', color=TEXT_COLOR)
            content_label.bind(texture_size=content_label.setter('size')) # İçerik değiştikçe label boyutunu ayarla

            scroll_view_content = ScrollView(size_hint=(1, 0.8))
            scroll_view_content.add_widget(content_label)

            close_button = Button(text='Kapat', size_hint_y=None, height=50, on_press=lambda x: popup.dismiss())

            box = BoxLayout(orientation='vertical', spacing=10, padding=10)
            box.add_widget(Label(text=f'Dosya İçeriği: {os.path.basename(filepath)}', size_hint_y=None, height=40, color=TEXT_COLOR))
            box.add_widget(scroll_view_content)
            box.add_widget(close_button)

            popup = Popup(title='Dosya Görüntüleyici', content=box, size_hint=(0.9, 0.9))
            popup.open()

        except PermissionError:
            self.show_info_popup("Hata!", "Dosyayı okumak için iznin yok reis.")
        except FileNotFoundError:
             self.show_info_popup("Hata!", "Dosya bulunamadı reis.")
        except Exception as e:
            self.show_info_popup("Hata!", f"Dosya okunurken bir hata oluştu reis: {e}")

    # Basit bilgi popup'ı gösterme fonksiyonu
    def show_info_popup(self, title, text):
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        box.add_widget(Label(text=text, size_hint_y=None, height=40, color=TEXT_COLOR))
        close_button = Button(text='Tamam', size_hint_y=None, height=40, on_press=lambda x: popup.dismiss())
        box.add_widget(close_button)
        popup = Popup(title=title, content=box, size_hint=(0.7, 0.3))
        popup.open()


    # Ana menüye geri dönüş fonksiyonu
    def go_back(self, instance):
        self.manager.current = 'main'


# Terminal Ekranı
class TerminalScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ekranın arka plan rengini ayarla
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))
        self.bind(size=self._update_bg, pos=self._update_bg)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Başlık
        title_label = Label(text='[b]Terminal[/b]', font_size='24sp',
                            halign='center', valign='middle', markup=True,
                            size_hint_y=None, height=60, color=TEXT_COLOR)
        layout.add_widget(title_label)

        # Komut çıktısı alanı
        self.output_textinput = TextInput(readonly=True, multiline=True, size_hint=(1, 1),
                                          background_color=(0.2, 0.2, 0.2, 1), foreground_color=TEXT_COLOR,
                                          font_name='monospace', # Terminal fontu
                                          cursor_color=(1,1,1,1))
        scroll_view_output = ScrollView(size_hint=(1, 1))
        scroll_view_output.add_widget(self.output_textinput)
        layout.add_widget(scroll_view_output)

        # Komut giriş alanı ve Çalıştır butonu
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        self.command_input = TextInput(hint_text='Komut Girin...', size_hint_x=1,
                                       multiline=False, write_tab=False) # Tek satır
        btn_execute = Button(text='Çalıştır', size_hint_x=None, width=100, on_press=self.execute_command)
        input_layout.add_widget(self.command_input)
        input_layout.add_widget(btn_execute)
        layout.add_widget(input_layout)


        # Ana Menüye Dön butonu
        btn_back = Button(text='Ana Menüye Dön', size_hint_y=None, height=50, on_press=self.go_back)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    # Arka planı güncelleme fonksiyonu
    def _update_bg(self, instance, value):
        self.canvas.before.clear()
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))

    # Komut çalıştırma fonksiyonu
    def execute_command(self, instance):
        command = self.command_input.text.strip() # Boşlukları temizle
        if not command:
            self.output_textinput.text += "\n[Hata] Lütfen bir komut girin reis."
            self.output_textinput.foreground_color = ERROR_COLOR
            return

        self.output_textinput.text += f"\n$ {command}\n" # Çalıştırılan komutu göster
        self.output_textinput.foreground_color = TEXT_COLOR # Rengi sıfırla

        # Komutu ayrı bir thread'de çalıştır ki UI donmasın
        threading.Thread(target=self._run_command_in_thread, args=(command,)).start()

    # Komutu ayrı thread'de çalıştıran yardımcı fonksiyon
    def _run_command_in_thread(self, command):
        try:
            # subprocess ile komutu çalıştır
            # shell=True kullanırken dikkatli ol, güvenlik riski oluşturabilir
            # Güvenli yollar için shell=False ve komut argümanlarını liste olarak vermek gerekir
            # Ancak Termux ortamında ve basit kullanım için shell=True çoğu zaman yeterli
            # capture_output=True çıktıyı yakalamak için
            # text=True çıktıyı metin olarak almak için (Python 3.7+)
            # encoding='utf-8' karakter sorunlarını önlemek için
            # errors='ignore' hata olursa yoksay

            # Termux'ta root komutları için 'tsu' kullanmak gerekebilir
            # Örnek: command = f'tsu -c "{command}"'
            # Ancak burası genel terminal, rootlu komutları kullanıcı kendisi 'tsu' ile yazabilir.
            # Biz şimdilik doğrudan komutu çalıştıralım.

            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       text=True, encoding='utf-8', errors='ignore')

            # Çıktıyı oku ve Textinput'a yaz (Basit yöntem, büyük çıktıları yönetmek için iyileştirilebilir)
            # Gerçek zamanlı çıktı okuma Kivy event loop'u ile biraz karmaşık, basitçe bekleyelim.
            # Daha iyisi: Clock.schedule_interval ile çıktı borusunu okumak.
            stdout, stderr = process.communicate(timeout=60) # 60 saniye timeout

            # Çıktıyı ana UI thread'inde güncelle
            Clock.schedule_once(lambda dt: self._update_output(stdout, stderr), 0)


        except FileNotFoundError:
            Clock.schedule_once(lambda dt: self._update_output(None, "[Hata] Komut bulunamadı reis! Doğru yazdığına emin misin?"), 0)
        except subprocess.TimeoutExpired:
             Clock.schedule_once(lambda dt: self._update_output(None, "[Hata] Komut zaman aşımına uğradı reis."), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self._update_output(None, f"[Hata] Komut çalıştırılırken bir hata oluştu reis: {e}"), 0)

    # Çıktıyı UI'da güncelleyen fonksiyon (ana thread'de çalışmalı)
    def _update_output(self, stdout, stderr):
        if stdout:
            self.output_textinput.text += stdout
        if stderr:
            self.output_textinput.text += f"[Hata Çıktısı]\n{stderr}"
            self.output_textinput.foreground_color = ERROR_COLOR # Hata çıktısı kırmızı olsun

        self.output_textinput.text += f"\n[Komut Tamamlandı]"
        self.output_textinput.foreground_color = TEXT_COLOR # Rengi sıfırla

        # İmleci en sona kaydır (çıktıyı görmek için)
        self.output_textinput.cursor = (0, len(self.output_textinput._lines) if hasattr(self.output_textinput, '_lines') else 0)


    # Ana menüye geri dönüş fonksiyonu
    def go_back(self, instance):
        self.manager.current = 'main'


# Güç Seçenekleri Ekranı
class PowerMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ekranın arka plan rengini ayarla
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))
        self.bind(size=self._update_bg, pos=self._update_bg)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10,
                           halign='center', valign='middle') # Ortala

        # Başlık
        title_label = Label(text='[b]Güç Seçenekleri[/b]', font_size='24sp',
                            halign='center', valign='middle', markup=True,
                            size_hint_y=None, height=80, color=TEXT_COLOR)
        layout.add_widget(title_label)

        # Butonlar için layout
        button_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=200) # Butonlar için sabit yükseklik

        btn_reboot = Button(text='Yeniden Başlat', on_press=self.show_reboot_popup)
        btn_shutdown = Button(text='Kapat', on_press=self.show_shutdown_popup)
        btn_back_to_termux = Button(text='Termux\'a Dön', on_press=self.back_to_termux) # Uygulamayı kapatır aslında
        btn_back = Button(text='Ana Menüye Dön', on_press=self.go_back)

        button_layout.add_widget(btn_reboot)
        button_layout.add_widget(btn_shutdown)
        button_layout.add_widget(btn_back_to_termux)
        button_layout.add_widget(btn_back)

        layout.add_widget(button_layout)
        self.add_widget(layout)

    # Arka planı güncelleme fonksiyonu
    def _update_bg(self, instance, value):
        self.canvas.before.clear()
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))

    # Yeniden başlatma onayı popup'ı
    def show_reboot_popup(self, instance):
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        box.add_widget(Label(text='Cihazı yeniden başlatmak istediğinden emin misin reis?', size_hint_y=None, height=40, color=TEXT_COLOR))
        button_box = BoxLayout(spacing=10)
        yes_button = Button(text='Evet', on_press=self.reboot_device, size_hint_y=None, height=40)
        no_button = Button(text='Hayır', on_press=lambda x: popup.dismiss(), size_hint_y=None, height=40)
        button_box.add_widget(yes_button)
        button_box.add_widget(no_button)
        box.add_widget(button_box)

        popup = Popup(title='Yeniden Başlat', content=box, size_hint=(0.8, 0.4))
        popup.open()

    # Cihazı yeniden başlatma fonksiyonu (ROOT GEREKİR)
    def reboot_device(self, instance):
        print("Cihaz yeniden başlatılıyor...")
        # Root komutu ile yeniden başlat (Termux'ta 'su -c reboot' veya 'tsu -c reboot' deneyin)
        # Bu komut direk cihazı etkiler ve root yetkisi kesinlikle gerektirir.
        # Dikkatli kullanın reis!
        try:
            # 'tsu -c reboot' komutunu ayrı bir thread'de çalıştır ki UI donmasın
            threading.Thread(target=lambda: os.system('tsu -c reboot')).start()
            # veya threading.Thread(target=lambda: os.system('su -c reboot')).start() # Geleneksel su kullanılıyorsa
            # veya threading.Thread(target=lambda: os.system('reboot')).start() # Termux ortamı doğrudan rootlu ise
            # Komut çalıştıktan sonra uygulama muhtemelen kapanacaktır.
        except Exception as e:
            print(f"Yeniden başlatma hatası: {e}")
            self.show_info_popup("Hata!", f"Cihaz yeniden başlatılamadı reis. Root yetkisini kontrol et: {e}")

    # Kapatma onayı popup'ı
    def show_shutdown_popup(self, instance):
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        box.add_widget(Label(text='Cihazı kapatmak istediğinden emin misin reis?', size_hint_y=None, height=40, color=TEXT_COLOR))
        button_box = BoxLayout(spacing=10)
        yes_button = Button(text='Evet', on_press=self.shutdown_device, size_hint_y=None, height=40)
        no_button = Button(text='Hayır', on_press=lambda x: popup.dismiss(), size_hint_y=None, height=40)
        button_box.add_widget(yes_button)
        button_box.add_widget(no_button)
        box.add_widget(button_box)

        popup = Popup(title='Cihazı Kapat', content=box, size_hint=(0.8, 0.4))
        popup.open()


    # Cihazı kapatma fonksiyonu (ROOT GEREKİR)
    def shutdown_device(self, instance):
        print("Cihaz kapatılıyor...")
        # Root komutu ile kapat (Termux'ta 'su -c shutdown' veya 'tsu -c shutdown' deneyin)
        # Bu komut direk cihazı etkiler ve root yetkisi kesinlikle gerektirir.
        # Dikkatli kullanın reis!
        try:
            # 'tsu -c shutdown' komutunu ayrı bir thread'de çalıştır ki UI donmasın
            threading.Thread(target=lambda: os.system('tsu -c shutdown')).start()
            # veya threading.Thread(target=lambda: os.system('su -c shutdown')).start() # Geleneksel su kullanılıyorsa
            # veya threading.Thread(target=lambda: os.system('shutdown')).start() # Termux ortamı doğrudan rootlu ise
            # Komut çalıştıktan sonra uygulama muhtemelen kapanacaktır.
        except Exception as e:
            print(f"Kapatma hatası: {e}")
            self.show_info_popup("Hata!", f"Cihaz kapatılamadı reis. Root yetkisini kontrol et: {e}")

    # Termux'a dön (uygulamayı kapat)
    def back_to_termux(self, instance):
        print("Termux'a dönülüyor (Uygulama kapatılıyor)...")
        App.get_running_app().stop() # Kivy uygulamasını durdur

    # Bilgi popup'ı
    def show_info_popup(self, title, text):
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        box.add_widget(Label(text=text, size_hint_y=None, height=40, color=TEXT_COLOR))
        close_button = Button(text='Tamam', size_hint_y=None, height=40, on_press=lambda x: popup.dismiss())
        box.add_widget(close_button)
        popup = Popup(title=title, content=box, size_hint=(0.7, 0.3))
        popup.open()

    # Ana menüye geri dönüş fonksiyonu
    def go_back(self, instance):
        self.manager.current = 'main'


# Siber Güvenlik Araçları Menüsü Ekranı
class PentestMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ekranın arka plan rengini ayarla
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))
        self.bind(size=self._update_bg, pos=self._update_bg)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Başlık
        title_label = Label(text='[b]Siber Güvenlik Araçları[/b]', font_size='24sp',
                            halign='center', valign='middle', markup=True,
                            size_hint_y=None, height=60, color=TEXT_COLOR)
        layout.add_widget(title_label)

        # Araçlar için ScrollView ve GridLayout
        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        tools_grid = GridLayout(cols=1, spacing=10, size_hint_y=None) # Tek kolonlu liste
        tools_grid.bind(minimum_height=tools_grid.setter('height')) # İçerik değiştikçe yüksekliği ayarla

        # Araç butonları
        btn_sms_bomber = Button(text='1. SMS Bomber', on_press=lambda x: self.go_to_tool('sms_bomber'))
        btn_nmap = Button(text='2. Nmap', on_press=lambda x: self.go_to_tool('nmap_tool'))
        btn_bloodhound = Button(text='3. Bloodhound', on_press=lambda x: self.go_to_tool('bloodhound_tool'))
        btn_powerview = Button(text='4. PowerView', on_press=lambda x: self.go_to_tool('powerview_tool'))
        btn_hydra = Button(text='5. Hydra', on_press=lambda x: self.go_to_tool('hydra_tool'))
        btn_john = Button(text='6. John The Ripper', on_press=lambda x: self.go_to_tool('john_tool'))
        btn_sqlmap = Button(text='7. sqlmap', on_press=lambda x: self.go_to_tool('sqlmap_tool'))
        btn_burp = Button(text='8. Burp Suite', on_press=lambda x: self.go_to_tool('burp_tool'))
        btn_ffuf = Button(text='9. ffuf', on_press=lambda x: self.go_to_tool('ffuf_tool'))
        btn_aircrack = Button(text='10. Aircrack-ng', on_press=lambda x: self.go_to_tool('aircrack_tool'))


        tools_grid.add_widget(btn_sms_bomber)
        tools_grid.add_widget(btn_nmap)
        tools_grid.add_widget(btn_bloodhound)
        tools_grid.add_widget(btn_powerview)
        tools_grid.add_widget(btn_hydra)
        tools_grid.add_widget(btn_john)
        tools_grid.add_widget(btn_sqlmap)
        tools_grid.add_widget(btn_burp)
        tools_grid.add_widget(btn_ffuf)
        tools_grid.add_widget(btn_aircrack)


        scroll_view.add_widget(tools_grid)
        layout.add_widget(scroll_view)

        # Ana Menüye Dön butonu
        btn_back = Button(text='Ana Menüye Dön', size_hint_y=None, height=50, on_press=self.go_back)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    # Arka planı güncelleme fonksiyonu
    def _update_bg(self, instance, value):
        self.canvas.before.clear()
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))

    # İlgili araç ekranına geçiş fonksiyonu
    def go_to_tool(self, tool_name):
        print(f"{tool_name} aracına gidiliyor...")
        self.manager.current = tool_name # ScreenManager adını kullanıyoruz


# SMS Bomber Ekranı
class SMSBomberScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ekranın arka plan rengini ayarla
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))
        self.bind(size=self._update_bg, pos=self._update_bg)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Başlık
        title_label = Label(text='[b]SMS Bomber[/b]', font_size='24sp',
                            halign='center', valign='middle', markup=True,
                            size_hint_y=None, height=60, color=TEXT_COLOR)
        layout.add_widget(title_label)

        # Hedef Numara Girişi
        layout.add_widget(Label(text='Hedef Telefon Numarası:', size_hint_y=None, height=30, color=TEXT_COLOR))
        self.target_number_input = TextInput(hint_text='Örn: +905xx1234567', multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.target_number_input)

        # Mesaj Girişi (Opsiyonel)
        layout.add_widget(Label(text='Mesaj (Opsiyonel):', size_hint_y=None, height=30, color=TEXT_COLOR))
        self.message_input = TextInput(hint_text='Bombardıman mesajı', multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.message_input)

        # Gönderme Sayısı Girişi (Opsiyonel)
        layout.add_widget(Label(text='Gönderme Sayısı (Opsiyonel, Varsayılan: 10):', size_hint_y=None, height=30, color=TEXT_COLOR))
        self.count_input = TextInput(hint_text='Sayı', multiline=False, size_hint_y=None, height=50, input_filter='int') # Sadece sayı girişi
        layout.add_widget(self.count_input)

        # Başlat butonu
        btn_start = Button(text='Bombardımanı Başlat', size_hint_y=None, height=50, on_press=self.start_bombing)
        layout.add_widget(btn_start)

        # Sonuç/Durum Alanı
        self.status_label = Label(text='Durum: Bekleniyor...', size_hint_y=None, height=40, color=TEXT_COLOR)
        layout.add_widget(self.status_label)

        # Geri butonu
        btn_back = Button(text='Geri', size_hint_y=None, height=50, on_press=self.go_back)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    # Arka planı güncelleme fonksiyonu
    def _update_bg(self, instance, value):
        self.canvas.before.clear()
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))

    # Bombardıman başlatma fonksiyonu (Placeholder)
    def start_bombing(self, instance):
        target_number = self.target_number_input.text.strip()
        message = self.message_input.text.strip()
        count = self.count_input.text.strip()

        if not target_number:
            self.status_label.text = "[Hata] Lütfen bir hedef numara girin reis!"
            self.status_label.color = ERROR_COLOR
            return

        # Gönderme sayısı varsayılan veya girilen değer
        try:
            count = int(count) if count else 10
            if count <= 0:
                 count = 10 # En az 1
        except ValueError:
             count = 10 # Geçersiz giriş varsa varsayılan

        self.status_label.text = f"Durum: Bombardıman Başlatılıyor...\nHedef: {target_number}, Sayı: {count}"
        self.status_label.color = TEXT_COLOR

        # BURAYA GERÇEK SMS GÖNDERME MANTIĞI EKLENECEK REİS
        # DİKKAT: Gerçek SMS gönderme servisleri API veya farklı yöntemler gerektirir.
        # Yasalara uygun kullanımdan sen sorumlusun!
        # Bu sadece bir PLACEHOLDER.

        print(f"SMS Bomber çalıştırılıyor (Simulasyon): Hedef={target_number}, Mesaj='{message}', Sayı={count}")

        # Simulasyon: Başarılı veya Başarısız mesajı göster
        Clock.schedule_once(self.simulation_result, 2) # 2 saniye sonra sonucu göster

    # Simulasyon sonucu gösterme (Placeholder)
    def simulation_result(self, dt):
         self.status_label.text = "Durum: Bombardıman tamamlandı (Simulasyon). Kontrol edin reis!"
         self.status_label.color = SUCCESS_COLOR # Yeşil renk

    # Geri dönüş fonksiyonu
    def go_back(self, instance):
        self.manager.current = 'pentest_menu'


# Nmap Ekranı
class NmapScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ekranın arka plan rengini ayarla
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))
        self.bind(size=self._update_bg, pos=self._update_bg)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Başlık
        title_label = Label(text='[b]Nmap - Ağ Tarayıcı[/b]', font_size='24sp',
                            halign='center', valign='middle', markup=True,
                            size_hint_y=None, height=60, color=TEXT_COLOR)
        layout.add_widget(title_label)

        # Hedef Girişi
        layout.add_widget(Label(text='Hedef IP veya Host Adı:', size_hint_y=None, height=30, color=TEXT_COLOR))
        self.target_input = TextInput(hint_text='Örn: 192.168.1.1 veya example.com', multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.target_input)

        # Port Aralığı Girişi (Opsiyonel)
        layout.add_widget(Label(text='Port Aralığı (Opsiyonel, Örn: 1-1024):', size_hint_y=None, height=30, color=TEXT_COLOR))
        self.ports_input = TextInput(hint_text='Varsayılan: En popüler 1000', multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.ports_input)

        # Tarama Tipi Seçimi (Basit Butonlar)
        layout.add_widget(Label(text='Tarama Tipi:', size_hint_y=None, height=30, color=TEXT_COLOR))
        scan_type_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        self.scan_type = '-sV' # Varsayılan Servis Versiyon Taraması
        btn_syn = Button(text='SYN (-sS)', on_press=lambda x: self.set_scan_type('-sS')) # Root gerekir
        btn_version = Button(text='Versiyon (-sV)', on_press=lambda x: self.set_scan_type('-sV'))
        btn_os = Button(text='OS Tespiti (-O)', on_press=lambda x: self.set_scan_type('-O'))
        scan_type_layout.add_widget(btn_syn)
        scan_type_layout.add_widget(btn_version)
        scan_type_layout.add_widget(btn_os)
        layout.add_widget(scan_type_layout)

        # Başlat butonu
        btn_start = Button(text='Taramayı Başlat', size_hint_y=None, height=50, on_press=self.start_scan)
        layout.add_widget(btn_start)

        # Sonuç/Durum Alanı
        self.output_textinput = TextInput(readonly=True, multiline=True, size_hint=(1, 1),
                                          background_color=(0.2, 0.2, 0.2, 1), foreground_color=TEXT_COLOR,
                                          font_name='monospace', cursor_color=(1,1,1,1))
        scroll_view_output = ScrollView(size_hint=(1, 1))
        scroll_view_output.add_widget(self.output_textinput)
        layout.add_widget(scroll_view_output)

        # Geri butonu
        btn_back = Button(text='Geri', size_hint_y=None, height=50, on_press=self.go_back)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    # Arka planı güncelleme fonksiyonu
    def _update_bg(self, instance, value):
        self.canvas.before.clear()
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))

    # Tarama tipini ayarla
    def set_scan_type(self, scan_type):
        self.scan_type = scan_type
        print(f"Nmap tarama tipi ayarlandı: {self.scan_type}")

    # Taramayı başlatma fonksiyonu
    def start_scan(self, instance):
        target = self.target_input.text.strip()
        ports = self.ports_input.text.strip()

        if not target:
            self.output_textinput.text += "\n[Hata] Lütfen bir hedef IP veya host adı girin reis!"
            self.output_textinput.foreground_color = ERROR_COLOR
            return

        # Nmap komutunu oluştur
        command = ['nmap']
        if self.scan_type:
            command.append(self.scan_type)
        if ports:
            command.extend(['-p', ports]) # Port aralığını ekle
        command.append(target)

        # Root komutu için 'tsu -c' ekle (SYN taraması gibi root gerektirenler için)
        # Kullanıcıya root gereksinimini belirtmek önemli
        if self.scan_type == '-sS' or self.scan_type == '-O': # SYN veya OS tespiti genelde root ister
             # command = ['tsu', '-c', ' '.join(command)] # 'tsu -c "nmap -sS hedef"' gibi olur
             # Alternatif ve daha temiz: komutu string yapıp tsu'ya vermek
             command_str = ' '.join(command)
             command = ['tsu', '-c', command_str]
             self.output_textinput.text += f"\n[Bilgi] Bu tarama tipi root yetkisi gerektirir. 'tsu' ile çalıştırılıyor olabilir."
             self.output_textinput.foreground_color = TEXT_COLOR # Tekrar beyaz yap


        self.output_textinput.text += f"\n[+] Nmap Komutu: {' '.join(command)}\n"
        self.output_textinput.foreground_color = TEXT_COLOR # Metin rengini varsayılana döndür

        # Komutu ayrı bir thread'de çalıştır ki UI donmasın
        threading.Thread(target=self._run_command_in_thread, args=(command,)).start()


    # Komutu ayrı thread'de çalıştıran yardımcı fonksiyon
    def _run_command_in_thread(self, command):
        try:
            # Gerçek zamanlı çıktı için Popen kullanıyoruz
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       text=True, encoding='utf-8', errors='ignore')

            # Çıktıyı oku ve Textinput'a yaz (Basit yöntem, büyük çıktıları yönetmek için iyileştirilebilir)
            # Gerçek zamanlı çıktı okuma Kivy event loop'u ile biraz karmaşık, basitçe bekleyelim.
            # Daha iyisi: threading veya Clock.schedule_interval ile çıktı borusunu okumak.
            # Şimdilik komut bitene kadar bekleyelim ve çıktıyı alalım.

            stdout, stderr = process.communicate(timeout=300) # 5 dakika timeout

            # Çıktıyı ana UI thread'inde güncelle
            Clock.schedule_once(lambda dt: self._update_output(stdout, stderr), 0)


        except FileNotFoundError:
            Clock.schedule_once(lambda dt: self._update_output(None, "[Hata] Nmap komutu bulunamadı reis! Termux'a 'pkg install nmap' ile kurdun mu?"), 0)
        except subprocess.TimeoutExpired:
             Clock.schedule_once(lambda dt: self._update_output(None, "[Hata] Nmap taraması zaman aşımına uğradı reis."), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self._update_output(None, f"[Hata] Nmap çalıştırılırken bir hata oluştu reis: {e}"), 0)

    # Çıktıyı UI'da güncelleyen fonksiyon (ana thread'de çalışmalı)
    def _update_output(self, stdout, stderr):
        if stdout:
            self.output_textinput.text += stdout
        if stderr:
            self.output_textinput.text += f"[Hata Çıktısı]\n{stderr}"
            self.output_textinput.foreground_color = ERROR_COLOR # Hata çıktısı kırmızı olsun

        self.output_textinput.text += f"\n[+] Tarama Tamamlandı."
        self.output_textinput.foreground_color = SUCCESS_COLOR # Yeşil renk

        # İmleci en sona kaydır
        self.output_textinput.cursor = (0, len(self.output_textinput._lines) if hasattr(self.output_textinput, '_lines') else 0)


    # Geri dönüş fonksiyonu
    def go_back(self, instance):
        self.manager.current = 'pentest_menu'


# Bloodhound Ekranı (Bilgilendirme)
class BloodhoundScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ekranın arka plan rengini ayarla
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))
        self.bind(size=self._update_bg, pos=self._update_bg)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Başlık
        title_label = Label(text='[b]Bloodhound[/b]', font_size='24sp',
                            halign='center', valign='middle', markup=True,
                            size_hint_y=None, height=60, color=TEXT_COLOR)
        layout.add_widget(title_label)

        # Bilgilendirme yazısı
        info_text = """
        Reis, Bloodhound genellikle Active Directory ortamındaki ilişkileri analiz etmek için kullanılır.
        Veri toplama (Ingestor) ve analiz (Neo4j + GUI) bileşenlerinden oluşur.

        Termux ortamında doğrudan Bloodhound GUI'sini çalıştırmak mümkün değildir.
        Python tabanlı Ingestor'lar teorik olarak çalışabilir ancak:
        - Hedef Active Directory'ye ağ erişimi gerektirir.
        - Geçerli kimlik bilgileri (kullanıcı adı/şifre veya hash) gerektirir.
        - Ek Python kütüphaneleri (örn: impacket) kurulumu gerekebilir.

        Bu bölüm sadece bilgi amaçlıdır. Bloodhound analizi genellikle ayrı bir makine veya ortamda yapılır.
        """
        info_label = Label(text=info_text, size_hint_y=None, height=300, color=TEXT_COLOR,
                           halign='left', valign='top', text_size=(Window.width * 0.9 - 20, None)) # Pencere genişliğine göre ayarla
        layout.add_widget(info_label)

        # Geri butonu
        btn_back = Button(text='Geri', size_hint_y=None, height=50, on_press=self.go_back)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    # Arka planı güncelleme fonksiyonu
    def _update_bg(self, instance, value):
        self.canvas.before.clear()
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))

    # Geri dönüş fonksiyonu
    def go_back(self, instance):
        self.manager.current = 'pentest_menu'


# PowerView Ekranı (Bilgilendirme)
class PowerViewScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ekranın arka plan rengini ayarla
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))
        self.bind(size=self._update_bg, pos=self._update_bg)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Başlık
        title_label = Label(text='[b]PowerView[/b]', font_size='24sp',
                            halign='center', valign='middle', markup=True,
                            size_hint_y=None, height=60, color=TEXT_COLOR)
        layout.add_widget(title_label)

        # Bilgilendirme yazısı
        info_text = """
        Reis, PowerView genellikle Active Directory keşfi için kullanılan PowerShell scriptlerini içerir.
        PowerShell, Windows işletim sistemine özgüdür.

        Termux'ta PowerShell Core kurup çalıştırmak teknik olarak mümkün olsa da,
        PowerView scriptlerinin büyük çoğunluğu Windows API'lerine bağımlıdır ve
        Termux ortamında doğrudan çalışmaları çok zordur veya imkansızdır.

        Active Directory keşfi için Termux'ta Impacket gibi Python kütüphanelerini
        kullanmak daha uygun bir yaklaşımdır.

        Bu bölüm sadece bilgi amaçlıdır. PowerView analizi genellikle Windows tabanlı
        bir makine üzerinden yapılır.
        """
        info_label = Label(text=info_text, size_hint_y=None, height=300, color=TEXT_COLOR,
                           halign='left', valign='top', text_size=(Window.width * 0.9 - 20, None))
        layout.add_widget(info_label)

        # Geri butonu
        btn_back = Button(text='Geri', size_hint_y=None, height=50, on_press=self.go_back)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    # Arka planı güncelleme fonksiyonu
    def _update_bg(self, instance, value):
        self.canvas.before.clear()
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))

    # Geri dönüş fonksiyonu
    def go_back(self, instance):
        self.manager.current = 'pentest_menu'


# Hydra Ekranı
class HydraScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ekranın arka plan rengini ayarla
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))
        self.bind(size=self._update_bg, pos=self._update_bg)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Başlık
        title_label = Label(text='[b]Hydra - Parola Kırıcı[/b]', font_size='24sp',
                            halign='center', valign='middle', markup=True,
                            size_hint_y=None, height=60, color=TEXT_COLOR)
        layout.add_widget(title_label)

        # Hedef Girişi
        layout.add_widget(Label(text='Hedef IP veya Host Adı:', size_hint_y=None, height=30, color=TEXT_COLOR))
        self.target_input = TextInput(hint_text='Örn: 192.168.1.1', multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.target_input)

        # Servis Seçimi (Basit Dropdown veya Butonlar) - Şimdilik TextInput
        layout.add_widget(Label(text='Servis (Örn: ssh, ftp, http-post-form):', size_hint_y=None, height=30, color=TEXT_COLOR))
        self.service_input = TextInput(hint_text='Örn: ssh', multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.service_input)

        # Kullanıcı Adı Listesi (Dosya Yolu)
        layout.add_widget(Label(text='Kullanıcı Adı Listesi Dosya Yolu (-L):', size_hint_y=None, height=30, color=TEXT_COLOR))
        self.user_list_input = TextInput(hint_text='Örn: /sdcard/users.txt', multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.user_list_input)

        # Parola Listesi (Dosya Yolu)
        layout.add_widget(Label(text='Parola Listesi Dosya Yolu (-P):', size_hint_y=None, height=30, color=TEXT_COLOR))
        self.pass_list_input = TextInput(hint_text='Örn: /sdcard/passwords.txt', multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.pass_list_input)

        # Başlat butonu
        btn_start = Button(text='Saldırıyı Başlat', size_hint_y=None, height=50, on_press=self.start_attack)
        layout.add_widget(btn_start)

        # Sonuç/Durum Alanı
        self.output_textinput = TextInput(readonly=True, multiline=True, size_hint=(1, 1),
                                          background_color=(0.2, 0.2, 0.2, 1), foreground_color=TEXT_COLOR,
                                          font_name='monospace', cursor_color=(1,1,1,1))
        scroll_view_output = ScrollView(size_hint=(1, 1))
        scroll_view_output.add_widget(self.output_textinput)
        layout.add_widget(scroll_view_output)


        # Geri butonu
        btn_back = Button(text='Geri', size_hint_y=None, height=50, on_press=self.go_back)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    # Arka planı güncelleme fonksiyonu
    def _update_bg(self, instance, value):
        self.canvas.before.clear()
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))

    # Saldırıyı başlatma fonksiyonu
    def start_attack(self, instance):
        target = self.target_input.text.strip()
        service = self.service_input.text.strip()
        user_list = self.user_list_input.text.strip()
        pass_list = self.pass_list_input.text.strip()

        if not target or not service or not user_list or not pass_list:
            self.output_textinput.text += "\n[Hata] Lütfen tüm alanları doldurun reis (Hedef, Servis, Kullanıcı ve Parola Listesi)."
            self.output_textinput.foreground_color = ERROR_COLOR
            return

        # Hydra komutunu oluştur
        command = ['hydra']
        command.extend(['-L', user_list])
        command.extend(['-P', pass_list])
        command.extend([target, service])

        # Hydra genelde root istemez ama ağ trafiği için gerekebilir, yine de tsu eklemiyoruz şimdilik.
        # Eğer Termux rootluysa, ağ erişimi zaten vardır.

        self.output_textinput.text += f"\n[+] Hydra Komutu: {' '.join(command)}\n"
        self.output_textinput.foreground_color = TEXT_COLOR

        # Komutu ayrı bir thread'de çalıştır ki UI donmasın
        threading.Thread(target=self._run_command_in_thread, args=(command,)).start()

    # Komutu ayrı thread'de çalıştıran yardımcı fonksiyon
    def _run_command_in_thread(self, command):
        try:
            # Gerçek zamanlı çıktı için Popen kullanıyoruz
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       text=True, encoding='utf-8', errors='ignore')

            # Çıktıyı oku ve Textinput'a yaz (Basit yöntem, büyük çıktıları yönetmek için iyileştirilebilir)
            # Gerçek zamanlı çıktı okuma Kivy event loop'u ile biraz karmaşık, basitçe bekleyelim.
            # Daha iyisi: threading veya Clock.schedule_interval ile çıktı borusunu okumak.
            # Şimdilik komut bitene kadar bekleyelim ve çıktıyı alalım.
            stdout, stderr = process.communicate(timeout=900) # 15 dakika timeout

            # Çıktıyı ana UI thread'inde güncelle
            Clock.schedule_once(lambda dt: self._update_output(stdout, stderr), 0)

        except FileNotFoundError:
            Clock.schedule_once(lambda dt: self._update_output(None, "[Hata] Hydra komutu bulunamadı reis! Termux'a 'pkg install hydra' ile kurdun mu?"), 0)
        except subprocess.TimeoutExpired:
             Clock.schedule_once(lambda dt: self._update_output(None, "[Hata] Hydra saldırısı zaman aşımına uğradı reis."), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self._update_output(None, f"[Hata] Hydra çalıştırılırken bir hata oluştu reis: {e}"), 0)

    # Çıktıyı UI'da güncelleyen fonksiyon (ana thread'de çalışmalı)
    def _update_output(self, stdout, stderr):
        if stdout:
            self.output_textinput.text += stdout
        if stderr:
            self.output_textinput.text += f"[Hata Çıktısı]\n{stderr}"
            self.output_textinput.foreground_color = ERROR_COLOR # Hata çıktısı kırmızı olsun

        self.output_textinput.text += f"\n[+] Saldırı Tamamlandı."
        # Başarılı parola bulunursa yeşil renkle belirtebiliriz (çıktıyı parse etmek gerek)
        if stdout and "password:" in stdout:
             self.output_textinput.text += "\n[!!!] Başarılı parola/kullanıcı kombinasyonları bulundu reis! Çıktıyı kontrol et!"
             self.output_textinput.foreground_color = SUCCESS_COLOR # Yeşil
        else:
             self.output_textinput.foreground_color = TEXT_COLOR

        # İmleci en sona kaydır
        self.output_textinput.cursor = (0, len(self.output_textinput._lines) if hasattr(self.output_textinput, '_lines') else 0)


    # Geri dönüş fonksiyonu
    def go_back(self, instance):
        self.manager.current = 'pentest_menu'


# John The Ripper Ekranı
class JohnScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ekranın arka plan rengini ayarla
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))
        self.bind(size=self._update_bg, pos=self._update_bg)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Başlık
        title_label = Label(text='[b]John The Ripper - Hash Kırıcı[/b]', font_size='24sp',
                            halign='center', valign='middle', markup=True,
                            size_hint_y=None, height=60, color=TEXT_COLOR)
        layout.add_widget(title_label)

        # Hash Girişi veya Hash Dosyası Yolu
        layout.add_widget(Label(text='Kırılacak Hash veya Hash Dosyası Yolu:', size_hint_y=None, height=30, color=TEXT_COLOR))
        self.hash_input = TextInput(hint_text='Hash değeri veya /sdcard/hashes.txt', multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.hash_input)

        # Parola Listesi (Wordlist) Dosya Yolu (Opsiyonel, genelde -w)
        layout.add_widget(Label(text='Parola Listesi (Wordlist) Dosya Yolu (-w, Opsiyonel):', size_hint_y=None, height=30, color=TEXT_COLOR))
        self.wordlist_input = TextInput(hint_text='Örn: /sdcard/wordlist.txt', multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.wordlist_input)

        # Başlat butonu
        btn_start = Button(text='Kırma İşlemini Başlat', size_hint_y=None, height=50, on_press=self.start_cracking)
        layout.add_widget(btn_start)

        # Sonuç/Durum Alanı
        self.output_textinput = TextInput(readonly=True, multiline=True, size_hint=(1, 1),
                                          background_color=(0.2, 0.2, 0.2, 1), foreground_color=TEXT_COLOR,
                                          font_name='monospace', cursor_color=(1,1,1,1))
        scroll_view_output = ScrollView(size_hint=(1, 1))
        scroll_view_output.add_widget(self.output_textinput)
        layout.add_widget(scroll_view_output)


        # Geri butonu
        btn_back = Button(text='Geri', size_hint_y=None, height=50, on_press=self.go_back)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    # Arka planı güncelleme fonksiyonu
    def _update_bg(self, instance, value):
        self.canvas.before.clear()
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))

    # Kırma işlemini başlatma fonksiyonu
    def start_cracking(self, instance):
        hash_value_or_file = self.hash_input.text.strip()
        wordlist = self.wordlist_input.text.strip()

        if not hash_value_or_file:
            self.output_textinput.text += "\n[Hata] Lütfen kırılacak hash veya hash dosyası yolu girin reis!"
            self.output_textinput.foreground_color = ERROR_COLOR
            return

        # John komutunu oluştur
        command = ['john']

        # Wordlist eklendiyse
        if wordlist:
             command.extend(['--wordlist', wordlist])

        # Hash değeri mi yoksa dosya mı olduğunu kontrol et
        if os.path.exists(hash_value_or_file):
             command.append(hash_value_or_file) # Dosya yolu
        else:
             # Hash değeri ise -stdin kullanabiliriz veya dosyaya yazıp kullanabiliriz
             # Basitlik için şimdilik sadece dosya yolu kabul edelim veya komuta doğrudan hash verelim
             # Direkt hash vermek için farklı formatlar gerekebilir, dosya daha standart
             # O yüzden uyarı verip dosya yolu isteyelim
             self.output_textinput.text += "\n[Bilgi] Girilen değer bir dosya yolu olarak algılanıyor. Eğer bir hash değeri girmek istediyseniz, lütfen hash'i bir dosyaya kaydedip dosya yolunu girin reis."
             command.append(hash_value_or_file) # Yine de komuta ekleyelim, belki John kendisi algılar


        self.output_textinput.text += f"\n[+] John Komutu: {' '.join(command)}\n"
        self.output_textinput.foreground_color = TEXT_COLOR


        # Komutu ayrı bir thread'de çalıştır ki UI donmasın
        threading.Thread(target=self._run_command_in_thread, args=(command,)).start()

    # Komutu ayrı thread'de çalıştıran yardımcı fonksiyon
    def _run_command_in_thread(self, command):
        try:
            # Gerçek zamanlı çıktı için Popen kullanıyoruz
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       text=True, encoding='utf-8', errors='ignore')

            self.output_textinput.text += "\n[+] Kırma İşlemi Başlatıldı...\n"
            # Komut bitene kadar bekleyip çıktıyı alalım
            stdout, stderr = process.communicate(timeout=1800) # 30 dakika timeout (kırma uzun sürebilir)

            # Çıktıyı ana UI thread'inde güncelle
            Clock.schedule_once(lambda dt: self._update_output(stdout, stderr), 0)


        except FileNotFoundError:
            Clock.schedule_once(lambda dt: self._update_output(None, "[Hata] John The Ripper komutu bulunamadı reis! Termux'a 'pkg install john the ripper' ile kurdun mu?"), 0)
        except subprocess.TimeoutExpired:
             Clock.schedule_once(lambda dt: self._update_output(None, "[Hata] Kırma işlemi zaman aşımına uğradı reis."), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self._update_output(None, f"[Hata] John çalıştırılırken bir hata oluştu reis: {e}"), 0)

    # Çıktıyı UI'da güncelleyen fonksiyon (ana thread'de çalışmalı)
    def _update_output(self, stdout, stderr):
        if stdout:
            self.output_textinput.text += stdout
        if stderr:
            self.output_textinput.text += f"[Hata Çıktısı]\n{stderr}"
            self.output_textinput.foreground_color = ERROR_COLOR # Hata çıktısı kırmızı olsun

        self.output_textinput.text += f"\n[+] Kırma İşlemi Tamamlandı."
        # Kırılan parolalar çıktıda "Cracked passwords for ..." gibi görünür
        if stdout and "Cracked passwords for" in stdout: # Basit bir kontrol
             self.output_textinput.text += "\n[!!!] Başarılı hash kırılmaları bulundu reis! Çıktıyı kontrol et!"
             self.output_textinput.foreground_color = SUCCESS_COLOR # Yeşil
        else:
             self.output_textinput.foreground_color = TEXT_COLOR

        # İmleci en sona kaydır
        self.output_textinput.cursor = (0, len(self.output_textinput._lines) if hasattr(self.output_textinput, '_lines') else 0)


    # Geri dönüş fonksiyonu
    def go_back(self, instance):
        self.manager.current = 'pentest_menu'


# sqlmap Ekranı
class SqlmapScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ekranın arka plan rengini ayarla
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))
        self.bind(size=self._update_bg, pos=self._update_bg)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Başlık
        title_label = Label(text='[b]sqlmap - SQL Enjeksiyon Tarayıcı[/b]', font_size='24sp',
                            halign='center', valign='middle', markup=True,
                            size_hint_y=None, height=60, color=TEXT_COLOR)
        layout.add_widget(title_label)

        # Hedef URL Girişi
        layout.add_widget(Label(text='Hedef URL:', size_hint_y=None, height=30, color=TEXT_COLOR))
        self.target_url_input = TextInput(hint_text='Örn: http://example.com/vuln.php?id=1', multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.target_url_input)

        # Seçenekler (Basit TextInput)
        layout.add_widget(Label(text='Ek Seçenekler (Opsiyonel, Örn: --dbs --batch):', size_hint_y=None, height=30, color=TEXT_COLOR))
        self.options_input = TextInput(hint_text='Boş bırakabilirsiniz', multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.options_input)


        # Başlat butonu
        btn_start = Button(text='Taramayı Başlat', size_hint_y=None, height=50, on_press=self.start_scan)
        layout.add_widget(btn_start)

        # Sonuç/Durum Alanı
        self.output_textinput = TextInput(readonly=True, multiline=True, size_hint=(1, 1),
                                          background_color=(0.2, 0.2, 0.2, 1), foreground_color=TEXT_COLOR,
                                          font_name='monospace', cursor_color=(1,1,1,1))
        scroll_view_output = ScrollView(size_hint=(1, 1))
        scroll_view_output.add_widget(self.output_textinput)
        layout.add_widget(scroll_view_output)


        # Geri butonu
        btn_back = Button(text='Geri', size_hint_y=None, height=50, on_press=self.go_back)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    # Arka planı güncelleme fonksiyonu
    def _update_bg(self, instance, value):
        self.canvas.before.clear()
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))

    # Taramayı başlatma fonksiyonu
    def start_scan(self, instance):
        target_url = self.target_url_input.text.strip()
        options = self.options_input.text.strip()

        if not target_url:
            self.output_textinput.text += "\n[Hata] Lütfen bir hedef URL girin reis!"
            self.output_textinput.foreground_color = ERROR_COLOR
            return

        # sqlmap komutunu oluştur
        command = ['sqlmap', '-u', target_url]

        # Ek seçenekler varsa ekle
        if options:
            command.extend(options.split()) # Boşluklara göre ayırıp listeye ekle

        # sqlmap genelde root istemez.
        self.output_textinput.text += f"\n[+] sqlmap Komutu: {' '.join(command)}\n"
        self.output_textinput.foreground_color = TEXT_COLOR


        # Komutu ayrı bir thread'de çalıştır ki UI donmasın
        threading.Thread(target=self._run_command_in_thread, args=(command,)).start()

    # Komutu ayrı thread'de çalıştıran yardımcı fonksiyon
    def _run_command_in_thread(self, command):
        try:
            # Gerçek zamanlı çıktı için Popen kullanıyoruz
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       text=True, encoding='utf-8', errors='ignore')

            self.output_textinput.text += "\n[+] Tarama Başlatıldı...\n"
            # Komut bitene kadar bekleyip çıktıyı alalım
            stdout, stderr = process.communicate(timeout=600) # 10 dakika timeout

            # Çıktıyı ana UI thread'inde güncelle
            Clock.schedule_once(lambda dt: self._update_output(stdout, stderr), 0)


        except FileNotFoundError:
            Clock.schedule_once(lambda dt: self._update_output(None, "[Hata] sqlmap komutu bulunamadı reis! Termux'a 'pkg install sqlmap' ile kurdun mu?"), 0)
        except subprocess.TimeoutExpired:
             Clock.schedule_once(lambda dt: self._update_output(None, "[Hata] sqlmap taraması zaman aşımına uğradı reis."), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self._update_output(None, f"[Hata] sqlmap çalıştırılırken bir hata oluştu reis: {e}"), 0)

    # Çıktıyı UI'da güncelleyen fonksiyon (ana thread'de çalışmalı)
    def _update_output(self, stdout, stderr):
        if stdout:
            self.output_textinput.text += stdout
        if stderr:
            self.output_textinput.text += f"[Hata Çıktısı]\n{stderr}"
            self.output_textinput.foreground_color = ERROR_COLOR # Hata çıktısı kırmızı olsun

        self.output_textinput.text += f"\n[+] Tarama Tamamlandı."
        # Zafiyet bulunursa çıktıda belirtir
        if stdout and "Parameter: " in stdout and "Type: " in stdout: # Basit bir kontrol
             self.output_textinput.text += "\n[!!!] SQL Enjeksiyon zafiyeti bulunmuş olabilir reis! Çıktıyı kontrol et!"
             self.output_textinput.foreground_color = SUCCESS_COLOR # Yeşil
        else:
             self.output_textinput.foreground_color = TEXT_COLOR

        # İmleci en sona kaydır
        self.output_textinput.cursor = (0, len(self.output_textinput._lines) if hasattr(self.output_textinput, '_lines') else 0)


    # Geri dönüş fonksiyonu
    def go_back(self, instance):
        self.manager.current = 'pentest_menu'


# Burp Suite Ekranı (Bilgilendirme)
class BurpSuiteScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ekranın arka plan rengini ayarla
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))
        self.bind(size=self._update_bg, pos=self._update_bg)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Başlık
        title_label = Label(text='[b]Burp Suite[/b]', font_size='24sp',
                            halign='center', valign='middle', markup=True,
                            size_hint_y=None, height=60, color=TEXT_COLOR)
        layout.add_widget(title_label)

        # Bilgilendirme yazısı
        info_text = """
        Reis, Burp Suite web uygulaması güvenliği testleri için popüler bir araçtır.
        Bir Java GUI uygulamasıdır ve bu Python tabanlı Kivy uygulamasının içinde
        doğrudan çalıştırılamaz.

        Burp Suite'i kullanmak için:
        1. Burp Suite'i bilgisayarınızda veya ayrı bir ortamda çalıştırın.
        2. Test edeceğiniz cihazın (bu telefon veya başka bir cihaz) internet trafiğini
           Burp Suite'in çalıştığı IP ve porta proxy olarak ayarlayın.
        3. Gerekirse Burp'ün CA sertifikasını cihaza yükleyin.

        Bu ekran sadece bilgi amaçlıdır. Burp Suite harici bir araçtır.
        """
        info_label = Label(text=info_text, size_hint_y=None, height=300, color=TEXT_COLOR,
                           halign='left', valign='top', text_size=(Window.width * 0.9 - 20, None))
        layout.add_widget(info_label)

        # Geri butonu
        btn_back = Button(text='Geri', size_hint_y=None, height=50, on_press=self.go_back)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    # Arka planı güncelleme fonksiyonu
    def _update_bg(self, instance, value):
        self.canvas.before.clear()
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))

    # Geri dönüş fonksiyonu
    def go_back(self, instance):
        self.manager.current = 'pentest_menu'


# ffuf Ekranı
class FFUFScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ekranın arka plan rengini ayarla
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))
        self.bind(size=self._update_bg, pos=self._update_bg)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Başlık
        title_label = Label(text='[b]ffuf - Web Fuzzer[/b]', font_size='24sp',
                            halign='center', valign='middle', markup=True,
                            size_hint_y=None, height=60, color=TEXT_COLOR)
        layout.add_widget(title_label)

        # Hedef URL Girişi
        layout.add_widget(Label(text='Hedef URL (FUZZ Kelimesini Kullanın):', size_hint_y=None, height=30, color=TEXT_COLOR))
        self.target_url_input = TextInput(hint_text='Örn: http://example.com/FUZZ', multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.target_url_input)

        # Wordlist Dosyası Yolu
        layout.add_widget(Label(text='Wordlist Dosyası Yolu (-w):', size_hint_y=None, height=30, color=TEXT_COLOR))
        self.wordlist_input = TextInput(hint_text='Örn: /sdcard/wordlists/common.txt', multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.wordlist_input)

        # Başlat butonu
        btn_start = Button(text='Fuzzingi Başlat', size_hint_y=None, height=50, on_press=self.start_fuzzing)
        layout.add_widget(btn_start)

        # Sonuç/Durum Alanı
        self.output_textinput = TextInput(readonly=True, multiline=True, size_hint=(1, 1),
                                          background_color=(0.2, 0.2, 0.2, 1), foreground_color=TEXT_COLOR,
                                          font_name='monospace', cursor_color=(1,1,1,1))
        scroll_view_output = ScrollView(size_hint=(1, 1))
        scroll_view_output.add_widget(self.output_textinput)
        layout.add_widget(scroll_view_output)


        # Geri butonu
        btn_back = Button(text='Geri', size_hint_y=None, height=50, on_press=self.go_back)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    # Arka planı güncelleme fonksiyonu
    def _update_bg(self, instance, value):
        self.canvas.before.clear()
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))

    # Fuzzingi başlatma fonksiyonu
    def start_fuzzing(self, instance):
        target_url = self.target_url_input.text.strip()
        wordlist = self.wordlist_input.text.strip()

        if not target_url or not wordlist:
            self.output_textinput.text += "\n[Hata] Lütfen hedef URL ve wordlist yolu girin reis!"
            self.output_textinput.foreground_color = ERROR_COLOR
            return

        if "FUZZ" not in target_url:
             self.output_textinput.text += "\n[Hata] Hedef URL içinde 'FUZZ' kelimesini kullanmalısın reis!"
             self.output_textinput.foreground_color = ERROR_COLOR
             return

        if not os.path.exists(wordlist):
             self.output_textinput.text += "\n[Hata] Girilen wordlist dosyası bulunamadı reis!"
             self.output_textinput.foreground_color = ERROR_COLOR
             return


        # ffuf komutunu oluştur
        command = ['ffuf', '-w', wordlist, '-u', target_url]

        # ffuf genelde root istemez.
        self.output_textinput.text += f"\n[+] ffuf Komutu: {' '.join(command)}\n"
        self.output_textinput.foreground_color = TEXT_COLOR


        # Komutu ayrı bir thread'de çalıştır ki UI donmasın
        threading.Thread(target=self._run_command_in_thread, args=(command,)).start()

    # Komutu ayrı thread'de çalıştıran yardımcı fonksiyon
    def _run_command_in_thread(self, command):
        try:
            # Gerçek zamanlı çıktı için Popen kullanıyoruz
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       text=True, encoding='utf-8', errors='ignore')

            self.output_textinput.text += "\n[+] Fuzzing Başlatıldı...\n"
            # Komut bitene kadar bekleyip çıktıyı alalım
            stdout, stderr = process.communicate(timeout=600) # 10 dakika timeout

            # Çıktıyı ana UI thread'inde güncelle
            Clock.schedule_once(lambda dt: self._update_output(stdout, stderr), 0)


        except FileNotFoundError:
            Clock.schedule_once(lambda dt: self._update_output(None, "[Hata] ffuf komutu bulunamadı reis! Termux'a 'pkg install ffuf' ile kurdun mu?"), 0)
        except subprocess.TimeoutExpired:
             Clock.schedule_once(lambda dt: self._update_output(None, "[Hata] Fuzzing işlemi zaman aşımına uğradı reis."), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self._update_output(None, f"[Hata] ffuf çalıştırılırken bir hata oluştu reis: {e}"), 0)

    # Çıktıyı UI'da güncelleyen fonksiyon (ana thread'de çalışmalı)
    def _update_output(self, stdout, stderr):
        if stdout:
            self.output_textinput.text += stdout
        if stderr:
            self.output_textinput.text += f"[Hata Çıktısı]\n{stderr}"
            self.output_textinput.foreground_color = ERROR_COLOR # Hata çıktısı kırmızı olsun

        self.output_textinput.text += f"\n[+] Fuzzing Tamamlandı."
        # Başarılı sonuçları çıktıda görürsün
        self.output_textinput.foreground_color = TEXT_COLOR # Duruma göre renklendirme eklenebilir

        # İmleci en sona kaydır
        self.output_textinput.cursor = (0, len(self.output_textinput._lines) if hasattr(self.output_textinput, '_lines') else 0)


    # Geri dönüş fonksiyonu
    def go_back(self, instance):
        self.manager.current = 'pentest_menu'


# Aircrack-ng Ekranı (Bilgilendirme)
class AircrackNGScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ekranın arka plan rengini ayarla
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))
        self.bind(size=self._update_bg, pos=self._update_bg)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Başlık
        title_label = Label(text='[b]Aircrack-ng[/b]', font_size='24sp',
                            halign='center', valign='middle', markup=True,
                            size_hint_y=None, height=60, color=TEXT_COLOR)
        layout.add_widget(title_label)

        # Bilgilendirme yazısı
        info_text = """
        Reis, Aircrack-ng Wi-Fi ağlarının güvenliğini test etmek için kullanılır.
        Termux'ta 'pkg install aircrack-ng' ile kurulabilir.

        Ancak Aircrack-ng'nin doğru çalışması için:
        1. Cihazın (telefonun) Wi-Fi çipsetinin monitor modunu desteklemesi gerekir. (Çoğu telefon desteklemez)
        2. Alternatif olarak, monitor modu destekleyen harici bir USB Wi-Fi adaptörü kullanmanız gerekir.
        3. **Kesinlikle root yetkisi gereklidir.**

        Bu Kivy uygulaması içinden Aircrack-ng komutlarını çalıştırmak teknik olarak
        mümkün olsa da, yukarıdaki donanım ve yetki gereksinimleri nedeniyle bu bölüm
        sadece bilgi amaçlıdır. Gerçek kullanım için Termux'un komut satırından veya
        harici bir Linux dağıtımından kullanmanız daha uygundur.
        """
        info_label = Label(text=info_text, size_hint_y=None, height=300, color=TEXT_COLOR,
                           halign='left', valign='top', text_size=(Window.width * 0.9 - 20, None))
        layout.add_widget(info_label)

        # Geri butonu
        btn_back = Button(text='Geri', size_hint_y=None, height=50, on_press=self.go_back)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    # Arka planı güncelleme fonksiyonu
    def _update_bg(self, instance, value):
        self.canvas.before.clear()
        self.canvas.before.add(kivy.graphics.Color(*BG_COLOR))
        self.canvas.before.add(kivy.graphics.Rectangle(size=self.size, pos=self.pos))

    # Geri dönüş fonksiyonu
    def go_back(self, instance):
        self.manager.current = 'pentest_menu'


# Ana uygulama sınıfı
class TakoOSApp(App):
    def build(self):
        self.title = 'TakoOS PyCore™' # Uygulama başlığı
        sm = TakoOSScreenManager()
        # TÜM EKRANLARI BURAYA ADD_WIDGET İLE EKLE REİS
        sm.add_widget(BootSplash(name='boot'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(AppLauncherScreen(name='app_launcher'))
        sm.add_widget(FileManagerScreen(name='file_manager'))
        sm.add_widget(TerminalScreen(name='terminal'))
        sm.add_widget(PowerMenuScreen(name='power_menu'))
        sm.add_widget(PentestMenuScreen(name='pentest_menu'))
        # Pentest araç ekranlarını da ekle
        sm.add_widget(SMSBomberScreen(name='sms_bomber'))
        sm.add_widget(NmapScreen(name='nmap_tool'))
        sm.add_widget(BloodhoundScreen(name='bloodhound_tool'))
        sm.add_widget(PowerViewScreen(name='powerview_tool'))
        sm.add_widget(HydraScreen(name='hydra_tool'))
        sm.add_widget(JohnScreen(name='john_tool'))
        sm.add_widget(SqlmapScreen(name='sqlmap_tool'))
        sm.add_widget(BurpSuiteScreen(name='burp_tool'))
        sm.add_widget(FFUFScreen(name='ffuf_tool'))
        sm.add_widget(AircrackNGScreen(name='aircrack_tool'))


        # Uygulama başladığında ilk gösterilecek ekran
        sm.current = 'boot'
        return sm

    # Kapatma onayı için popup
    def show_exit_popup(self):
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        box.add_widget(Label(text='TakoOS\'tan çıkmak istediğinden emin misin reis?', size_hint_y=None, height=40, color=TEXT_COLOR))
        button_box = BoxLayout(spacing=10)
        yes_button = Button(text='Evet', on_press=self.stop, size_hint_y=None, height=40) # Uygulamayı durdur
        no_button = Button(text='Hayır', on_press=lambda x: popup.dismiss(), size_hint_y=None, height=40) # Popup'ı kapat
        button_box.add_widget(yes_button)
        button_box.add_widget(no_button)
        box.add_widget(button_box)

        popup = Popup(title='Çıkış Onayı', content=box, size_hint=(0.8, 0.4))
        popup.open()

    # Android geri tuşunu yönetmek için (Termux'ta çalışmayabilir ama denemek lazım)
    # Geri tuşa basıldığında ana menüye dönmek için bu metodu kullanabilirsin
    # def on_key_down(self, window, key, scancode, codepoint, modifier):
    #     # Android geri tuşu genellikle 278 veya 1000 civarı bir keycode'a sahiptir
    #     # platform == 'android' kontrolü eklemek iyi olabilir
    #     if key == 278 or key == 1000: # Örnek keycode, cihazına göre değişebilir
    #         current_screen = self.root.current
    #         if current_screen != 'main' and current_screen != 'boot':
    #             # Boot ve Main ekranında değilsek geri dön
    #             self.root.current = 'main' # Veya bir önceki ekrana dönme mantığı kur
    #             return True # Olayı tükettik
    #     return False # Olayı diğer widget'lara ilet

    # Window.bind(on_key_down=self.on_key_down) # build metodunda bu satırı ekle


    def on_pause(self):
        # Uygulama arka plana alındığında True döndürürsek çalışmaya devam eder
        # False döndürürsek duraklatılır
        return True

    def on_stop(self):
        # Uygulama kapanırken yapılacaklar (varsa)
        pass

# Eğer script doğrudan çalıştırılıyorsa uygulamayı başlat
if __name__ == '__main__':
    # Kivy'nin log seviyesini ayarlayabilirsin (isteğe bağlı)
    # import logging
    # from kivy.logger import Logger
    # Logger.setLevel(logging.DEBUG)

    TakoOSApp().run()
