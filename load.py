import csv
from answer import Answer
from setting import session
import os
from dotenv import load_dotenv


class Loader:
    KEY_DICT_BY_SURVEY = {
        1523: {
            "Age": "y22_q2",
            "Gender": "y22_q1",
            "EducationalAttainment": "y22_q5",
            "MainJobIncome": "y22_q100_1"
        },
    }

    def __init__(self):
        load_dotenv()
        self.csvPath = os.getenv("CSV_PATH")

    def load(self, survey_number: int) -> None:
        # 対象のレコードを事前に削除
        session.query(Answer).filter(Answer.SurveyNumber == survey_number).delete(synchronize_session='fetch')

        # キーの辞書を取得
        key_dict = self.KEY_DICT_BY_SURVEY[survey_number]

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
                    "Age": row[key_dict['Age']],
                    "Gender": row[key_dict['Gender']],
                    "EducationalAttainment": row[key_dict['EducationalAttainment']],
                    "MainJobIncome": row[key_dict["MainJobIncome"]] if row[key_dict['MainJobIncome']] != '' else 0,
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
