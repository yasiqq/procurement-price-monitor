import requests

def read_quotes_from_iss():

   url = 'https://iss.moex.com/iss/history/engines/currency/markets/selt/boards/CETS/securities/GLDRUB_TOM.json?from=2024-10-08&till=2026-10-27'

   # отправляем запрос
   initial_response = requests.get(url, timeout=5) # ответ = запрос.url
   # проверяем успешность ответа
   initial_response.raise_for_status()
   # преобразование в json
   initial_data = initial_response.json()

   all_rows = []
   cursor_data = initial_data["history.cursor"]["data"]

   for start in range(cursor_data[0][0], cursor_data[0][1], cursor_data[0][2]):
      params = {
          "start": start
      }

      page_response = requests.get(url, params=params)
      page_response.raise_for_status()

      page_data = page_response.json()

      for row in page_data["history"]["data"]:
         dict_row = dict(zip(page_data["history"]["columns"], row))
         all_rows.append(dict_row)

   return all_rows



