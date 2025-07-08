import cv2
from django.shortcuts import render, redirect
from .models import ResiScan
from PIL import Image
import numpy as np
import os
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
import easyocr
from .utils import klasifikasi_wilayah, ekstrak_nomor_resi
from datetime import datetime
from django.utils.timezone import now
import tensorflow as tf
from .models import Jawa, LuarJawa


model_cnn = tf.keras.models.load_model(os.path.join(settings.MEDIA_ROOT, 'model_resi_cnn.h5'))
labels = ['REG_JAWA', 'REG_LUARJAWA']

@never_cache
@login_required(login_url='login')
def index(request):
    data = Jawa.objects.all()
    luarJawa = LuarJawa.objects.all()
    
    jumlah_reg_jawa = Jawa.objects.filter(lokasi_resi='REG_JAWA').count()
    jumlah_reg_luar_jawa = LuarJawa.objects.filter(lokasi_resi='REG_LUARJAWA').count()

    total_all = Jawa.objects.count() + LuarJawa.objects.count()

    persen_reg_jawa = round((jumlah_reg_jawa / total_all) * 100, 2) if total_all > 0 else 0
    persen_reg_luar_jawa = round((jumlah_reg_luar_jawa / total_all) * 100, 2) if total_all > 0 else 0

    return render(request, 'pages/index.html', {
        'data': data,
        'jumlah_reg_jawa': jumlah_reg_jawa,
        'persen_reg_jawa': persen_reg_jawa,
        'jumlah_reg_luar_jawa' : jumlah_reg_luar_jawa,
        'persen_reg_luar_jawa': persen_reg_luar_jawa,
    })

@never_cache
@login_required(login_url='login')
def table_jawa(request):
    data = Jawa.objects.all()
    return render(request, 'pages/tables/jawa.html', {'data': data})

@never_cache
@login_required(login_url='login')
def table_luar_jawa(request):
    data = LuarJawa.objects.all()
    return render(request, 'pages/tables/luar-jawa.html', {'data': data})

@never_cache
@login_required(login_url='login')
def upload_resi(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']

        # Prediksi CNN dulu
        cnn_pred_label, akurasi = klasifikasi_cnn(image) # perhatikan: jika klasifikasi_cnn butuh path, simpan sementara dulu

        # Tentukan folder dan model sesuai label
        if cnn_pred_label == 'REG_JAWA':
            folder = 'REG_JAWA'
            ModelResi = Jawa
        else:
            folder = 'REG_LUARJAWA'
            ModelResi = LuarJawa

        # Buat path penyimpanan
        path = os.path.join(settings.MEDIA_ROOT, 'resi', folder, image.name)
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # Simpan gambar
        with open(path, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)

        # OCR
        reader = easyocr.Reader(['en', 'id'])
        ocr_result = reader.readtext(path)
        hasil_text = ' '.join([res[1] for res in ocr_result])

        # Ekstrak nomor resi
        nomor_resi = ekstrak_nomor_resi(hasil_text)

        # Simpan record ke DB tabel sesuai label
        ModelResi.objects.create(
            gambar=f'resi/{folder}/{image.name}',
            nomor_resi=nomor_resi,
            lokasi_resi=cnn_pred_label
        )

        return render(request, 'pages/forms/general.html', {
            'tanggal': now(),
            'image_url': f'media/resi/{folder}/{image.name}',
            'text': hasil_text,
            'wilayah': cnn_pred_label,
            'nomor_resi': nomor_resi,
            'akurasi': akurasi
        })

    return render(request, 'pages/forms/general.html')


def klasifikasi_cnn(image_path):
    img = Image.open(image_path).convert('RGB')
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    pred = model_cnn.predict(img_array)
    prob = pred[0][0]  # misal: 0.92 berarti 92% yakin REG_LUARJAWA

    if prob >= 0.5:
        label = 'REG_LUARJAWA'
        akurasi = prob * 100  # misal: 0.92 => 92%
    else:
        label = 'REG_JAWA'
        akurasi = (1 - prob) * 100  # misal: 0.08 => 92% untuk REG_JAWA

    return label, akurasi

