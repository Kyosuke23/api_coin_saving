from fastapi import FastAPI
from pymongo import MongoClient
from bson.json_util import dumps
from datetime import date, datetime

# ローカル起動コマンド uvicorn main:app --reload --host 0.0.0.0

app = FastAPI()
CONNECTION_URL = 'mongodb://cluster0_user:cluster0_pass@cluster0-shard-00-00.bxkz1.mongodb.net:27017,cluster0-shard-00-01.bxkz1.mongodb.net:27017,cluster0-shard-00-02.bxkz1.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-qn0lud-shard-0&authSource=admin&retryWrites=true&w=majority'

def get_collection():
    """
    コレクションオブジェクトを取得する
    """
    client = MongoClient(CONNECTION_URL)
    db = client.private_db
    collection = db.coin_saving_log
    return collection

def get_coinlog_main(target_date: date = None):
    """
    500円玉貯金ログ情報を取得する(主処理)
    """
    # コレクションオブジェクトを取得
    collection = get_collection()

    # 日付指定なしの場合は全件検索
    if (target_date is None):
        result = collection.find(sort=[('COING_SAVING_ID', 1)])
    # 日付指定ありの場合は検索条件に日付を追加
    else:
        result = collection.find_one(filter={'SAVING_DATE': str(target_date)})

    # 検索を実行して返却
    return result

@app.get("/")
def index():
    """
    デフォルト
    /
    """
    return {
        'title' : '池田さんの500円玉貯金ログ',
        'description' : 'クソAPI',
        'columns' : {
            'id' : 'レコードのID',
            'saving_date' : '貯金日付',
            'amount' : 'その日に貯金した枚数の合計',
            'total_amount' : '累計貯金枚数',
            'created_at' : 'レコードの作成日時',
            'updated_at' : 'レコードの更新日時',
            }
        }

@app.get("/datas/")
def get_all(target_date: date = None):
    """
    全件取得
    /datas/
    """
    result = get_coinlog_main(target_date)
    return dumps(result)

@app.get("/datas/{target_date}")
def get_by_date(target_date: date = None):
    """
    貯金日付による絞り込み検策
    /datas/{yyyy-mm-dd}
    """
    result = get_coinlog_main(target_date)
    return dumps(result)

@app.post("/update/{target_date}/{amount}")
async def update(target_date: date = None, amount: int = 0):
    """
    500円玉貯金ログ情報を更新する
    /update/{target_date}/{amount}
    """
    # パラメータチェック
    if(target_date is None) or (amount == 0):
        return {'parameter error'}
    
    # コレクションオブジェクトを取得
    collection = get_collection()

    # 更新条件
    filter = {'SAVING_DATE': str(target_date)}

    # 更新値
    update_value = {
            '$inc':{
                'AMOUNT': amount,
                'TOTAL_AMOUNT': amount
                },
            '$set':{'UPDATED_AT': datetime.now()}
        }

    # 更新実行
    collection.update_one(filter, update_value, upsert=False)

    # 実行結果を取得
    updated_data = dumps(get_coinlog_main(target_date))

    # 返却値を作成
    result = {
        'input_date' : target_date,   # 更新されたレコードの貯金日付
        'input_amount' : amount,      # 加算された枚数
        'updated_data' : updated_data # 更新後のレコード
    }

    # 更新されたレコードを返却
    return result

