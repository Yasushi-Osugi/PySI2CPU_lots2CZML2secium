# PySI2CPU_lots2CZML2secium
Visualising Supply Chain activities on earth(secium) with translating Supply Chain Planned lots to CZML for secium. PySI is Global weekly PSI planner, that has a trial function decoupling point and its buffer inventory analysis.

本ソースコードは、サプライチェーン計画Global Weekly PSI plannering and Simulationのアウトプットを地球儀(secium)の上に可視化するトライアルです。
サプライチェーン計画Global weekly PSI Planは、ISO標準の週を単位として、製品ロット単位の生産、出荷、搬送、着荷、在庫、販売というビジネス活動をグローバルレベルで計画します。
共通計画単位CPU:Commomn Planning Unitと呼ぶ、製品ロット単位の計画データを元に、地球儀(secium)の上に、1製品ロット=1立方体という対応で、サプライチェーンのモノの動きを可視化します。
本ソースコードに関連するSNSの記事は、「グローバル・サプライチェーンの動きを地球儀(secium)の上に可視化する」
no+eの下記URL
https://note.com/osuosu1123/n/nfa1df807853b
または、
はてなブログの下記URL
https://osuosu1123.hatenablog.com/entry/2024/02/02/114159?_gl=1*ogk58s*_gcl_au*NzA3NDY0NTIxLjE3MDY4NDEwMzQ.
を参照ください。
いずれのURLも同じ内容の記事です。

【処理手順】
1. PySI_make_CPU_lots_by_decoupling_pattern.pyを実行する共通ロット単位の製品ロットの計画データを出力する。
   入力データ
   - supply_chain_tree_outbound_attributes_JPN.csv アウトバウド(完成品の市場流通サイド)サプライチェーンの定義ファイル
   - supply_chain_tree_inbound_attributes_JPN      インバウンド(素部材の完成供給サイド)サプライチェーンの定義ファイル
   - S_month_data_prev_year_JPN                    最終需要地における月次需要計画　※中長期の経営計画などから定義
   - node_position                                 サプライチェーンの各事業拠点の座標データ

   Global Weekly PSI Planning処理
   - 初期処理
   - インバウンドとアウトバウンドのサプライチェーンのtree構造の読込み
   - 最終需要地における月次需要計画からISO週単位の週次計画を生成する LOT_ID = LEAF_NODE_NAME + YYYYWW 
  
   - PSI計画処理 ( DP: Decoupling Point )
   - Backward Planning 最終需要地の需要データを起点に需要データ(LOT_ID単位)を各拠点にbackward planningで配置する
   - Demand Prioriting on Production Capacity and PreProduction timeshift 完成出荷の優先度計算　※生産キャパと先行生産タイムシフト
   - Finding Decouple Point nodes 需要変動を吸収するDPデカップリング・ポイントの在庫拠点のすべての候補を洗い出し
   - Forward/PUSH Planning 完成出荷拠点からDPへ、優先度を見ながら供給データ(LOT_ID単位)を各拠点にforward planningでPUSH配置する
   - Backward/PULL planning DPから先の拠点nodeでは、初期セットの需要発生位置を起点に、需要データ(LOT_ID単位)をbackward planでPULL配置する
  
   - 出力処理
   - 処理処理で生成されたISO週単位の需要データ    S_iso_week_data.csv
   - サプライチェーン計画の共通ロット単位データ    CPU_OUT_FW_plan010.csv 
   - デカップリング在庫の配置パターン毎の共通ロット単位データ    CPU_OUT_FW_planXX.csv ※XXはデカップリング在庫の配置パターン番号
   
2. PSIの共通ロット単位データ(CPU_OUT_FW_plan010.csv)から地球儀(secium)描画用のCZMLファイルへの変換処理
   - 入力ファイル　PSIの共通ロット単位データ(CPU_OUT_FW_plan010.csv)
   - 変換処理CPU_CZML_translator010.pyにより、CPU:Common Planning Unit)単位のLOTデータを立方体のBOX定義のCZMLファイルに変換
   - 出力ファイル　変換されたCZMLファイル　CPU2CZML010.csv
     
3. 地球儀(secium)を起動するHTMLファイルglobal_PSI_monitor_frame.htmlを作る。
   - seciumのホームページから"MyToken"を取得する。
   - CZMLファイル(CPU2CZML010.csv)をglobal_PSI_monitor_frame.htmlの//STARTと//ENDの間にコピペする。
     
   - 本来は、CZMLファイルをloadする関数があるので、このような原始的なコピペ作業は不要のハズですが、
   　私の開発環境がwindows localのためか、HTMLファイルからのCZMLファイルのloadが(URL指定でないので)うまく動かなかったので、コピペしています。
   
5. CZMLを組み込んだHTML(global_PSI_monitor_frame.html)を起動する。地球儀(secium)が立ち上がるまで、数十秒待つ。
   seciumタイマーのスタート・ボタンで、アニメーション開始
   - シミュレーションの時間単位　1週間 = 1秒
   - 1製品ロット = 1立方体

以上です。
