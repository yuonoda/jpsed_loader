import sys
from sqlalchemy import Column, Integer, BigInteger, ForeignKey, String, Boolean, UniqueConstraint
from sqlalchemy.dialects.postgresql import INT4RANGE
from sqlalchemy.orm import relationship

from setting import Base, Engine, session

class Answer(Base):
    __tablename__ = 'answers_fact'
    __table_args__ = (
        (UniqueConstraint('survey_number', 'answer_key', name='survey_number_answer_key_uk')),
        {'comment': '回答のファクトテーブル'},
    )
    answer_id = Column('answer_id', BigInteger, primary_key=True, autoincrement=True)
    survey_number = Column('survey_number', Integer,
                           ForeignKey('surveys_dim.survey_number', onupdate='CASCADE', ondelete='CASCADE'))
    answer_key = Column('answer_key', Integer)

    user_ID = Column('user_id', BigInteger)
    age = Column('age', Integer)
    gender = Column('gender', Integer)
    educational_attainment = Column('educational_attainment', Integer,
                                    ForeignKey('educational_attainments_dim.key', onupdate='CASCADE',
                                               ondelete='CASCADE'))
    main_job_income = Column('main_job_income', Integer)
    occupation = Column('occupation', Integer,
                        ForeignKey('occupations_dim.key', onupdate='CASCADE', ondelete='CASCADE'))
    industry = Column('industry', Integer,
                        ForeignKey('industries_dim.key', onupdate='CASCADE', ondelete='CASCADE'))

    degree = Column('degree', Integer,
                    ForeignKey('degrees_dim.key', onupdate='CASCADE', ondelete='CASCADE'))
    self_learning = Column('self_learning', Boolean)
    place_of_residence = Column('place_of_residence', Integer,
                                ForeignKey('place_of_residences_dim.key', onupdate='CASCADE', ondelete='CASCADE'))
    has_spouse = Column('has_spouse', Boolean, comment='配偶者の有無')
    has_children = Column('has_children', Boolean, comment='子供の有無')
    children_count = Column('children_count', Integer, comment='子ども人数【ベース：子どもあり】')
    major = Column('major', Integer,
                   ForeignKey('majors_dim.key', onupdate='CASCADE', ondelete='CASCADE'))

    working_situation = Column('working_situation', Integer,
                               ForeignKey('working_situations_dim.key', onupdate='CASCADE', ondelete='CASCADE'))
    working_status = Column('working_status', Integer,
                            ForeignKey('working_statuses_dim.key', onupdate='CASCADE', ondelete='CASCADE'))
    employment_status = Column('employment_status', Integer,
                           ForeignKey('employment_statuses_dim.key', onupdate='CASCADE', ondelete='CASCADE'))



class Survey(Base):
    __tablename__ = 'surveys_dim'
    __table_args__ = {
        'comment': '調査の次元テーブル'
    }
    survey_number = Column('survey_number', Integer, primary_key=True)
    year = Column('year', Integer)


class Occupation(Base):
    __tablename__ = 'occupations_dim'
    __table_args__ = {
        'comment': '職種の次元テーブル'
    }
    key = Column('key', Integer, primary_key=True)
    title = Column('title', String)

    answers = relationship('Answer', backref='occupations_dim')


class EducationalAttainment(Base):
    __tablename__ = 'educational_attainments_dim'
    __table_args__ = {
        'comment': '学歴の次元テーブル'
    }
    key = Column('key', Integer, primary_key=True)
    title = Column('title', String)

    answers = relationship('Answer', backref='educational_attainments_dim')


class AgeClass(Base):
    __tablename__ = 'age_classes_dim'
    __table_args__ = {
        'comment': '年齢階級の次元テーブル'
    }
    key = Column('key', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String, nullable=False)
    age_range = Column('age_range', INT4RANGE, nullable=False)


class Degree(Base):
    __tablename__ = 'degrees_dim'
    __table_args__ = {
        'comment': '学位の次元テーブル'
    }
    key = Column('key', Integer, primary_key=True, autoincrement=True)
    area = Column('area', String, nullable=False)

    answers = relationship('Answer', backref='degrees_dim')


class PlaceOfResidence(Base):
    __tablename__ = 'place_of_residences_dim'
    __table_args__ = {
        'comment': '居住地の次元テーブル'
    }
    key = Column('key', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String, nullable=False)


class Major(Base):
    __tablename__ = 'majors_dim'
    __table_args__ = {
        'comment': '学部の次元テーブル'
    }
    key = Column('key', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String, nullable=False)


class WorkingSituation(Base):
    __tablename__ = 'working_situations_dim'
    __table_args__ = {
        'comment': '就業状態の次元テーブル'
    }
    key = Column('key', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String, nullable=False)


class WorkingStatus(Base):
    __tablename__ = 'working_statuses_dim'
    __table_args__ = {
        'comment': '就業形態の次元テーブル'
    }
    key = Column('key', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String, nullable=False)


class EmploymentStatus(Base):
    __tablename__ = 'employment_statuses_dim'
    __table_args__ = {
        'comment': '雇用形態の次元テーブル'
    }
    key = Column('key', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String, nullable=False)


class Industry(Base):
    __tablename__ = 'industries_dim'
    __table_args__ = {
        'comment': '業種の次元テーブル'
    }
    key = Column('key', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String, nullable=False)

def main(args):
    """
    メイン関数
    """
    Base.metadata.create_all(bind=Engine)

    # 調査マスタを追加
    surveys = [
        {"survey_number": 1523, "year": 2022},
        {"survey_number": 1429, "year": 2021},
        {"survey_number": 1349, "year": 2020},
        {"survey_number": 1279, "year": 2019},
        {"survey_number": 1227, "year": 2018},
        {"survey_number": 1164, "year": 2017},
        {"survey_number": 1088, "year": 2016},
    ]
    session.bulk_insert_mappings(Survey, surveys)
    session.commit()

    # 職種マスタを追加
    occupations = [
        {"key": 1, "title": "家政婦（夫）、ホームヘルパーなど"},
        {"key": 2, "title": "理容師"},
        {"key": 3, "title": "美容師"},
        {"key": 4, "title": "エステティシャン"},
        {"key": 5, "title": "その他生活衛生サービス職業従事者"},
        {"key": 6, "title": "和食調理師、すし職人"},
        {"key": 7, "title": "洋食調理師"},
        {"key": 8, "title": "中華料理調理師"},
        {"key": 9, "title": "その他調理職、バーテンダー"},
        {"key": 10, "title": "ウエイター・ウエイトレス"},
        {"key": 11, "title": "ホールスタッフ（パチンコ・遊技場）"},
        {"key": 12, "title": "宿泊施設接客"},
        {"key": 13, "title": "添乗員・ツアーコンダクター"},
        {"key": 14, "title": "その他接客・給仕職業"},
        {"key": 15, "title": "ビル・駐車場・マンション・ボイラー等管理"},
        {"key": 16, "title": "自動車・バイク整備士"},
        {"key": 17, "title": "機械保守・メンテナンス"},
        {"key": 18, "title": "サービススタッフ（ガソリンスタンド）"},
        {"key": 19, "title": "他に分類されないサービス職業従事者"},
        {"key": 20, "title": "自衛官、警察官"},
        {"key": 21, "title": "警備、守衛など"},
        {"key": 22, "title": "農耕作業者、造園職、養畜作業者、林業・漁業作業者"},
        {"key": 23, "title": "ドライバー（バン、ワゴン）"},
        {"key": 24, "title": "ドライバー（トラック）"},
        {"key": 25, "title": "ドライバー（バス）"},
        {"key": 26, "title": "ドライバー（2輪）"},
        {"key": 27, "title": "ドライバー（タクシー・ハイヤー）"},
        {"key": 28, "title": "鉄道運転従事者、電話交換手、郵便配達など"},
        {"key": 29, "title": "金属の製造・生産工程・修理作業者"},
        {"key": 30, "title": "機械の製造・生産工程・修理作業者"},
        {"key": 31, "title": "電気の製造・生産工程・修理作業者"},
        {"key": 32, "title": "自動車の製造・生産工程・修理作業者"},
        {"key": 33, "title": "食料品・日用品の製造・生産工程作業者"},
        {"key": 34, "title": "建設作業者（土木作業員）"},
        {"key": 35, "title": "建設作業者（建設作業員）"},
        {"key": 36, "title": "建設作業者（設備工事作業員）"},
        {"key": 37, "title": "その他の建設・土木・採掘作業者"},
        {"key": 38, "title": "清掃"},
        {"key": 39, "title": "配達、倉庫作業、その他"},
        {"key": 40, "title": "管理職（技術系）"},
        {"key": 41, "title": "管理職（事務職）"},
        {"key": 42, "title": "管理職（営業職）"},
        {"key": 43, "title": "管理職（専門職）"},
        {"key": 44, "title": "管理職（販売職）"},
        {"key": 45, "title": "管理職（サービス職）"},
        {"key": 46, "title": "スーパーバイザー"},
        {"key": 47, "title": "店長"},
        {"key": 48, "title": "管理職（その他）"},
        {"key": 49, "title": "総務"},
        {"key": 50, "title": "人事"},
        {"key": 51, "title": "労務"},
        {"key": 52, "title": "法務"},
        {"key": 53, "title": "広報"},
        {"key": 54, "title": "経営企画"},
        {"key": 55, "title": "営業事務"},
        {"key": 56, "title": "管理事務"},
        {"key": 57, "title": "国際業務"},
        {"key": 58, "title": "貿易事務"},
        {"key": 59, "title": "業務"},
        {"key": 60, "title": "在庫管理"},
        {"key": 61, "title": "商品管理"},
        {"key": 62, "title": "仕入"},
        {"key": 63, "title": "購買・資材"},
        {"key": 64, "title": "医療事務"},
        {"key": 65, "title": "秘書"},
        {"key": 66, "title": "受付"},
        {"key": 67, "title": "電話交換手"},
        {"key": 68, "title": "手配業務"},
        {"key": 69, "title": "スタッフコーディネーター"},
        {"key": 70, "title": "その他一般事務系職"},
        {"key": 71, "title": "企画"},
        {"key": 72, "title": "販売促進"},
        {"key": 73, "title": "マーケティング"},
        {"key": 74, "title": "宣伝"},
        {"key": 75, "title": "調査"},
        {"key": 76, "title": "商品開発"},
        {"key": 77, "title": "商品企画"},
        {"key": 78, "title": "バイヤー"},
        {"key": 79, "title": "マーチャンダイザー"},
        {"key": 80, "title": "店舗開発"},
        {"key": 81, "title": "その他企画・販促系事務職"},
        {"key": 82, "title": "財務、会計"},
        {"key": 83, "title": "経理"},
        {"key": 84, "title": "不動産営業"},
        {"key": 85, "title": "食品営業"},
        {"key": 86, "title": "医薬品営業"},
        {"key": 87, "title": "化学品営業"},
        {"key": 88, "title": "機械営業"},
        {"key": 89, "title": "電気・電子機器営業"},
        {"key": 90, "title": "通信営業"},
        {"key": 91, "title": "システム営業"},
        {"key": 92, "title": "銀行営業"},
        {"key": 93, "title": "保険営業"},
        {"key": 94, "title": "証券営業"},
        {"key": 95, "title": "旅行営業"},
        {"key": 96, "title": "その他の営業"},
        {"key": 97, "title": "キーパンチャー、パソコン、オペレーターなど"},
        {"key": 98, "title": "販売店員、ファッションアドバイザー"},
        {"key": 99, "title": "レジ"},
        {"key": 100, "title": "商品訪問販売従事者"},
        {"key": 101, "title": "不動産仲介・売買人、保険代理人など"},
        {"key": 102, "title": "その他の事務従事者"},
        {"key": 103, "title": "研究開発（化学）"},
        {"key": 104, "title": "研究開発（バイオテクノロジー）"},
        {"key": 105, "title": "農業技術者"},
        {"key": 106, "title": "畜産技術者"},
        {"key": 107, "title": "林業技術者"},
        {"key": 108, "title": "水産技術者"},
        {"key": 109, "title": "食品技術者"},
        {"key": 110, "title": "その他の農林水産業・食品技術者"},
        {"key": 111, "title": "研究開発（電気・電子）"},
        {"key": 112, "title": "研究開発（光関連技術）"},
        {"key": 113, "title": "研究開発（通信技術）"},
        {"key": 114, "title": "研究開発（半導体）"},
        {"key": 115, "title": "研究開発（機械）"},
        {"key": 116, "title": "研究開発（メカトロニクス）"},
        {"key": 117, "title": "アナログ回路設計"},
        {"key": 118, "title": "デジタル回路設計"},
        {"key": 119, "title": "電気回路設計"},
        {"key": 120, "title": "半導体開発設計"},
        {"key": 121, "title": "機械設計"},
        {"key": 122, "title": "メカトロ設計"},
        {"key": 123, "title": "電気通信技術者"},
        {"key": 124, "title": "制御設計"},
        {"key": 125, "title": "金型設計"},
        {"key": 126, "title": "その他電気・電子・機械設計関連職"},
        {"key": 127, "title": "化学技術者"},
        {"key": 128, "title": "その他の鉱工業技術者"},
        {"key": 129, "title": "技術開発（建築・土木・プラント・設備）"},
        {"key": 130, "title": "建築設計"},
        {"key": 131, "title": "土木設計"},
        {"key": 132, "title": "意匠設計"},
        {"key": 133, "title": "構造解析"},
        {"key": 134, "title": "プラント設計"},
        {"key": 135, "title": "空調設備設計"},
        {"key": 136, "title": "電気設備設計"},
        {"key": 137, "title": "CAD設計"},
        {"key": 138, "title": "その他設計"},
        {"key": 139, "title": "建築施工管理・現場監督・工事監理者"},
        {"key": 140, "title": "土木施工管理・現場監督・工事監理者"},
        {"key": 141, "title": "設備施工管理・現場監督・工事管理者"},
        {"key": 142, "title": "その他の建築・土木・測量技術者"},
        {"key": 143, "title": "研究開発（コンピュータ）"},
        {"key": 144, "title": "開発職（ソフトウエア関連職）"},
        {"key": 145, "title": "データベース系SE"},
        {"key": 146, "title": "制御系SE"},
        {"key": 147, "title": "ネットワークエンジニア"},
        {"key": 148, "title": "プログラマ"},
        {"key": 149, "title": "CGプログラマ"},
        {"key": 150, "title": "サポートエンジニア（ソフト）"},
        {"key": 151, "title": "システムアナリスト"},
        {"key": 152, "title": "システムコンサルタント"},
        {"key": 153, "title": "通信・ネットワークエンジニア"},
        {"key": 154, "title": "画像処理"},
        {"key": 155, "title": "CADオペレーター"},
        {"key": 156, "title": "WEB系プログラマ"},
        {"key": 157, "title": "WEB系アプリケーション開発"},
        {"key": 158, "title": "サーバ管理エンジニア"},
        {"key": 159, "title": "ローカライゼーションエンジニア"},
        {"key": 160, "title": "ITコンサルタント"},
        {"key": 161, "title": "セキュリティ技術者"},
        {"key": 162, "title": "ERPコンサルタント"},
        {"key": 163, "title": "その他ソフトウエア関連技術職"},
        {"key": 164, "title": "ECコンサルタント"},
        {"key": 165, "title": "WEBマスター"},
        {"key": 166, "title": "WEBプロデューサー・ディレクター"},
        {"key": 167, "title": "WEBデザイナー"},
        {"key": 168, "title": "セキュリティコンサルタント"},
        {"key": 169, "title": "WEBコンテンツ企画・制作"},
        {"key": 170, "title": "eビジネスプロデューサー・インキュベーター"},
        {"key": 171, "title": "その他のインターネット関連専門職"},
        {"key": 172, "title": "その他研究開発"},
        {"key": 173, "title": "カスタマーエンジニア"},
        {"key": 174, "title": "サポートエンジニア（ハード）"},
        {"key": 175, "title": "フィールドエンジニア"},
        {"key": 176, "title": "プロセスエンジニア"},
        {"key": 177, "title": "特許"},
        {"key": 178, "title": "工業デザイナー"},
        {"key": 179, "title": "その他エンジニア"},
        {"key": 180, "title": "薬剤師"},
        {"key": 181, "title": "医師、歯科医師、獣医師"},
        {"key": 182, "title": "保健師・助産師"},
        {"key": 183, "title": "看護師（準看護師を含む）"},
        {"key": 184, "title": "放射線技師、臨床検査技師、歯科技工士、理学療法士など"},
        {"key": 185, "title": "栄養士"},
        {"key": 186, "title": "マッサージ"},
        {"key": 187, "title": "カウンセラーなどその他医療専門職"},
        {"key": 188, "title": "福祉相談指導専門員"},
        {"key": 189, "title": "保育士"},
        {"key": 190, "title": "介護士"},
        {"key": 191, "title": "弁護士、弁理士、司法書士など"},
        {"key": 192, "title": "公認会計士、税理士など"},
        {"key": 193, "title": "文芸家、記者、編集者、校正者など"},
        {"key": 194, "title": "キャラクター、CGデザイナー"},
        {"key": 195, "title": "グラフィックデザイナー・エディトリアルデザイナー"},
        {"key": 196, "title": "ファッション関連デザイナー"},
        {"key": 197, "title": "写真家"},
        {"key": 198, "title": "その他美術家"},
        {"key": 199, "title": "経営・会計コンサルタントなど"},
        {"key": 200, "title": "ディーラー"},
        {"key": 201, "title": "ファンドマネージャー"},
        {"key": 202, "title": "アクチュアリ"},
        {"key": 203, "title": "ファイナンシャルプランナー"},
        {"key": 204, "title": "証券アナリスト"},
        {"key": 205, "title": "その他金融関連専門職"},
        {"key": 206, "title": "ゲームプロデューサー"},
        {"key": 207, "title": "ゲームディレクター"},
        {"key": 208, "title": "ゲームデザイナー"},
        {"key": 209, "title": "ゲームプログラマ"},
        {"key": 210, "title": "その他ゲーム関連専門職"},
        {"key": 211, "title": "コピーライター"},
        {"key": 212, "title": "イラストレーター"},
        {"key": 213, "title": "広告・出版・マスコミプロデューサー・ディレクター"},
        {"key": 214, "title": "その他広告・出版・マスコミ専門職"},
        {"key": 215, "title": "DTPオペレーター"},
        {"key": 216, "title": "印刷機オペレーター"},
        {"key": 217, "title": "その他印刷関連専門職"},
        {"key": 218, "title": "ファッション関連職"},
        {"key": 219, "title": "インテリア関連職"},
        {"key": 220, "title": "教員（小中高）"},
        {"key": 221, "title": "塾講師"},
        {"key": 222, "title": "インストラクター"},
        {"key": 223, "title": "通訳"},
        {"key": 224, "title": "分類不能の職業"},
    ]
    session.bulk_insert_mappings(Occupation, occupations)
    session.commit()

    # 学歴マスタを追加
    attainments = [
        {"key": 1, "title": "[卒業済]小学校・中学校"},
        {"key": 2, "title": "[卒業済]高等学校"},
        {"key": 3, "title": "[卒業済]専修各種学校（専門学校）"},
        {"key": 4, "title": "[卒業済]短期大学"},
        {"key": 5, "title": "[卒業済]高等工業専門学校"},
        {"key": 6, "title": "[卒業済]大学"},
        {"key": 7, "title": "[卒業済]大学院修士課程"},
        {"key": 8, "title": "[卒業済]大学院博士課程"},
        {"key": 9, "title": "[在学中]高等学校"},
        {"key": 10, "title": "専修各種学校（専門学校）"},
        {"key": 11, "title": "[在学中]短期大学"},
        {"key": 12, "title": "[在学中]高等工業専門学校"},
        {"key": 13, "title": "[在学中]大学"},
        {"key": 14, "title": "[在学中]大学院修士課程"},
        {"key": 15, "title": "[在学中]大学院博士課程"},
    ]
    session.bulk_insert_mappings(EducationalAttainment, attainments)
    session.commit()

    # 年齢階級マスタを追加
    age_classes = [
        {"name": "under20s", "age_range": "[0, 20)"},
        {"name": "20s", "age_range": "[20, 30)"},
        {"name": "30s", "age_range": "[30, 40)"},
        {"name": "40s", "age_range": "[40, 50)"},
        {"name": "50s", "age_range": "[50, 60)"},
        {"name": "60s", "age_range": "[60, 70)"},
        {"name": "over70s", "age_range": "[70, 100)"},
    ]
    session.bulk_insert_mappings(AgeClass, age_classes)
    session.commit()

    # 学位のマスタデータを追加
    degrees = [
        {"key": 1, "area": "人文科学"},
        {"key": 2, "area": "社会科学"},
        {"key": 3, "area": "自然科学"},
        {"key": 4, "area": "医学、薬学"},
        {"key": 5, "area": "建築"},
        {"key": 6, "area": "芸術"},
        {"key": 7, "area": "福祉"},
        {"key": 8, "area": "その他"},
    ]
    session.bulk_insert_mappings(Degree, degrees)
    session.commit()

    # 居住地のマスタデータを追加
    place_of_residences = [
        {"key": 1, "name": "北海道"},
        {"key": 2, "name": "青森県"},
        {"key": 3, "name": "岩手県"},
        {"key": 4, "name": "宮城県"},
        {"key": 5, "name": "秋田県"},
        {"key": 6, "name": "山形県"},
        {"key": 7, "name": "福島県"},
        {"key": 8, "name": "茨城県"},
        {"key": 9, "name": "栃木県"},
        {"key": 10, "name": "群馬県"},
        {"key": 11, "name": "埼玉県"},
        {"key": 12, "name": "千葉県"},
        {"key": 13, "name": "東京都"},
        {"key": 14, "name": "神奈川県"},
        {"key": 15, "name": "新潟県"},
        {"key": 16, "name": "富山県"},
        {"key": 17, "name": "石川県"},
        {"key": 18, "name": "福井県"},
        {"key": 19, "name": "山梨県"},
        {"key": 20, "name": "長野県"},
        {"key": 21, "name": "岐阜県"},
        {"key": 22, "name": "静岡県"},
        {"key": 23, "name": "愛知県"},
        {"key": 24, "name": "三重県"},
        {"key": 25, "name": "滋賀県"},
        {"key": 26, "name": "京都府"},
        {"key": 27, "name": "大阪府"},
        {"key": 28, "name": "兵庫県"},
        {"key": 29, "name": "奈良県"},
        {"key": 30, "name": "和歌山県"},
        {"key": 31, "name": "鳥取県"},
        {"key": 32, "name": "島根県"},
        {"key": 33, "name": "岡山県"},
        {"key": 34, "name": "広島県"},
        {"key": 35, "name": "山口県"},
        {"key": 36, "name": "徳島県"},
        {"key": 37, "name": "香川県"},
        {"key": 38, "name": "愛媛県"},
        {"key": 39, "name": "高知県"},
        {"key": 40, "name": "福岡県"},
        {"key": 41, "name": "佐賀県"},
        {"key": 42, "name": "長崎県"},
        {"key": 43, "name": "熊本県"},
        {"key": 44, "name": "大分県"},
        {"key": 45, "name": "宮崎県"},
        {"key": 46, "name": "鹿児島県"},
        {"key": 47, "name": "沖縄県"},
        {"key": 48, "name": "海外"},
    ]
    session.bulk_insert_mappings(PlaceOfResidence, place_of_residences)
    session.commit()

    # 学部のマスタデータを追加
    majors = [
        {"key": 1, "name": "人文科学"},
        {"key": 2, "name": "社会科学"},
        {"key": 3, "name": "自然科学"},
        {"key": 4, "name": "医学、薬学"},
        {"key": 5, "name": "建築"},
        {"key": 6, "name": "芸術"},
        {"key": 7, "name": "福祉"},
        {"key": 8, "name": "その他"},
    ]
    session.bulk_insert_mappings(Major, majors)
    session.commit()

    # 就業状態のマスタデータを追加
    working_situations = [
        {"key":1, "name":"おもに仕事をしていた（原則週5日以上の勤務）"},
        {"key":2, "name":"おもに仕事をしていた（原則週5日未満の勤務）"},
        {"key":3, "name":"通学のかたわらに仕事をしていた"},
        {"key":4, "name":"家事などのかたわらに仕事をしていた"},
        {"key":5, "name":"仕事を休んでいた（疾病などによる休職）"},
        {"key":6, "name":"仕事を休んでいた（閑散期で仕事がなかった）"},
        {"key":7, "name":"仕事を探していた"},
        {"key":8, "name":"通学をしていた"},
        {"key":9, "name":"家事・育児をしていた"},
        {"key":10, "name":"介護をしていた"},
        {"key":11, "name":"その他"},
    ]
    session.bulk_insert_mappings(WorkingSituation, working_situations)
    session.commit()

    # 就業形態のマスタデータを追加
    working_status = [
        {"key":1, "name":"会社・団体等に雇われていた"},
        {"key":2, "name":"会社などの役員"},
        {"key":3, "name":"自営業主（雇い人あり）"},
        {"key":4, "name":"自営業主（雇い人なし）"},
        {"key":5, "name":"家族従業者（飲食店・卸小売店・農業等の家族従業者"},
        {"key":6, "name":"内職"},
    ]
    session.bulk_insert_mappings(WorkingStatus, working_status)
    session.commit()

    # 雇用形態のマスタデータを追加
    employment_statuses = [
        {"key":1, "name":"正規の職員・従業員"},
        {"key":2, "name":"パート・アルバイト"},
        {"key":3, "name":"労働者派遣事業所の派遣社員"},
        {"key":4, "name":"契約社員"},
        {"key":5, "name":"嘱託"},
        {"key":6, "name":"その他"},
    ]
    session.bulk_insert_mappings(EmploymentStatus, employment_statuses)
    session.commit()

    # 業種のマスタデータを追加
    industries = [
        {"key":1, "name":"農林漁業"},
        {"key":2, "name":"鉱業"},
        {"key":3, "name":"総合工事業"},
        {"key":4, "name":"識別工事業（大工、とび、左官、石工など）"},
        {"key":5, "name":"設備工事業"},
        {"key":6, "name":"食料品製造業"},
        {"key":7, "name":"繊維工業、衣服・繊維製品製造業"},
        {"key":8, "name":"木材・木製品、家具、紙・パルプ"},
        {"key":9, "name":"印刷・同関連業"},
        {"key":10, "name":"化学工業、石油・石炭製品、プラスチック製品製造業"},
        {"key":11, "name":"ゴム、革、窯業・土石製品製造業"},
        {"key":12, "name":"鉄鋼業"},
        {"key":13, "name":"非鉄金属製造業"},
        {"key":14, "name":"金属製品製造業"},
        {"key":15, "name":"一般機械器具製造業"},
        {"key":16, "name":"総合電機"},
        {"key":17, "name":"重電・産業用電気機器"},
        {"key":18, "name":"コンピュータ・通信機器・OA機器関連"},
        {"key":19, "name":"家電・AV機器"},
        {"key":20, "name":"ゲーム・アミューズメント機器"},
        {"key":21, "name":"半導体・電子・電気部品"},
        {"key":22, "name":"その他の電気機械器具製造業"},
        {"key":23, "name":"自動車・鉄道・航空機等製造、同部品製造"},
        {"key":24, "name":"精密機械器具製造業"},
        {"key":25, "name":"その他の製造業"},
        {"key":26, "name":"電気・ガス・熱供給・水道業"},
        {"key":27, "name":"放送業"},
        {"key":28, "name":"通信業（電気通信業、信書送達業など）"},
        {"key":29, "name":"情報サービス・調査業"},
        {"key":30, "name":"インターネット付随サービス業"},
        {"key":31, "name":"映像・音声・文字情報制作業"},
        {"key":32, "name":"鉄道、道路旅客運送業"},
        {"key":33, "name":"道路貨物運送業"},
        {"key":34, "name":"倉庫業"},
        {"key":35, "name":"旅行業および運輸に付帯するサービス業"},
        {"key":36, "name":"その他の運輸業"},
        {"key":37, "name":"卸売業"},
        {"key":38, "name":"百貨店、ディスカウントストア"},
        {"key":39, "name":"織物・衣服・身の回り品小売業"},
        {"key":40, "name":"スーパー・ストア"},
        {"key":41, "name":"コンビニエンスストア"},
        {"key":42, "name":"その他の飲食料品小売業"},
        {"key":43, "name":"その他の小売業"},
        {"key":44, "name":"銀行・信託業"},
        {"key":45, "name":"信金、信用組合業"},
        {"key":46, "name":"貸金業、投資業等非預金信用機関"},
        {"key":47, "name":"証券業、商品先物取引業"},
        {"key":48, "name":"保険業"},
        {"key":49, "name":"その他金融"},
        {"key":50, "name":"不動産業"},
        {"key":51, "name":"飲食店"},
        {"key":52, "name":"旅館、ホテル、レジャー"},
        {"key":53, "name":"医療業（病院、歯科診療所など）"},
        {"key":54, "name":"社会保険、社会福祉（保育所、託児所、訪問介護など）"},
        {"key":55, "name":"教育（小・中・高等学校、短大、大学専修学校など）"},
        {"key":56, "name":"郵便局（郵便事業のみ）"},
        {"key":57, "name":"理美容、エステ、クリーニング、浴場"},
        {"key":58, "name":"駐車場業"},
        {"key":59, "name":"その他の生活関連サービス業"},
        {"key":60, "name":"自動車整備業"},
        {"key":61, "name":"物品賃貸業"},
        {"key":62, "name":"広告代理業"},
        {"key":63, "name":"専門サービス業"},
        {"key":64, "name":"その他の事業サービス業"},
        {"key":65, "name":"その他のサービス業"},
        {"key":66, "name":"公務"},
        {"key":67, "name":"他に分類されないもの"},
    ]
    session.bulk_insert_mappings(Industry, industries)
    session.commit()

    # (\d+)\s(.+)
    # {"key":$1, "name":"$2"},


if __name__ == "__main__":
    main(sys.argv)
