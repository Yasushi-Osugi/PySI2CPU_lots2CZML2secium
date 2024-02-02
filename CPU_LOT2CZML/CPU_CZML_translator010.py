import pandas as pd
import json
from datetime import datetime, timedelta





# CSVファイルを読み込む
df = pd.read_csv('CPU_OUT_FW_plan010.csv', names=['ISO_week_no', 'lot_id_yyyyww', 'PSI_flag', 'node_name', 'longitude', 'latitude', 'height', 'lot_size'])



## lot_idから右側の6文字（YYYYWW）を削除してlot_nameを取得
#df['lot_id'] = df['lot_id_yyyyww'].str[:-7]

# lot_idから左側の4文字（XXX_）を取得して、filtering
df['lot_id_name'] = df['lot_id_yyyyww'].str[:4]



## 特定のlot_idを指定
##target_lot_id = 'your_target_lot_id'  # ここに対象とするlot_idを指定します
#
#

# filtering STOP
#target_lot_id = 'CAN_'  # ここに対象とするlot_idを指定します
#
#
# フィルタリング
#df = df[df['lot_id_name'] == target_lot_id]





# 経度の調整
df.loc[df['PSI_flag'] == 's', 'longitude'] += 0.5
df.loc[df['PSI_flag'] == 'p', 'longitude'] -= 0.5

# BOXの一辺の長さを計算
df['lot_size'] *= 100

# BOXの色を設定
color_dict = {'s': [0, 0, 255, 255], 'i1': [165, 42, 42, 255], 'p': [255, 255, 0, 255]}
df['color'] = df['PSI_flag'].map(color_dict)

# 開始日と終了日を計算
start_date = datetime(2024, 1, 1)
df['start_date'] = df['ISO_week_no'].apply(lambda x: (start_date + timedelta(weeks=x-1)).strftime('%Y-%m-%dT12:00:00Z'))
df['end_date'] = df['ISO_week_no'].apply(lambda x: (start_date + timedelta(weeks=x)).strftime('%Y-%m-%dT11:59:59Z'))

# CZMLのBOX定義を生成
czml = []

for _, row in df.iterrows():
    czml.append({
        "id": row['lot_id_yyyyww'],
        "position": {
            "cartographicDegrees": [row['longitude'], row['latitude'], row['height']*10000]
        },
        "box": {
            "dimensions": {

                "cartesian": [row['lot_size']*5, row['lot_size']*5, row['lot_size']*5]

            },
            "material": {
                "solidColor": {
                    "color": {
                        "rgba": row['color']
                    }
                }
            },
            "show": [
                {
                    "interval": row['start_date'] + '/' + row['end_date'],
                    "boolean": True
                },
                {
                    "interval": row['end_date'] + '/9999-12-31T24:00:00Z',
                    "boolean": False
                }
            ]
        }
    })





# 各CZML定義をJSON形式の文字列に変換
czml_texts = [json.dumps(item, indent=2) for item in czml]

# CZMLのテキストをカンマと改行で結合
czml_text = ',\n'.join(czml_texts)

# CZMLのテキストをファイルに出力
with open('CPU2CZML010.czml', 'w') as f:
    f.write(czml_text)




## ************************
## CZMLをJSON形式のテキストに変換
## ************************
#czml_text = json.dumps(czml)
#
## CZMLのテキストをファイルに出力
#with open('output.czml', 'w') as f:
#    f.write(czml_text)


## ************************
## czmlのtextファイル出力
## ************************
#
#filename = "CPU_lots_czml.txt"
#
# textファイルの書き込みモード
#with open(filename, "w") as textfile:
#    for item in czml:
#        # json.dumpsを使用してPythonオブジェクトを文字列に変換
#        textfile.write(json.dumps(item) + '\n')
#
#
