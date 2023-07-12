def isCyrillic(s: str):
  '''
  Символ кирилица?
  :param s: буковка
  :return: bool
  '''
  alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
  if s.lower() in alphabet:
    return True
  return False

def in10system(s: str, system: int):
  '''
  Перевод в 10СС
  :param s: число
  :param system: из какой СС переводим
  :return: 10СС
  '''
  lst = s.split()
  for i in range(len(lst)):
    lst[i] = int(lst[i], system)
  return ' '.join(lst)

def inXsystem(s: str, system: int, spase=False, bit=False):
  '''
  из 10СС куда-нибудь
  :param s: 10CC
  :param system: во что переводим
  :param spase: удалить пробелы
  :param bit: число до нужного количества бит - число бит
  :return: числа в нужной СС
  '''
  lst = s.split()
  for i in range(len(lst)):
    n = int(lst[i])
    p = 1
    ans = ""
    while (p * system <= n):
        p *= system
    while p:
      digit = n // p
      match digit:
        case 10:
          ans += 'a'
        case 11:
          ans += 'b'
        case 12:
          ans += 'c'
        case 13:
          ans += 'd'
        case 14:
          ans += 'e'
        case 15:
          ans += 'f'
        case _:
          ans += str(digit)

      n %= p
      p //= system
    lst[i] = ans

  if bit:
    for i in range(len(lst)):
      lst[i] = zeroToXbit(lst[i], bit)
  if spase:
    return ' '.join(lst)
  return ''.join(lst)

def inAscii(c): # В 10сс по ASCII
  '''
  получение ASCII кода в 10СС
  :param c: символ
  :return: код по ASCII
  '''
  if isCyrillic(c):
    if c == 'ё':
      c = 184
    elif c == "Ё":
      c = 168
    else:
      c = ord(c) - 848
  else:
    c = ord(c)
  return c

def textInAscii(s: str, system=10):
  '''
  Переводим текст в ASCII кода
  :param s: текст
  :param system: 10 или 16 ASCII код
  :return: ASCII
  '''
  res = ""
  for i in s:
    c = inAscii(i)
    if system == 16:
      c = hex(c)[2:]
    res += str(c) + " "
  return res

def fromAsciiToChar(x: int):
  '''
  ASCII в букву
  :param x: код ASCII
  :return: символ
  '''
  if 192 <= x <= 255 or x == 168 or x == 184:
    x += 848
  return chr(x)

def textAsciiToText(s: str, system=10):
  '''
  ДЕКдирование ASCII
  :param s: ASCII
  :param system: какая система 16СС или 10СС
  :return: текст
  '''
  if not (" " in s) and system == 16:
    s = inXbit(s, 2)
  res = ""
  lst = s.split()
  for i in lst:
    if system == 10:
      res += fromAsciiToChar(int(i))
    elif system == 16:
      res += fromAsciiToChar(int(i, 16))

  return res

def zeroToXbit(s: str, bit=8):
  '''
  Добавляем спереди нули
  :param s: строка
  :param bit: сколько надо бит в сумме
  :return: 00000111
  '''
  length = len(s)
  quantNul = bit - length
  if length < bit:
    s = "0" * quantNul + s

  return s

def inXbit(s: str, bit: int, sym=" "):
  '''
  Деление по определенному количеству битов
  :param s: строка
  :param bit: по сколько бит делить
  :param sym: какими символами делить
  :return: то что надо
  '''
  result = ""
  counter = 0
  for i in s:
    if counter >= bit:
      result += sym
      counter = 0
    result += i
    counter += 1
  return result

def splitBin(s: str):
  '''
  Деление по группам 1 и 0
  :param s: набор 1 и 0
  :return: отдельно 1 и ноль по элементам в списке
  '''
  lst = []
  num = ""
  group = num

  for digit in s:
    if digit == num:
      group += digit
    else:
      lst.append(group)
      num = digit
      group = digit

  lst.append(group)
  return lst

def eliasAddRemovZero(s: str, encoding=True):
  '''
  Гамма код добавляем/убираем нули
  :param s: элементик
  :param encoding: добавляем - True, убираем - False
  :return:
  '''
  if encoding:
    length = len(s) - 1
    s = "0" * length + s
  else:
    length = len(s) // 2
    s = s[length:]
  return s

def eliasDecoding(x: str):
  '''
  Разделяем на группы гамма код
  :param x: строка
  :return:
  '''
  counter = 0
  s = ""
  flag = False
  lst = []
  for i in x:
    if i == "0" and not flag:
      counter += 1
      s += i
    elif i == "0" and flag:
      s += i
      counter -= 1
    elif i == "1":
      if counter > 0 and not flag:
        s += i
        flag = True
      elif counter > 0 and flag:
        counter -= 1
        s += i
    if counter <= 0:
      if flag:
        flag = False
        lst.append(s)
        s = ""
      else:
        lst.append(i)
  return lst

def base64Char(c, decod=False):
  base64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
  if not decod:
    return base64[c]
  else:
    if c != "=":
      return base64.find(c)

def RLE_encoding(x: str):
  lst = [s for s in x]
  s = ""
  steps = []
  steps.append(f"\n1. Переведи в 16СС по табличке ASCII 1251:\n{''.join([hex(inAscii(i))[2:] + ' ' for i in lst])}\n")


  for i in range(len(lst)):
    lst[i] = inAscii(lst[i]) # перевод в 10сс, для ручного решения надо в 16сс!
    lst[i] = bin(lst[i])[2:] # Перевод в 2сс
    lst[i] = zeroToXbit(lst[i]) # Доводим до 8 бит

    s += lst[i]

  steps.append(f"2. Переводим в 2СС (по 8 бит):\n{s}\n")

  lst = splitBin(s[1:]) # Делим по группам
  steps.append(f"3. Делим по группам:\n{' '.join(lst)}\n")

  s = s[0] # Записываем первый символ
  step1 = f"{s}:"
  step2 = f"{s}:"
  step3 = f"{s}:"
  for i in range(len(lst)):
    lst[i] = len(lst[i]) # Записываем длину группы
    step1 += str(lst[i]) + " "
    lst[i] = bin(int(lst[i]))[2:] # Переводим в 2сс
    step2 += lst[i] + " "
    lst[i] = eliasAddRemovZero(lst[i]) # Добавляем нули
    step3 += lst[i] + " "
    s += lst[i]

  steps.append(f"4. Записываем первый символ и кол-ва в группах:\n{step1}\n")
  steps.append(f"5. Переводим в 2СС:\n{step2}\n")
  steps.append(f"6. Добавляем нули для гамма-кода:\n{step3}\n")

  print("\n".join(map(str, steps)))
  return s # Радость)

def RLE_decoding(x: str):
  x = x.replace(" ", "")
  steps = []

  first = x[0] # Отделяем первый символ
  s = x[1:] # Отделяем первый символ
  steps.append(f"\n1. Отделяем первый бит:\n{first}:{s}")

  lst = eliasDecoding(s) # Разделяем на группы
  steps.append(f"2. Разбиваем на гамма-группы:\n{first}:{' '.join(lst)}")

  lst = [eliasAddRemovZero(i, False) for i in lst] # Убираем нули
  lst = [int(i, 2) for i in lst] # Переводим в 10СС
  steps.append(f"3. Переводим в 10СС:\n{first}:{' '.join(lst)}")

  # Переводим в серии и соединяем
  s = ""
  for i in lst:
    s += first * i
    first = "0" if first == "1" else "1"
  steps.append(f"4. Переводим в серии:\n{' '.join(splitBin(s))}")
  steps.append(f"5. Соединяем:\n{s}")

  s = inXbit(s, 8) # Разделить по 8 бит
  steps.append(f"6. Делим по 8 бит:\n{s}")
  lst = s.split()
  steps.append(f"7. Переводим в 16СС:\n{' '.join([hex(int(i, 2))[2:] for i in lst])}\n")
  for i in range(len(lst)):
    # print(int(lst[i], 2))
    lst[i] = fromAsciiToChar(int(lst[i], 2)) # Перевод по аскии
  print("\n\n".join(map(str, steps)))
  return ''.join(lst)

def base64_encoding(x: str):
  lst = [inAscii(i) for i in x]# Перевод в 10сс по ASCII
  steps = []
  steps.append(f"\n1. Переведи по табличке:\n{' '.join([hex(i)[2:] for i in lst])}")


  lst = [zeroToXbit(bin(int(i))[2:]) for i in lst]# Перевод в 2сс
  steps.append(f"2. Переведи в 2СС:\n{' '.join(lst)}")

  s = inXbit(''.join(lst), 6)
  while s[-7] != " ":
    s = s.replace(" ", "")
    s += "00000000"
    s = inXbit(s, 6)
  steps.append(f"3. Разбей по 6 бит (не забудь про нолики в конце!):\n{s}")
  lst = s.split()

  lst = [int(i, 2) for i in lst]
  steps.append(f"4. Переведи в 10СС:\n{' '.join(lst)}")

  flag = True
  for i in range(len(lst)-1, -1, -1):
    if flag and lst[i] == 0:
      lst[i] = "="
    elif flag and lst[i] != 0:
      flag = False
      lst[i] = base64Char(lst[i])
    elif not flag:
      lst[i] = base64Char(lst[i])

  print("\n\n".join(map(str, steps)))
  return ''.join(lst)

def base64_decoding(x: str):
  x = x.replace(" ", "")
  lst = []
  steps = []
  for s in x:
    st = base64Char(s, True)
    if not (st is None):
      lst.append(st)
  steps.append(f"\n1. Переводим по таблице BASE64, = не считается:\n{' '.join(lst)}")

  lst = [zeroToXbit(bin(int(i))[2:], 6) for i in lst]
  steps.append(f"2. Переводим каждое число в 2СС (по 6 битов!):\n{' '.join(lst)}")

  s = ''.join(lst)
  s = inXbit(s, 8)
  lst = s.split()

  if len(lst[-1]) != 8:
    lst.pop()
  steps.append(f"3. Соединяем и делим по 8 бит (если в конце есть 8 нулей - убираем!):\n{' '.join(lst)}")

  lst = [int(i, 2) for i in lst]
  steps.append(f"4. Переводим в 16СС:\n{''.join([hex(i)[2:] + ' ' for i in lst])}")

  lst = [fromAsciiToChar(i) for i in lst]
  print("\n\n".join(map(str, steps)))
  return ''.join(lst)

# Сибирь
def sibirsCompletPyramid(length: int): #
  '''
  Составление пирамидки
  :param length: количество элементов
  :return: пирамидка/ключ
  '''
  count = 1
  lst = ["a"]
  while count < length:
    for i in range(len(lst)):
      lst[i] += "a"
      count += 1
      if count == length:
        return lst

    for i in range(2):
      lst.append("a")
      count += 1
      if count == length:
        return lst

    for i in range(len(lst)-2, -1, -1):
      lst[i] += "a"
      count += 1
      if count == length:
        return lst

  return lst

def sibirsWordsInPyramid(s: str):
  '''
  подстановка значений в пирамидку
  :param s: строка шифра
  :return: пирамидка с подставленными значениями
  '''
  pyramid = sibirsCompletPyramid(len(s))
  for i in range(len(pyramid)):
    pyramid[i] = s[:len(pyramid[i])]
    s = s[len(pyramid[i]):]
  return pyramid

def sibirsRead(lst: list):
  '''
  Чтение пирамидки
  :param lst: пирамидка
  :return: ответ
  '''
  row, col = -1, 2
  col_max = 3
  col_n = -1 # отвечает в плюс идем или в минус

  row_max = 2
  row_n = 1

  result = lst[0][0]

  while True:
    # увеличиваем колонку до максимума и идем обратно
    col += col_n

    if col == col_max:
      col_max += 2
      col_n *= -1
    elif col < 0:
      col = 0
      col_n *= -1

    row += row_n
    if row == row_max:
      row_max += 2
      row_n *= -1
    elif row < 0:
      row = 0
      row_n *= -1
    try:
      result += lst[row][col]
    except:
      break
  return result

def sibirsHard(s: str):
  '''
  Сибирь разделенная пробелами по 4 символа
  :param s: шифр
  :return: нормальный текст
  '''
  s = s.replace(" ", "")
  lst = sibirsWordsInPyramid(s)
  s = sibirsRead(lst)
  return s

def sibirsHardPlus(s: str):
  '''
  тот же hard, но он не стирает пробелы
  :param s: шифр
  :return: нормальная фраза
  '''
  lst = []
  counter = 0
  sl = ""
  for i in range(len(s)):
    if counter >= 4:
      lst.append(sl)
      sl = ""
      counter = 0
      continue
    sl += s[i]
    counter += 1
  lst.append(sl)
  s = sibirsWordsInPyramid(''.join(lst))
  s = sibirsRead(s)
  return s

def permutatLetter(s: str):
  '''
  Обмена пар символов
  '''
  ans = ""
  for i in range(0, len(s), 2):
    try:
      ans += s[i+1] + s[i]
    except IndexError:
      ans += s[i]
  return ans

def snickers(s: str, deleteSpase=True, deletePunct=True):
  '''
  торобоан
  :param s: строка
  :param deleteSpase: удалить пробелы
  :param deletePunct: удалить пунктуацию
  :return: строка наоборот
  '''
  res = s
  if deleteSpase:
    res = s.replace(" ", "")
  if deletePunct:
    res = ""
    for i in s:
      if i.isalpha() or i == " ":
        res += i
  return res[::-1]

def hamming_decoding(s: str):
  answer = ''
  lst = s.split()
  for i in range(len(lst)):
    line = lst[i]

    pr1 = int(line[0]) ^ int(line[2]) ^ int(line[4]) ^ int(line[6]) ^ int(line[8]) ^ int(line[10]) ^ int(line[12]) ^ int(line[14])
    pr2 = int(line[1]) ^ int(line[2]) ^ int(line[5]) ^ int(line[6]) ^ int(line[9]) ^ int(line[10]) ^ int(line[13]) ^ int(line[14])
    pr4 = int(line[3]) ^ int(line[4]) ^ int(line[5]) ^ int(line[6]) ^ int(line[11]) ^ int(line[12]) ^ int(line[13]) ^ int(line[14])
    pr8 = int(line[7]) ^ int(line[8]) ^ int(line[9]) ^ int(line[10]) ^ int(line[11]) ^ int(line[12]) ^ int(line[13]) ^ int(line[14])

    err = pr1 * 1 + pr2 * 2 + pr4 * 4 + pr8 * 8

    if err != 0:
      err -= 1
      a = '1' if line[err] == '0' else '0'
      line = line[:err] + a + line[err+1:]

    line = line[:7] + line[8:]
    line = line[:3] + line[4:]
    line = line[:1] + line[2:]
    line = line[:0] + line[1:]

    answer += str(line)
  # return textAsciiToText(in10system(inXbit(answer, 8), 2))
  return answer

def caesar(s: str):
  '''
  Цезарь
  :param s: шифр
  :return: вкусный салат
  '''
  result = ""
  for c in s:
    ans = ""
    upper = c.isupper()
    c = c.lower()
    if c.isalpha():
      if isCyrillic(c):
        if c in "абвгджзийклмнопрстуфхцчшщъыьэю":
          ans = chr(ord(c) + 1)
        elif c == 'е':
          ans = "ё"
        elif c == 'ё':
          ans = 'ж'
        elif c == 'я':
          ans = 'а'
      else:
        if c == 'z':
          ans = 'a'
        else:
          ans = chr(ord(c) + 1)
      if upper:
        ans = ans.upper()
    else:
      ans = c
    result += ans
  return result

def digitUnderstand(s: str):
  '''
  Разбиение числа по разрядам
  '''
  s = s[::-1]
  s = inXbit(s, 3)[::-1]
  return s

def ne_ta_rascladka(s: str):
  '''
  Меняет раскладку
  '''
  data = {'q': 'й', 'й': 'q', 'w': 'ц', 'ц': 'w', 'e': 'у', 'у': 'e', 'r': 'к', 'к': 'r', 't': 'е', 'е': 't', 'y': 'н',
           'н': 'y', 'u': 'г', 'г': 'u', 'i': 'ш', 'ш': 'i', 'o': 'щ', 'щ': 'o', 'p': 'з', 'з': 'p', '[': 'х', 'х': '[',
           ']': 'ъ', 'ъ': ']', '{': 'Х', 'Х': '{', '}': 'Ъ', 'Ъ': '}', 'a': 'ф', 'ф': 'a', 's': 'ы', 'ы': 's', 'd': 'в',
           'в': 'd', 'f': 'а', 'а': 'f', 'g': 'п', 'п': 'g', 'h': 'р', 'р': 'h', 'j': 'о', 'о': 'j', 'k': 'л', 'л': 'k',
           'l': 'д', 'д': 'l', ';': 'ж', 'ж': ';', "'": 'э', 'э': "'", ':': 'Ж', 'Ж': ':', '"': 'Э', 'Э': '"', 'z': 'я',
           'я': 'z', 'x': 'ч', 'ч': 'x', 'c': 'с', 'с': 'c', 'v': 'м', 'м': 'v', 'b': 'и', 'и': 'b', 'n': 'т', 'т': 'n',
           'm': 'ь', 'ь': 'm', ',': 'б', 'б': ',', '.': 'ю', 'ю': '.', '<': 'Б', 'Б': '<', '>': 'Ю', 'Ю': '>'}
  ans = ""
  punk = "[]{};:'\",.<>"
  for c in s:
    if c.isalpha() or c in punk:
      if c in "БЮ":
        c = data[c]
      else:
        upper = c.isupper() # Сохраняет регистр
        c = data[c.lower()]
        c = c.upper() if upper else c
    ans += c
  return ans

