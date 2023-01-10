# 設定ファイル

#基本的な設定
invalid_title = "@@@@@@" # 字幕の文字が分からなかった場合に表示される文字
#video_track_number = 10 # 未使用
audio_track_number = 2 # VOICEVOXの.wavのオーディオトラック
audio_track_continuous_time = 2 # この秒数しか.wavに隙間がない場合、隙間も字幕を表示する
frame_rate = 30 # Timelineのフレームレート

# .srt字幕に関する設定
srt_output = True # 字幕ファイルを出力するか
srt_filename = "字幕.srt" # 字幕ファイル名

# .fcpxml字幕に関する設定
xml_output = True # XMLの字幕ファイルを出力するか
xml_filename = "Subtitle.fcpxml" # XMLの字幕ファイル名
xml_font = "Open Sans"  # XMLの字幕のフォント
xml_bold = "1" # XMLの字幕のを太字にするか
xml_size = "67" # XMLの字幕のサイズ
xml_video_format = "FFVideoFormat1080p30" # XMLの字幕のタイムラインのフォーマット
xml_video_width = "1920" # XMLの字幕のタイムラインのサイズ幅
xml_video_height = "1080" # XMLの字幕のタイムラインのサイズ高さ

# Text+字幕に関する設定
text_plus_output = False # Text+の字幕を作成するか
text_plus_font = "Open Sans" # Text+字幕のフォント
text_plus_style = "Bold" # Text+字幕のスタイル
text_plus_size = 0.0641 # Text+字幕のサイズ
text_plus_center = [0.5, 0.0715] # Text+字幕の位置

