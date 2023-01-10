# DaVinciResolveCreateVoicevoxSubtitle
DaVinci ResolveでVOICEVOXのwavファイルを配置したオーディオトラックから字幕を作成します。

## 必要なもの
python3系がインストールされている必要があります  

## とりあえずの使い方
まずDaVinci Resolveでスクリプトを使えるようにします。  
DaVinci Resolveで対象となるプロジェクトを開きます。  
プロジェクトにはVOICEVOXの音声データが配置されたオーディオトラックが必要です（この「とりあえずの使い方」ではオーディオトラック2である必要があります）。  
DaVinci Resolveを開きメニューの [DaVinci Resolve] - [環境設定...] - [システム] - [一般] - [一般環境設定] の「外部スクリプトに使用」で「ローカル」を選択して保存します。  
この操作でDaVinci Resolve側ではスクリプトが使えるようになりました。  
DaVinci Resolveはこのまま閉じないでおいて下さい。  

VOICEVOXで「テキストを繋げて書き出し」を行い、どこかにテキストを保存します。  
このテキストファイルはスクリプトで使用します。  

次にスクリプトを実行します。  
コマンドプロンプトを開き、CreateSubtitle.batがあるフォルダに移動します。  
```
cd /d C:\～～～～～～～（CreateSubtitle.batがあるフォルダ）
```
実行します。  
```
CreateSubtitle.bat C:\～～～～～～～（VOICEVOXのテキストファイル）
```
上手くいっていればVOICEVOXのテキストファイルと同じフォルダに字幕.srt（字幕ファイル）とSubtitle.fcpxml（字幕用タイムライン）が保存されます。  

.srtはDaVinci Resolveでメディアとして扱えます  

.fcpxmlはDaVinci Resolveで[ファイル] - [読み込み] - [タイムライン...]から読み込みできます  
字幕用のテキストクリップが配置されたタイムラインとなっているので、テキストクリップを全選択してからコピー&ペーストして使うことをお勧めします  
またテキストクリップの設定をまとめて変える際は、テキストクリップを全選択して変更すると便利です  

## ライセンス表記について
スクリプトから作成した字幕を使用する際には何も表記する必要はありませんが、作者Twitterをフォローしてもらえると喜びます。  
https://twitter.com/yamayamadagames  
https://twitter.com/yamayamada0_0  

スクリプト自体を再頒布する際はMITライセンスに基づいて下さい。  

## ファイル
| ファイル名 | 説明 |
| --- | --- |
| CreateSubtitle.py | スクリプト本体です |
| CreateSubtitle.bat | Windowsで簡単にスクリプトを使うためのbatです、使わなくても大丈夫です |

## 詳細な使い方
設定ファイル `settings.py` を編集することで色々と設定の変更が可能です  

| 設定名 | 説明 |
| --- | --- |
| invalid_title | オーディオトラックのクリップに対してどの文字か判別できなかった際に使用される文字列 |
| audio_track_number | オーディオトラックの番号指定<br>一番上のオーディオトラックが1<br>VOICEVOXから書き出される.wavファイルの名前を変更することなく、このオーディオトラックに配置している必要があります |
| audio_track_continuous_time | この秒数しか.wav同士に隙間がない場合、隙間も字幕を表示する |
| frame_rate | Timelineのフレームレート(30以外未テスト) |
| srt_output | .srt形式の字幕ファイルを出力するか |
| srt_filename | 字幕ファイル名 |
| xml_output | .fcpxml形式の字幕ファイルを出力するか |
| xml_filename | XMLの字幕ファイル名 |
| xml_font | XMLの字幕のフォント |
| xml_bold | XMLの字幕のを太字にするか(読み込み時に無視されているかも) |
| xml_size | XMLの字幕のサイズ、`"67"` のように文字列で数値を渡す
| xml_video_format | XMLの字幕のタイムラインのフォーマット
| xml_video_width | XMLの字幕のタイムラインのサイズ幅
| xml_video_height | XMLの字幕のタイムラインのサイズ高さ
| text_plus_output | Text+の字幕を作成するか(**非推奨**) |
| text_plus_font | Text+字幕のフォント |
| text_plus_style | Text+字幕のスタイル |
| text_plus_size | Text+字幕のサイズ、こちらは数値で渡す |
| text_plus_center | Text+字幕の位置 |

フックファイル `hooks.py` を編集することで、VOICEVOXのテキストそのままではなく、編集したテキストを字幕にすることができます

| 関数名 | 説明 |
| --- | --- |
| AdjustSubitleText( original_text ) | この関数の内容を変更すると.srt形式の字幕の内容を修正できます |
| AdjustTitleText( original_text ) | この関数の内容を変更すると.fcpxml形式の字幕とText+の字幕の内容を修正できます。<br>最初から「。を除去」「、をスペースに変更」「先頭＆末尾のスペースを除去」が入っています |

## Text+字幕について
DaVinci Resolveのスクリプトの制約で
* クリップの長さは5秒固定  
* 選択しているトラックに配置

となっています。  
そのためかなり品質が低い字幕になるのでご注意下さい。  
特に字幕の間隔が5秒未満になると、手前の置いた字幕が分割されて本来の位置と離れた位置に字幕が置かれます。  
