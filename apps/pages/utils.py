

import spacy
import easyocr
import re


nlp = spacy.load("en_core_web_sm")

DAFTAR_KOTA = [
    "JAKARTA", "BANDUNG", "SURABAYA", "SEMARANG", "YOGYAKARTA",
    "MEDAN", "PALEMBANG", "MAKASSAR", "BALIKPAPAN", "PONTIANAK",
    "BANJARMASIN", "SAMARINDA", "MANADO", "AMBON", "JAYAPURA",
    "SORONG", "BATAM", "PEKANBARU", "PADANG", "DENPASAR",
    "MALANG", "CIANJUR", "BOGOR", "TANGERANG", "DEPOK", "JAWA TIMUR", "JAWA TENGAH", "JAWA BARAT",
]

# Klasifikasi wilayah berdasarkan nama kota
def klasifikasi_wilayah(text):
    text_upper = text.upper()

    kota_ditemukan = []
    for kota in DAFTAR_KOTA:
        if kota in text_upper:
            kota_ditemukan.append((text_upper.index(kota), kota))

    if kota_ditemukan:
        kota_ditemukan.sort()
        kota_terakhir = kota_ditemukan[-1][1]

        # Contoh klasifikasi wilayah berdasarkan kota
        if kota_terakhir in ["JAKARTA", "JAKARTA PUSAT", "JAKARTA UTARA", "JAKARTA SELATAN",
        "JAKARTA TIMUR", "JAKARTA BARAT", "SERANG", "CILEGON", "TANGERANG", "TANGERANG SELATAN",
        "BANDUNG", "BEKASI", "BOGOR", "DEPOK", "CIMAHI", "SUKABUMI", "CIREBON", "TASIKMALAYA",
        "BANJAR", "SEMARANG", "SURAKARTA", "SOLO", "SALATIGA", "MAGELANG", "PEKALONGAN", "PATI", "KUDUS",
        "DEMAK", "JEPARA", "BLORA", "REMBANG", "BOYOLALI", "KLATEN", "SUKOHARJO", "WONOGIRI","YOGYAKARTA", "PURWOREJO", "KEBUMEN", "GUNUNGKIDUL", "BANTUL", "KULON PROGO",
        "SURABAYA", "MALANG", "PASURUAN", "SIDOARJO", "GRESIK", "LAMONGAN", "MOJOKERTO", "BONDOWOSO", "BATU",
        "MADURA", "BANYUWANGI", "JEMBER", "LUMAJANG", "PROBOLINGGO", "TULUNGAGUNG", "BLITAR", "NGANJUK", "TRENGGALEK",
        "KEDIRI", "MAGETAN", "NGANJUK", "PACITAN", "BOJONEGORO", "LAMONGAN", "GRESIK", "SIDOARJO", "MOJOKERTO",
        "BANYUMAS", "PURWOKERTO", "CILACAP", "KARANGANYAR", "PEKALONGAN", "BATANG", "TEGAL", "BREBES", "WONOSOBO",
        "PURWOREJO", "TEMANGGUNG"]:
            return "REG_JAWA"
        elif kota_terakhir in ["MEDAN", "PALEMBANG", "PEKANBARU", "PADANG", "BANDAR LAMPUNG",
        "BENGKULU", "JAMBI", "PANGKAL PINANG", "TANJUNG PINANG", "BATAM",
        "BANGKA", "BELITUNG", "LAMPUNG", "SUMATERA BARAT", "SUMATERA SELATAN",
        "SUMATERA UTARA", "RIAU", "KEPULAUAN RIAU", "KEPULAUAN BANGKA BELITUNG",
        "JAMBI", "BENGKULU", "LAMPUNG", "BANDAR LAMPUNG", "PALEMBANG", "MEDAN", "PADANG",
        "BANDA ACEH", "LANGSA", "LHOKSEUMAWE", "SABANG", "BIREUEN", "ACEH TENGAH", "ACEH BARAT", "ACEH SINGKIL",
        "ACEH TAMIANG", "ACEH TIMUR", "ACEH BESAR", "ACEH SELATAN", "ACEH UTARA", "ACEH TENGGARA", "ACEH BARAT DAYA",
        "ACEH SINGKIL", "ACEH TENGGARA", "ACEH BARAT", "ACEH SELATAN", "ACEH UTARA", "ACEH TAMIANG", "ACEH TIMUR",
        "ACEH BESAR", "ACEH SINGKIL", "ACEH TENGGARA", "ACEH BARAT DAYA", "ACEH SELATAN", "ACEH UTARA",
        "ACEH TAMIANG", "ACEH TIMUR", "ACEH BESAR", "KALIMANTAN", "BALIKPAPAN", "SAMARINDA", "BONTANG",
        "PONTIANAK", "SINGKAWANG", "BANJARMASIN", "PALANGKA RAYA", "KOTAWARINGIN BARAT", "KALIMANTAN BARAT",
        "KALIMANTAN TENGAH", "KALIMANTAN SELATAN", "KALIMANTAN TIMUR", "KALIMANTAN UTARA",
        "KUTAI KARTANEGARA", "KUTAI TIMUR", "PASER", "BERAU", "PANGKALAN BUN", "BARITO KUALA",
        "BARITO TIMUR", "BARITO SELATAN", "BARITO UTARA", "BARITO BARAT", "KATINGAN",
        "SERUYAN", "MURUNG RAYA", "SAMPIT"]:
            return "REG_LUARJAWA"
        else:
            return "REG_LAINNYA"
    
    return "Tidak Dikenali"



def ekstrak_nomor_resi(text):
    text = text.upper()

    # Coba cari baris yang mengandung "NO"
    lines = text.splitlines()
    for line in lines:
        if "NO" in line:
            # Ambil kandidat yang mengandung SPX
            match = re.search(r'(SPX[A-Z0-9]{10,})', line)
            if match:
                return match.group(1)
    
    # Fallback: scan seluruh teks
    match = re.search(r'SPX[A-Z0-9]{10,}', text)
    if match:
        return match.group(0)

    return "Tidak ditemukan"

