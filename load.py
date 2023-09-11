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
            "place_of_residence": "y21_q4",
            "has_spouse": "y21_q9",
            "has_children": "y21_q10",
            "children_count": "y21_q11",
            "major": "y21_q6",
        },
        1523: {
            "age": "y22_q2",
            "gender": "y22_q1",
            "educational_attainment": "y22_q5",
            "main_job_income": "y22_q100_1",
            "occupation": "y22_q32",
            "degree": "y22_q6",
            "self_learning": "y22_q67",
            "place_of_residence": "y22_q4",
            "has_spouse": "y22_q9",
            "has_children": "y22_q10",
            "children_count": "y22_q11",
            "major": "y22_q6",
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
                    "self_learning": row[key_dict['self_learning']] == '1',
                    "place_of_residence": row[key_dict['place_of_residence']],
                    "has_spouse": row[key_dict['has_spouse']] == '1',
                    "has_children": row[key_dict['has_children']] == '1',
                    "children_count": row[key_dict['children_count']] if row[key_dict['children_count']] != '' else None,
                    "major": row[key_dict['major']] if row[key_dict['major']] != '' else None,
                })

                # 1000件ごとにバルクインサート
                if i % 1000 == 0:
                    session.bulk_insert_mappings(Answer, data)
                    session.commit()
                    data = []
                i += 1

            # 調査番号とロード件数を出力
            print("survey_number: " + str(survey_number) + ", count: " + str(i))


loader = Loader()
loader.load_all()
