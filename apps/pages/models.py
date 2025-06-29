from django.db import models
from django.conf import settings


# Create your models here.

class Product(models.Model):
    id    = models.AutoField(primary_key=True)
    name  = models.CharField(max_length = 100) 
    info  = models.CharField(max_length = 100, default = '')
    price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

class ResiScan(models.Model):
    tanggal = models.DateTimeField(auto_now_add=True)  # Otomatis isi waktu saat dibuat
    gambar = models.ImageField(upload_to='resi/')      # Lokasi file disimpan di /media/resi/
    nomor_resi = models.CharField(max_length=100)
    lokasi_resi = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nomor_resi} - {self.lokasi_resi}"

class Jawa(models.Model):
    tanggal = models.DateTimeField(auto_now_add=True)  # Otomatis isi waktu saat dibuat
    gambar = models.ImageField(upload_to='resi/REG_JAWA/')      # Lokasi file disimpan di /media/resi/
    nomor_resi = models.CharField(max_length=100)
    lokasi_resi = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nomor_resi} - {self.lokasi_resi}"

class LuarJawa(models.Model):
    tanggal = models.DateTimeField(auto_now_add=True)  # Otomatis isi waktu saat dibuat
    gambar = models.ImageField(upload_to='resi/REG_LUARJAWA/')      # Lokasi file disimpan di /media/resi/
    nomor_resi = models.CharField(max_length=100)
    lokasi_resi = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nomor_resi} - {self.lokasi_resi}"