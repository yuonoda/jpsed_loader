import sys
from sqlalchemy import Column, Integer, String
from setting import Base, Engine

class Answer(Base):
    __tablename__ = 'answers_fact'
    __table_args__ = {
        'comment': '回答のファクトテーブル'
    }
    SurveyNumber = Column('survey_number', Integer, primary_key=True)
    AnswerKey = Column('answer_key', String(25), primary_key=True,)

    UserID = Column('user_id', Integer)
    Age = Column('age', Integer)


def main(args):
    """
    メイン関数
    """
    Base.metadata.create_all(bind=Engine)

if __name__ == "__main__":
    main(sys.argv)