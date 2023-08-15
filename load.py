import csv
from answer import Answer
from setting import session
import os
from dotenv import load_dotenv

# 変数の設定
load_dotenv()
csvPath = os.getenv("CSV_PATH")
SurveyNumber = 1523

# 対象のレコードを事前に削除
session.query(Answer).filter(Answer.SurveyNumber == SurveyNumber).delete(synchronize_session='fetch')

data = []
with open(csvPath, 'r') as file:
    reader = csv.DictReader(file)
    i = 0
    for row in reader:
        reader = csv.DictReader(file)

        # 回答モデルにマッピング
        data.append({
            "SurveyNumber": SurveyNumber,
            "AnswerKey": row['key'],
            "UserID": row['pkey'],
            "Age": row['y22_q2']
        })

        # 1000件ごとにバルクインサート
        if i % 1000 == 0:
            session.bulk_insert_mappings(Answer, data)
            session.commit()
            data = []
        i += 1

    print(i)
