# Tiger

# OverView
公開求人マッチングプロジェクト

#
## 導入手順
### 環境
#### 更新日 2022/01/13
```
Python 3.9.1
Django 4.0.1
git    2.31.1.windows.1
```

### プロジェクトを配置したい階層に移動し、以下のコマンドを実行
```
 git clone https://github.com/mynavi/sys-order-matching.git
```

### こんな感じになれば成功
```
s12100400@ws41363 MINGW64 /c/Users/s12100400/cloneTest
$ git clone https://github.com/mynavi/sys-order-matching.git
Cloning into 'sys-order-matching'...
remote: Enumerating objects: 18, done.
remote: Counting objects: 100% (18/18), done.
remote: Compressing objects: 100% (13/13), done.
remote: Total 18 (delta 3), reused 18 (delta 3), pack-reused 0
Receiving objects: 100% (18/18), 5.75 KiB | 2.87 MiB/s, done.
Resolving deltas: 100% (3/3), done.

s12100400@ws41363 MINGW64 /c/Users/s12100400/cloneTest
```

### cloneしたリポジトリ配下に移動
```
cd sys-order-matching/
```
現在インストール済みのライブラリを確認
```
pip freeze
```

### ライブラリの一括インストール
```
pip install -r requirements.txt --proxy=http://proxy.int.mynavi.jp:8080
```

### インストール後のライブラリを確認
```
pip freeze
```
Djangoの開発用サーバの起動
```
python manage.py runserver
```
下記のURLにアクセス
```
http://127.0.0.1:8000/
```
終了は以下のコマンド
```
Ctrl + c
```


### 既存のDBからmodelを作る方法
①：setting.py に以下を追加、必要があればカンマ区切りでスキーマ名追加
```
'OPTIONS': {
            'options': '-c search_path=public,doc,cp2,pjm'
        }
```

②：APPターミナルで以下コマンドを叩く。
```
python manage.py inspectdb < テーブル名 >
```

③：出力されたmodelをすべてコピーしてmodel.pyに貼り付け