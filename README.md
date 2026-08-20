# Pygame_Platformer : PGZero ve Pygame Esasli 2D Platform Oyunu

Bu layihe Pygame Zero freymvorku uzerinde qurulmus 2D platformer macera oyunudur. Oyunda dinamik xarakter animasiyalari, fiziki toqquşma mexanizmi, sikkə toplama, can bərpası sistemi və fon musiqisi tətbiq olunmuşdur.

## Oyun Xususiyyetleri

* Qəhrəman Animasiyaları: Sakit dayanma (Idle), Qaçış (Run) və Tullanma (Jump) hərəkət dövrləri.
* Qravitasiya və Toqquşma Fizikası: Platformalar və divarlarla dəqiq blok toqquşması.
* Resurs Sistemi: Xəritə boyunca səpələnmiş sikkələrin toplanması və xalların hesablanması.
* Sağlamlıq və Bərpa: Düşmənlərlə təmasda can azalması və can qutuları vasitəsilə sağlamlığın bərpası.
* Audio Mühit: Dinamik fon musiqisi və interaktiv səs effektləri.

## Oyunun İdarəetmə Düymələri

| Düymə | Hərəkət |
| :--- | :--- |
| Sol Ox (`Left Arrow`) / A | Sola Hərəkət |
| Sağ Ox (`Right Arrow`) / D | Sağa Hərəkət |
| Yuxarı Ox (`Up Arrow`) / Space | Tullanma |
| Q | Oyundan Çıxış |

## Quraşdırma və İşə Salma

### 1: Repozitoriyanı Klonlamaq
```bash
git clone https://github.com/MahammadBabayevBhos/Pygame_Platformer.git
cd Pygame_Platformer
```

### 2: Asılılıqları Quraşdırmaq
```bash
pip install -r requirements.txt
```

### 3: Oyunu Başlatmaq
```bash
pgzrun main_game.py
```

## Proyekt Strukturu

| Qovluq / Fayl | Təsvir |
| :--- | :--- |
| `main_game.py` | Əsas oyun məntiqi, fizika və kadr yenilənməsi. |
| `images/` | Qəhrəman, düşmən, platforma və arxa fon spriteləri. |
| `music/` | Oyunun audio və fon musiqi faylları. |
| `requirements.txt` | Tələb olunan Pygame Zero asılılıqları. |

## Texnologiyalar

* Mühit: Python 3.8:3.12
* Oyun Freymvorku: Pygame Zero (pgzero), Pygame
