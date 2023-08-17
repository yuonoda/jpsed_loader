import sys
from sqlalchemy import Column, Integer, BigInteger, ForeignKey, String, Boolean
from sqlalchemy.dialects.postgresql import INT4RANGE
from sqlalchemy.orm import relationship

from setting import Base, Engine, session


class Answer(Base):
    __tablename__ = 'answers_fact'
    __table_args__ = {
        'comment': '回答のファクトテーブル'
    }
    survey_number = Column('survey_number', Integer, primary_key=True)
    answer_key = Column('answer_key', Integer, primary_key=True, )

    user_ID = Column('user_id', BigInteger)
    age = Column('age', Integer)
    gender = Column('gender', Integer)
    educational_attainment = Column('educational_attainment', Integer,
                        ForeignKey('educational_attainments_dim.key', onupdate='CASCADE', ondelete='CASCADE'))
    main_job_income = Column('main_job_income', Integer)
    occupation = Column('occupation', Integer,
                        ForeignKey('occupations_dim.key', onupdate='CASCADE', ondelete='CASCADE'))
    degree = Column('degree', Integer,
                    ForeignKey('degrees_dim.key', onupdate='CASCADE', ondelete='CASCADE'))
    self_learning = Column('self_learning', Boolean)

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

def main(args):
    """
    メイン関数
    """
    Base.metadata.create_all(bind=Engine)

    # 職種マスタを追加
    occupations =[
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
        {"key":1, "area": "人文科学"},
        {"key":2, "area": "社会科学"},
        {"key":3, "area": "自然科学"},
        {"key":4, "area": "医学、薬学"},
        {"key":5, "area": "建築"},
        {"key":6, "area": "芸術"},
        {"key":7, "area": "福祉"},
        {"key":8, "area": "その他"},
    ]
    session.bulk_insert_mappings(Degree, degrees)
    session.commit()

if __name__ == "__main__":
    main(sys.argv)