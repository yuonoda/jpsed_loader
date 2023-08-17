import csv
from migrate import Answer
from setting import session
import os
from dotenv import load_dotenv


class Loader:
    KEY_DICT_BY_SURVEY = {
        1429: {
            "age": "y21_q2",
            "gender": "y21_q1",
            "educational_attainment": "y21_q5",
            "main_job_income": "y21_q100_1",
            "occupation": "y21_q32",
            "degree": "y21_q6",
            "self_learning": "y21_q69",
        },
        1523: {
            "age": "y22_q2",
            "gender": "y22_q1",
            "educational_attainment": "y22_q5",
            "main_job_income": "y22_q100_1",
            "occupation": "y22_q32",
            "degree": "y22_q6",
            "self_learning": "y22_q67",
        },
    }

    def __init__(self):
        load_dotenv()
        self.csvDir = os.getenv("CSV_DIR")

    def load_all(self) -> None:
        for survey_number in self.KEY_DICT_BY_SURVEY.keys():
            self.load(survey_number)

    def load(self, survey_number: int) -> None:

        # その調査のレコードを事前に削除
        session.query(Answer).filter(Answer.survey_number == survey_number).delete(synchronize_session='fetch')

        # キーの辞書を取得
        key_dict = self.KEY_DICT_BY_SURVEY[survey_number]

        # CSVを読み込み
        data = []
        csvPath = self.csvDir + str(survey_number) + ".csv"
        with open(csvPath, 'r') as file:
            reader = csv.DictReader(file)
            i = 0
            for row in reader:

                # 回答モデルにマッピング
                data.append({
                    "survey_number": survey_number,
                    "answer_key": row['key'],
                    "user_ID": row['pkey'],
                    "age": row[key_dict['age']],
                    "gender": row[key_dict['gender']],
                    "educational_attainment": row[key_dict['educational_attainment']],
                    "main_job_income": row[key_dict["main_job_income"]] if row[key_dict['main_job_income']] != '' else 0,
                    "occupation": row[key_dict['occupation']] if row[key_dict['occupation']] != '' else None,
                    "degree": row[key_dict['degree']] if row[key_dict['degree']] != '' else None,
                    "self_learning": row[key_dict['self_learning']] == '1'
                })

                # 1000件ごとにバルクインサート
                if i % 1000 == 0:
                    session.bulk_insert_mappings(Answer, data)
                    session.commit()
                    data = []
                i += 1

            print(i)


loader = Loader()
loader.load_all()
