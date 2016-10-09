# execjson
Service Request should be written in JSON

[Getting Started]
http://d.hatena.ne.jp/aaabbb_200904/20150430/1430398428

[Install]
事前にdjango インストールが必要
※ centos7, django1.6(EPEL)で動作確認済み。

1. /var/tmp 以下に展開
2. $ cd /var/tmp/execjson/web/mysite
3. $./manage.py syncdb  (セッションDBを作成)
4. $./manage.py runserver (HTTPサーバー起動)
5. $ cd /var/tmp/execjson/web/mysite/batch/ && ./do.sh  (ジョブ実行が開始される, fabricが必要)
