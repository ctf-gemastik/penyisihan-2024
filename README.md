# Penyisihan CTF GEMASTIK 2023

---

## Struktur Template
**Untuk pembuat soal**

Disediakan *template* pada folder `template/` agar memudahkan pembuatan soal. Silakan *copy* ke dalam folder kategori masing-masing dan diberi nama folder `judul-soal`. Strukturnya adalah sebagai berikut:
```
judul-soal/
 ├─ public/
 ├─ src/
 ├─ writeup/
 │   └─ README.md
 ├─ Dockerfile
 ├─ docker-compose.yml
 └─ README.md
```

Keterangan:
- `public/` 		: Seluruh file di folder ini akan di-zip dan menjadi attachment untuk peserta
- `src/`    		: Berisi file-file yang menjadi soal
- `writeup/`		: Berisi file-file yang menunjukkan solusi/PoC dari soal
- `Dockerfile` dan docker-compose.yml hanya untuk soal yang butuh di-*deploy*
- Update `README.md`
