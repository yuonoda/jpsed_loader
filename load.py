import csv
from answer import Answer
from setting import session
import os
from dotenv import load_dotenv


class Loader:
    def __init__(self):
        load_dotenv()
        self.csvPath = os.getenv("CSV_PATH")

    def load(self, survey_number: int) -> None:
        # 対象のレコードを事前に削除
        session.query(Answer).filter(Answer.SurveyNumber == survey_number).delete(synchronize_session='fetch')

        # CSVを読み込み
        data = []
        with open(self.csvPath, 'r') as file:
            reader = csv.DictReader(file)
            i = 0
            for row in reader:
                # 回答モデルにマッピング
                data.append({
                    "SurveyNumber": survey_number,
                    "AnswerKey": row['key'],
                    "UserID": row['pkey'],
                    "Age": row['y22_q2'],
                    "Gender": row['y22_q1'],
                    "EducationalAttainment": row['y22_q5'],
                    "MainJobIncome": row['y22_q100_1'] if row['y22_q100_1'] != '' else 0,
                })

                # 1000件ごとにバルクインサート
                if i % 1000 == 0:
                    session.bulk_insert_mappings(Answer, data)
                    session.commit()
                    data = []
                i += 1

            print(i)


loader = Loader()
loader.load(1523)
