# burst\_detect\_all.py
    arg: hoge.dump
    1日ごとのバースト検知結果を表示
    イベントごとのdumpを受付   

# pybursts.py
    module
    python 3.5では動いていたが、3.6.1で動かなくなったので修正したもの

# fullevent2event.py
    arg: hoge,dump
    fulleventをイベント別に分割

# host\_plot\_day.py
    arg: hoge_df.dump 20120101 prefix
    host別集計データフレームhoge_df.dumpの指定日の上位10件の累積和をプロット
    prefix/*-*/"イベント別dump"

# burst\_pandas.py
    arg: [dir-prefix]
    dir-prefix/*-*/*.txtにあるバースト結果を引数に、全バーストデータをdf化してdump
    burst_df = pd.DataFrame(index=pd.date_range(20120101-20130331),column=filenum)

# heat\_map.py
    arg: hoge.dump fuga.dump ...
    引数で受けたdumpの通年のヒートマップをプロット

# plot.py
    arg: hoge.dump
    dumpの通年の発生件数を日単位で集計してプロット

# plot\_day.py
    arg: hoge.dump 20120101
    hoge.dumpの指定日の累積和をプロット

# search\_burst.py
    arg: burst_df
    burstを集計したDataFrameを受けて、前後1min以内に発生しているバーストを集計

# event\_agg.py
    arg: [dir-prefix]
    dir-prefix/*-*/以下にあるファイルをホスト別に合算してdump

# host\_pandas.py
    arg: [dir-prefix]
    hostごとにテンプレートID別集計DataFrame生成

# show\_start\_end\_date.py
    arg: hoge.dump
    dumpの始点と終点を返す
