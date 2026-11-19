# AI Story TikTok — Brief untuk Claude

> Fail ni arahan untuk Claude. Setiap kali session buka repo ni, Claude baca fail ni dulu dan ikut.

## 0. MOD SEMASA: CapCut (separuh autopilot)
- **Claude TIDAK generate gambar/video.** Generate dibuat manual oleh aku dalam CapCut (Seedance 2.0 Mini).
- **Tugas Claude:** sediakan **pek episod** lengkap supaya aku cuma copy-paste dan klik.
- Aku post sendiri ke TikTok terus dari CapCut.
- (Mod Higgsfield autopilot penuh ada di bahagian 9, untuk masa depan. Jangan guna kecuali aku suruh.)

## 1. Matlamat
- Naikkan akaun TikTok **@[username]** ke **1,000 followers** supaya layak TikTok Shop affiliate.
- Cara: siri cerita seram animasi 3D bersiri, 1 episod sehari, supaya orang follow untuk tunggu episod seterusnya.

## 2. Siri (Story Bible)
- **Tajuk siri:** Rumah Sewa Lorong 13
- **Genre:** Seram / misteri
- **Bahasa:** Bahasa Melayu santai, gaya cakap orang muda KL
- **Gaya visual:** Animasi 3D gaya filem animasi, pencahayaan gelap dan suram, warna biru kehijauan waktu malam, kuning malap lampu rumah
- **Tone:** Suspen perlahan, seram dibina sikit-sikit, setiap episod ada satu klu baru, twist di hujung
- **Premis:** Aina, graduan baru, sewa rumah teres lama di Lorong 13 sebab sewa dia murah gila. Setiap malam tepat jam 3:13 pagi, ada benda pelik berlaku. Makin dia siasat, makin dia sedar penyewa sebelum dia hilang tanpa jejak, dan tuan rumah tahu sesuatu.

### Watak
| Nama | Umur | Rupa (WAJIB sama setiap episod) | Personaliti |
|---|---|---|---|
| **Aina** | 24 | Perempuan Melayu, tudung bawal maroon, cardigan kelabu, mata bulat, lesung pipit kiri, beg galas hitam | Berani tapi penakut dalam diam, suka cakap sorang-sorang, degil nak tahu |
| **Pak Mail** | 60-an | Lelaki kurus, kopiah putih lusuh, baju Melayu coklat pudar, misai putih nipis, selalu pegang tasbih kayu | Senyum tapi mata tak senyum, jawab soalan dengan soalan |
| **Hafiz** | 8 | Budak jiran, rambut cepak, baju T kuning besar, seluar pendek biru, selipar jepun, pegang lampu suluh kecil | Satu-satunya yang berani cakap pasal "kakak dulu" |
| **"Kakak Dulu"** | ? | Hanya nampak dari belakang: rambut panjang hitam basah, baju kurung putih kusam. **Muka tak pernah ditunjuk** sampai finale | Misteri utama siri |

### Lokasi tetap
- Rumah teres lama satu tingkat, cat hijau pudar, pagar besi berkarat, nombor "13" senget kat pintu
- Dalam rumah: ruang tamu dengan jam dinding kayu (jarum berhenti di 3:13), bilik belakang berkunci, dapur dengan tingkap menghadap belukar

### Arka cerita
- **Ep 1–5:** Aina pindah masuk. Bunyi ketukan jam 3:13. Jumpa barang penyewa lama. Hafiz bagi amaran.
- **Ep 6–12:** Bilik belakang terbuka sendiri. Jumpa diari penyewa lama. Pak Mail mula mencurigakan.
- **Ep 13–20:** Rahsia rumah terbongkar sikit-sikit. Twist besar: kaitan Pak Mail dan "Kakak Dulu".
- **Finale (Ep 20-an):** Muka "Kakak Dulu" ditunjuk. Penamat terbuka untuk Season 2.

## 3. Format Episod
- Panjang: **30–60 saat**, nisbah **9:16**
- **3 saat pertama:** hook kuat (bunyi pelik, visual mengejut, atau soalan terus kepada penonton)
- **Akhir episod:** cliffhanger + teks "Part [N+1] esok malam 🕒"
- Voiceover BM (suara Aina, orang pertama, perlahan, berbisik masa saat seram) + sari kata
- Komposisi: **~8 gambar** (beri gerakan zoom/pan dalam CapCut) + **3 klip video 5 saat** untuk saat paling seram. Kalau kredit CapCut longgar, boleh tukar lebih banyak gambar jadi video.

## 4. Pek Episod (apa Claude kena hasilkan)
Setiap episod → satu fail `episodes/ep-XX.md` dengan bahagian ini, ikut turutan:
1. **Ringkasan** 2 ayat + sambungan dari cliffhanger episod lepas
2. **Jadual shot**: setiap shot ada nombor, masa (saat), jenis (GAMBAR / VIDEO), reference yang kena upload, dan **prompt dalam Bahasa Inggeris** (model faham lebih baik), sedia untuk copy-paste
3. **Skrip voiceover BM** dengan masa, ikut shot
4. **Teks atas skrin** (hook, cliffhanger)
5. **Cadangan bunyi/muzik**
6. **Caption TikTok + hashtag**
7. **Checklist** langkah demi langkah dalam CapCut

### Peraturan prompt
- Setiap prompt watak MESTI ulang rupa penuh watak (dari jadual watak) supaya konsisten.
- Setiap prompt MESTI ada gaya: `3D animated film style, cinematic, dark moody lighting, vertical 9:16`
- Prompt video: terangkan **satu gerakan je** yang jelas (model 5 saat tak boleh buat banyak aksi).
- Jangan minta teks dalam gambar (AI selalu rosakkan tulisan). Teks letak dalam CapCut.

## 5. Aliran Kerja Claude
1. Baca `episodes/log.md` untuk tahu episod terakhir dan cliffhanger dia.
2. Tulis `episodes/ep-XX.md` ikut bahagian 4.
3. Kemas kini `episodes/log.md` (nombor, ringkasan, cliffhanger, status: "pek siap").
4. Commit dan push.
5. Bila aku bagitahu dah post, kemas kini status jadi "dah post" + link + prestasi kalau aku bagi.

## 6. Peraturan (WAJIB)
- Jadual post: **1 episod sehari, jam 8:30 malam waktu Malaysia**
- Setiap video **mesti label "AI-generated"** di TikTok.
- Jangan guna muka/nama orang sebenar, jenama, atau watak dari filem/cerita sedia ada.
- Seram yang sesuai untuk TikTok: suspen dan atmosfera. Tiada darah melampau, kecederaan grafik, atau bunuh diri.
- Jangan ulang plot atau visual yang sama. Setiap episod mesti ada perkembangan cerita.
- Kalau tak pasti, tanya aku. Jangan teka.

## 7. Hashtag & Caption
- Hashtag tetap: #ceritaseram #rumahsewalorong13 #seramMalaysia #ceritamelayu #animasi3d #fyp
- Gaya caption: 1 ayat suspen + soalan untuk penonton komen
- Bio akaun: "Cerita seram bersiri setiap malam 8:30 🕒 Follow supaya tak terlepas part seterusnya"

## 8. Struktur Repo
```
CLAUDE.md          ← fail ni
references/        ← gambar reference watak & lokasi (simpan yang terbaik, guna berulang)
references/prompts.md ← prompt untuk buat gambar reference
episodes/log.md    ← rekod semua episod
episodes/ep-XX.md  ← pek setiap episod
```

## 9. (Masa depan) Mod Higgsfield autopilot penuh
Guna hanya bila aku suruh tukar.
- Video: `seedance_2_0_mini`, 5 saat, `9:16`, `720p`, `generate_audio: false` (~5 kredit/klip)
- Gambar: `gpt_image_2_6`, `9:16` (~0.25 kredit/gambar)
- Had: 25 kredit/episod, 800 kredit/bulan, maksimum 2 kali generate semula setiap klip
- Jangan tukar model tanpa tanya. Semak baki kredit dulu. Mod semak: hantar video, tunggu approve sebelum post.

## 10. Prestasi
- Selepas setiap 5 episod, semak episod mana paling banyak view/follow dan laraskan gaya.
