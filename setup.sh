#!/bin/bash

echo "TakoOS PyCore™ Kurulum Scripti Başlatılıyor..."
echo "Gerekli paketler (python, kivy) kuruluyor..."

# Termux repolarını güncelleyelim reis
pkg update -y
pkg upgrade -y

# Python ve Kivy'yi kuralım
pkg install python -y
pkg install python-pip -y
# Kivy kurulumu, Termux'ta biraz farklı olabilir, genelde pip ile kurulur
pip install kivy

echo "Kurulum tamamlandı gibi reis. Eksik bir şey olursa main.py çalışırken belli olur."
echo "Şimdi 'python main.py' komutu ile TakoOS'u başlatabilirsin!"

# ROOT erişimi için, eğer 'tsu' veya 'sudo' kurulu değilse uyarı verelim
if ! command -v tsu &> /dev/null && ! command -v sudo &> /dev/null; then
    echo ""
    echo "UYARI: Siber Güvenlik Araçları modülü ve bazı sistem fonksiyonları root erişimi gerektirir."
    echo "Termux'ta root erişimi için 'pkg install tsu' komutunu çalıştırıp Termux'a root yetkisi vermeniz gerekebilir."
fi

echo "İyi kullanımlar reis! 😈"