from fastapi import FastAPI
from pymongo import MongoClient
from bson.json_util import dumps
from datetime import date, datetime

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
    # コレクションオブジェクトを取得
    collection = get_collection()

    # 全件検索を実行
    result = collection.find(sort=[('COING_SAVING_ID', 1)])

    # 結果を返却
    return dumps(result)


@app.get("/datas/{target_date}")
def get_by_date(target_date: date = None):
    """
    貯金日付による絞り込み検策
    /datas/{yyyy-mm-dd}
    """
    # コレクションオブジェクトを取得
    collection = get_collection()

    # 日付による絞り込み検索を実行
    result = collection.find_one(filter={'SAVING_DATE': str(target_date)})

    # 結果を返却
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
                'AMOUNT': amount, # 貯金枚数 +1
                'TOTAL_AMOUNT': amount # 累計貯金枚数 +1
                },
            '$set':{'UPDATED_AT': datetime.now()} # 更新日付
        }

    # 更新実行
    collection.update_one(filter, update_value, upsert=False)

    # 更新後のデータを取得
    updated_data = collection.find_one(filter={'SAVING_DATE': str(target_date)})

    # 返却値を作成
    result = {
        'input_date' : target_date,   # 更新されたレコードの貯金日付
        'input_amount' : amount,      # 加算された枚数
        'updated_data' : updated_data # 更新後のレコード
    }

    # 更新されたレコードを返却
    return result

