@echo off
REM lat2cyr.bat - Convert Latin letters (typed on EN layout) to Cyrillic (RU layout)
REM Example: ghbdtn -> привет
REM Save this file as UTF-8 (with BOM recommended).

chcp 65001 >nul
setlocal ENABLEDELAYEDEXPANSION

REM Read input either from args or prompt
set "input=%*"
if "%input%"=="" (
  set /p "input=Введите текст латиницей (например ghbdtn): "
)

REM Pass the input to PowerShell via STDIN to avoid quoting issues
echo %input% | powershell -NoProfile -Command ^
  "$s = [Console]::In.ReadToEnd().TrimEnd();" ^
  "$map = @{ 'q'='й'; 'w'='ц'; 'e'='у'; 'r'='к'; 't'='е'; 'y'='н'; 'u'='г'; 'i'='ш'; 'o'='щ'; 'p'='з'; '['='х'; ']'='ъ';" ^
  "               'a'='ф'; 's'='ы'; 'd'='в'; 'f'='а'; 'g'='п'; 'h'='р'; 'j'='о'; 'k'='л'; 'l'='д'; ';'='ж'; '''='э';" ^
  "               'z'='я'; 'x'='ч'; 'c'='с'; 'v'='м'; 'b'='и'; 'n'='т'; 'm'='ь'; ','='б'; '.'='ю'; '`'='ё';" ^
  "               'Q'='Й'; 'W'='Ц'; 'E'='У'; 'R'='К'; 'T'='Е'; 'Y'='Н'; 'U'='Г'; 'I'='Ш'; 'O'='Щ'; 'P'='З'; '{'='Х'; '}'='Ъ';" ^
  "               'A'='Ф'; 'S'='Ы'; 'D'='В'; 'F'='А'; 'G'='П'; 'H'='Р'; 'J'='О'; 'K'='Л'; 'L'='Д'; ':'='Ж'; '\"'='Э';" ^
  "               'Z'='Я'; 'X'='Ч'; 'C'='С'; 'V'='М'; 'B'='И'; 'N'='Т'; 'M'='Ь'; '<'='Б'; '>'='Ю'; '~'='Ё' };" ^
  "$out = ($s.ToCharArray() | ForEach-Object { if ($map.ContainsKey($_)) { $map[$_] } else { $_ } }) -join '';" ^
  "[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new();" ^
  "Write-Output $out;" ^
  "try { Set-Clipboard -Value $out } catch {}"

echo.
echo Готово.
echo Текст также скопирован в буфер обмена (если поддерживается).
endlocal
