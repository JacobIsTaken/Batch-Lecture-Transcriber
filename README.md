# Batch Lecture Transcriber

Ten prosty skrypt w Pythonie pozwala na masową transkrypcję nagrań wideo (np. wykładów) na tekst za pomocą modelu Whisper od OpenAI oraz FFmpeg. Skrypt jest dostosowany do pracy w określonym środowisku folderowym i zapisuje transkrypcje oraz czas przetwarzania każdego pliku.

## Wymagania

Przed uruchomieniem skryptu upewnij się, że masz zainstalowane:

1. **Python 3.x**  
   Pobierz Python ze strony [python.org](https://www.python.org/downloads/).

2. **Git**  
   Pobierz i zainstaluj Git ze strony [git-scm.com](https://git-scm.com/downloads).

3. **Whisper od OpenAI**  
   Zainstaluj model Whisper poleceniem:

   ```bash
   pip install git+https://github.com/openai/whisper.git
   ```

4. **FFmpeg**  
   Pobierz i zainstaluj FFmpeg ze strony [ffmpeg.org](https://ffmpeg.org/download.html). Upewnij się, że jest dostępny w PATH.

   [Polecam ten poradnik aby zainstalować ffmpeg](https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/)

---

## Struktura Folderów

```text
/twoj_folder_projektu
    ├── recordings/
    │   └── (umieść tutaj swoje pliki .mp4)
    ├── extracted/
    │   └── (skrypt zapisze tutaj transkrypcje)
    ├── logs.txt
    └── batch_transcriber.py  (skrypt Python)
```

- **`recordings/`**: Folder, do którego należy dodać pliki `.mp4` do przetworzenia.
- **`extracted/`**: Folder, w którym skrypt zapisze transkrypcje tekstowe.
- **`logs.txt`**: Plik, w którym zapisywane będą logi z czasem przetwarzania.

---

## Jak Użyć Skryptu

1. Umieść wszystkie pliki `.mp4` w folderze `recordings/`.

2. Jeśli chcesz zmienić ustawienia, edytuj zmienne w skrypcie:
   - **`whisper_model`**: Wybierz model (`small`, `medium`, `large`, `turbo`).
        - `small` (najszybszy, mniej dokładny)
        - `medium` (równowaga między szybkością a dokładnością)
        - `large` (najdokładniejszy, ale najwolniejszy)
        - `turbo` (szybszy model, dostosowany do wydajności)
   - **`whisper_language`**: Wprowadź kod języka (np. `pl` dla polskiego, `en-US` dla angielskiego).

3. Uruchom skrypt:

   ```bash
   python batch_transcriber.py
   ```

4. Skrypt wykona następujące kroki:
   - Przekształci każde wideo `.mp4` na plik audio `.mp3`.
   - Zastosuje filtry dźwiękowe, aby poprawić jakość audio (normalizacja głośności, filtr dolnoprzepustowy, filtr wysokoprzepustowy).
   - Użyje modelu Whisper do transkrypcji audio na tekst.
   - Zapisze transkrypcję w pliku `.txt` w folderze `extracted/`.
   - Zapisze czas przetwarzania każdego pliku w pliku `logs.txt`.

5. Po zakończeniu transkrypcji skrypt usunie plik audio.

## Pliki Wyjściowe

- Transkrypcja każdego wideo zostanie zapisana w folderze `extracted/` w pliku `.txt`, który będzie miał nazwę odpowiadającą nazwie wideo, np.  
  `wyklad_01_small.txt`

- Czas przetwarzania każdego pliku zostanie zapisany w pliku `logs.txt`. Na przykład:

```text
2025-01-02 14:30:45 - Processed "lecture_01.mp4" in 0:02:15 | Used model: small
2025-01-02 14:33:00 - Processed "lecture_02.mp4" in 0:03:45 | Used model: medium
```
