# 関数のhook
# このファイルを変えることで、VOICEVOXのテキストから字幕にする際に調整が可能

# srtファイルに出力するテキスト内容の調整
# original_text VOICEVOXで出力されたテキスト
# 戻り値 srt に出力するテキスト
def AdjustSubitleText( original_text ):
    return original_text

# xmlファイルとText+に出力するテキスト内容の調整
# original_text VOICEVOXで出力されたテキスト
# 戻り値 xmlファイルとText+に出力するテキスト
def AdjustTitleText( original_text ):
    return original_text

# 「、」を「 」に変換、「。」を除去、先頭＆末尾のスペースを除去する例
#def AdjustTitleText( original_text ):
#    return original_text.replace('、', ' ').replace('。', '').strip()

