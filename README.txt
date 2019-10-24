Plagiarism Checker
https://ouwkyuha.blogspot.com/2019/01/cek-plagiarisme-dengan-n-gram.html

Dilahirkan dengan maksud awal mendapat nilai tambahan.
-----------------------------------------------------------------------------

- Dibuat dengan Python 3.7.

- Kerja utama program ini adalah menghitung jumlah kecocokan n-Gram dari kedua teks per jumlah n-Gram teks yang dicurigai.


- Ada dua cara untuk mengimport teks yang ingin dibandingkan :
	1. Dengan mengklik tombol Suspect (untuk mengimport teks yang dicurigai) dan tombol Source (untuk mengimport teks sumber). Hanya file *txt.

	2. Dengan mencopy-paste teks kedalam box yang disediakan.

- PlagiarismChecker.exe hanya berjalan di OS Windows x64.

- Multi Sumber Teks diperbolehkan untuk kemungkinan Plagiator menyontek dari banyak sumber.

- Program ini memiliki 6 mode: Auto (default), 1-Gram, 2-Gram, 3-Gram, 4-Gram, juga 5-Gram. Auto yaitu  menjalankan perbandingan di mode 1-Gram hingga 5-Gram, lalu Skor akan di rata-rata. Sedangkan 1-Gram hingga 5-Gram hanya melakukan perbandingan dengan satu jenis n-Gram saja.

- Mohon download juga "synbank.txt" untuk meningkatkan akurasi program. Berisikan daftar sinonim kata dari blogspot orang lain. Mohon tambahkan isinya untuk improvisasi akurasi.

- Tidak mengenal emoji, sehingga menyontek emoji masih diperbolehkan disini.

-----------------------------------------------------------------------------

Program Ini Jelek & Cara Mempercantik
   
Tingkat akurasi program ini masih rendah. Banyak hal yang perlu diperbaiki dari program ini. Berikut adalah list usulan yang terpikir di benak saya :

1. Pada mode Auto, berikan weight yang berbeda pada tiap n-Gram, semakin tinggi n-Gram semakin besar weightnya.

2. Program ini hanya menampilkan persentasi kemiripan teks, tapi tidak menunjukkan bagian mana yang mirip. Pemberian fitur highlight pada kata yang mirip akan sangat membantu penilaian teks.

3. Mengurangi false positive dengan menghilangkan kutipan orang lain. Dapat direalisasikan dengan RegEx jika kutipan sesuai format umum.

4. Tokenisasi masih terbilang blak-blakan, pemisahan simbol secara membabi buta dapat menyebabkan false positive. Jadi, spesialisasi tokenisasi diperlukan.

5. Isi file synbank.txt masih sedikit, perlu ditambah sinonim lain.

6. Program ini mungkin berfungsi dengan baik jika Plagiator men-copy paste teks, namun lain cerita jika Plagiator mengketik ulang dari sumber, DAN ia typo :/ Tentunya menurunkan tingkat akurasi program ini. Untuk itu, diperlukan sebuah list berisikan kata-kata typo ATAU simulasi n-Gram untuk mengecek typo.
