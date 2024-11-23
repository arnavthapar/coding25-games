from random import randrange
from os import system
from time import sleep
files = {
    1: [[".py"], [".png"], [".jpeg", ".jpg"], [".css"], [".html"], [".txt"], [".csv"], [".md"], [".xml"], [".json"]],
    2: [[".java"], [".sh"], [".bat"], [".c", ".cc", ".cpp", ".cxx"], [".docx"], [".go"], [".pptx"], [".pdf"], [".php"], [".js"]],
    3: [[".cs"], [".rar"], [".zip"], [".bak", ".backup"], [".lua"], [".apk"], [".exe"], [".bin"], [".dmg"], [".mov"]],
    4: [[".uot", ".odt"], [".sqlite"], [".flac"], [".mp3"], [".wav"], [".avi"], [".mp4"], [".mkv"], [".log"], [".conf"]],
    5: [[".asp"], [".jsp"], [".swift"], [".kt", ".kts"], [".rs"], [".iso"], [".rb"], [".pl"], [".r"], [".xlsx", "xls"]],
    6: [[".tnsp"], [".yml", ".yaml"], [".toml"], [".ini"], [".json5"], [".lock"], [".tar.gz"], [".tmp"], [".old"], [".crt"]]}
desc = {
    1: ["the file type for Python files.", "the popular image format with lossless compression and transparency support.",
        "the common image format often used for photographs.", "the file type for Cascading Style Sheets.",
        "the file type for web pages written in HTML.", "the file type for plain text files.",
        "the file type for spreadsheets with comma-separated values.", "the file type for Markdown files.",
        "the file type for eXtensible Markup Language files.", "the file type for JavaScript Object Notation files."],
    2: ["the file type for Java files.", "the file type for shell script files.", "the file type for batch script files.",
        "the file type for C or C++ files.", "the file type for Microsoft Word documents.",
        "the file type for Go programming language files.", "the file type for Microsoft PowerPoint presentations.",
        "the file type for Portable Document Format files.", "the file type for PHP: Hypertext Preprocessor files.",
        "the file type for JavaScript files."],
    3: ["the file type for C# files.", "the file type for RAR archive files.", "the file type for ZIP archive files.",
        "the file type for backup files.", "the file type for Lua programming language files.",
        "the file type for Android application packages.", "the file type for executable files.",
        "the file type for binary files.", "the file type for macOS Disk Image files.",
        "the file type for QuickTime movie files."],
    4: ["the standard file type for LibreOffice text documents.", "the file type for SQLite database files.",
        "the file type for FLAC audio files.", "the file type for MP3 audio files.", "the file type for WAV audio files.",
        "the file type for AVI video files.", "the file type for MP4 video files.", "the file type for MKV video files.",
        "the file type for log files.", "the file type for configuration files."],
    5: ["the file type for Active Server Pages files.", "the file type for JavaServer Pages files.",
        "the file type for Swift programming language files.", "the file type for Kotlin files.",
        "the file type for Rust programming language files.", "the file type for disc image files.",
        "the file type for Ruby programming language files.", "the file type for Perl programming language files.",
        "the file type for R programming language files.", "the file type for Microsoft Excel spreadsheets."],
    6: ["the file type for all files on a TI Nspire CX II Calculator.", "the file type for YAML Ain't Markup Language files (Also known as Yet Another Markup language).",
        "the file type for TOML files.", "the file type for initialization files.", "the file type for JSON5 files.",
        "the file type for lock files.", "the file type for compressed tarball files.", "the file type for temporary files.",
        "the file type for old version files.", "the file type for public key certificates."]}
for i in range(6):
    prev_randoms = []
    for _ in range(5):
        m = randrange(0, 10)
        while m in prev_randoms:
            m = randrange(0, 10)
        prev_randoms.append(m)
        system('clear')
        print(f"Round {i+1}")
        answer = input(f"Type {desc[i+1][m]} => ")
        if answer in files[i+1][m]:
            print("Correct. Next,")
            sleep(1)
        else:
            print("That's incorrect.")
            string = ""
            for k in files[i+1][m]:
                string += k + ", "
            s = " was" if len(files[i+1][m]) > 1 else "s were"
            print(f"The correct answer{s} {string}")
            quit()
print('You won! Great job.')