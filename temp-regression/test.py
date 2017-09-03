import urllib.request
import json

data =  {
  "Inputs": {
    "input1":{
      "ColumnNames": [
        "気温(℃)", "日照時間(時間)", "現地気圧(hPa)", "降水量(mm)",
        "日射量(MJ/㎡)", "相対湿度(％)"
        ],
        "Values": [
          [ 
            "0", "1", "1000", "0.3", "3", "20"
          ]
        ]
      },
    },
  "GlobalParameters": {}
}

body = str.encode(json.dumps(data))

url = '{your searvice url}'
api_key = '{your api key}'
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}


req = urllib.request.Request(url, body, headers) 
with urllib.request.urlopen(req) as response:
  result_json = response.read().decode('utf-8')
  result = json.loads(result_json)
  weathers = result['Results']['output1']['value']['Values'][0]
  temp = weathers[len(weathers)-1]
  print("予測気温は %s ℃です"%temp)
  