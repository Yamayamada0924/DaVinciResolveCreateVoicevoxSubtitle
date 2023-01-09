#!/usr/bin/env python

"""
CreateSubtitle.py VOICEVOX_output.txt
"""

import sys
import csv
import time
import re
import os.path
import xml.etree.ElementTree as gfg

invalid_title = "@@@@@@" # 字幕の文字が分からなかった場合に表示される文字
#video_track_number = 10 # 未使用
audio_track_number = 2 # VOICEVOXの.wavのオーディオトラック
audio_track_continuous_time = 2 # この秒数しか.wavに隙間がない場合、隙間も字幕を表示する
frame_rate = 30 # Timelineのフレームレート

srt_output = True # 字幕ファイルを出力するか
srt_filename = "字幕.srt" # 字幕ファイル名

xml_output = True # XMLの字幕ファイルを出力するか
xml_filename = "Subtitle.fcpxml" # XMLの字幕ファイル名
xml_font = "Open Sans"  # XMLの字幕のフォント
xml_bold = "1" # XMLの字幕のを太字にするか
xml_size = "67" # XMLの字幕のサイズ
xml_video_format = "FFVideoFormat1080p30"
xml_video_width = "1920"
xml_video_height = "1080"

text_plus_output = False # Text+の字幕を作成するか
text_plus_font = "Open Sans" # Text+字幕のフォント
text_plus_style = "Bold" # Text+字幕のスタイル
text_plus_size = 0.0641 # Text+字幕のサイズ
text_plus_center = [0.5, 0.0715] # Text+字幕の位置

# srtファイルに出力するテキスト内容の調整
# original_text VOICEVOXで出力されたテキスト
# 戻り値 srt に出力するテキスト
def AdjustSubitleText( original_text )
    return original_text

# xmlファイルとText+に出力するテキスト内容の調整
# original_text VOICEVOXで出力されたテキスト
# 戻り値 xmlファイルとText+に出力するテキスト
def AdjustTitleText( original_text )
    return original_text.replace('、', ' ').replace('。', '').strip()



#from python_get_resolve import GetResolve
import DaVinciResolveScript

outpub_debug_log = False

args = sys.argv

notice_list = []

# VOICEVOXのテキストデータを解析した情報
class InputTextData:
    def __init__(self, index, start_text, subtitle_text, title_text):
        self.index = index
        self.start_text = start_text
        self.subtitle_text = subtitle_text
        self.title_text = title_text

#AudioTrackを解析した情報
class AudioClipData:
    def __init__(self, start_time, end_time, index, start_text):
        self.start_time = start_time
        self.end_time = end_time
        self.index = index
        self.start_text = start_text

# intのframeをTimecodeにする
def IntToTimecode( intTime ):
    hours = intTime // int(frame_rate * 60 * 60)
    minites = (intTime - int(hours * frame_rate * 60 * 60)) // int(frame_rate * 60)
    seconds = (intTime - int(hours * frame_rate * 60 * 60) - int(minites * frame_rate * 60)) // frame_rate
    frames = intTime - int(hours * frame_rate * 60 * 60) - int(minites * frame_rate * 60) - int(seconds * frame_rate)
    return format(hours,"02") + ':' + format(minites,"02") + ':' + format(seconds,"02") + ':' + format(frames,"02")

# intのframeをsrtのTimeにする
def IntToSrttime( intTime ):
    hours = intTime // int(30 * 60 * 60)
    minites = (intTime - int(hours * frame_rate * 60 * 60)) // int(frame_rate * 60)
    seconds = (intTime - int(hours * frame_rate * 60 * 60) - int(minites * frame_rate * 60)) // frame_rate
    frames = intTime - int(hours * frame_rate * 60 * 60) - int(minites * frame_rate * 60) - int(seconds * frame_rate)
    frame_time = 1000 * int(frames) // int(frame_rate)
    return format(hours,"02") + ':' + format(minites,"02") + ':' + format(seconds,"02") + ',' + format(frame_time,"03")

# 同じ字幕が複数あるかのチェック
def DuplicateCheck( duplicate_check, audio_clip_data, input_text_data, notice_list ):
    if input_text_data in duplicate_check:
        notice_list.append("duplicate audio clip data: " + IntToTimecode(audio_clip_data.start_time) + " " + audio_clip_data.start_text);
    else:
        duplicate_check.append(input_text_data)
    return

# intのframeをXmlのTimecodeにする
def GetXmlTimecode( intTime ):
    return str(intTime) + "/" + str(frame_rate) + "s"

# intのframeをXmlのTimecodeにする(秒単位)
def GetXmlTimecodeSec( intTime ):
    return str(intTime // frame_rate) + "/1s"


# VOICEVOXのtxtの解析
input_text_datas = []

csv_file = open(args[1], "r", encoding="utf_8", newline="")
lines = csv.reader(csv_file, delimiter=",", lineterminator="\r\n", skipinitialspace=True)

text_index = 1
for row in lines:
    input_text_datas.append( InputTextData(text_index, row[1][0:9], AdjustSubitleText(row[1]), AdjustTitleText(row[1]) ) )
    text_index += 1

csv_file.close()

if outpub_debug_log:
    for data in input_text_datas:
        print("index:", data.index, "start_text:", data.start_text, "subtitle_text:", data.subtitle_text, "title_text:", data.title_text)

#AudioTrackの解析
audio_clip_datas = []

#resolve = GetResolve()
resolve = DaVinciResolveScript.scriptapp("Resolve")
projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()
timeline = project.GetCurrentTimeline()

if not timeline:
    print("no timeline")
    quit()

trackType = "audio"
trackCount = timeline.GetTrackCount(trackType)
if audio_track_number > trackCount:
    print("no audio track number")
    quit()

audio_clips = timeline.GetItemListInTrack(trackType, audio_track_number)
for clip in audio_clips:
    clip_name = clip.GetName()
    if( re.match('^[0-9][0-9][0-9]_', clip_name) ):
        clip_name_trim = clip_name[4:]
        audio_clip_datas.append( AudioClipData(clip.GetStart(), clip.GetEnd(), int(clip_name[0:3]), clip_name_trim[clip_name_trim.find('_')+1:clip_name_trim.find('.wav')].replace('…','')) )

# 各種出力
if srt_output:
    srt_file = open(os.path.join(os.path.dirname(args[1]), srt_filename), 'w', encoding='UTF-8')
srt_index = 1

start_frame = timeline.GetStartFrame()
end_frame = timeline.GetEndFrame()
if xml_output:
    xml_root = gfg.Element("fcpxml", attrib={"version":"1.6"})
    #resource
    xml_resources = gfg.SubElement(xml_root, "resources")
    gfg.SubElement(xml_resources, "format", attrib={"width":xml_video_width, "frameDuration":GetXmlTimecode(1), "name":xml_video_format, "id":"r0", "height":xml_video_height})
    gfg.SubElement(xml_resources, "effect", attrib={"uid":".../Generators.localized/Solids.localized/Vivid.localized/Vivid.motn", "name":"Vivid", "id":"r1"})
    gfg.SubElement(xml_resources, "effect", attrib={"uid":".../Titles.localized/Bumper:Opener.localized/Basic Title.localized/Basic Title.moti", "name":"Basic Title", "id":"r2"})
    
    #library
    xml_library = gfg.SubElement(xml_root, "library")
    xml_event = gfg.SubElement(xml_library, "event")
    xml_project = gfg.SubElement(xml_event, "project", attrib={"name":"Subtitle"})
    xml_sequence = gfg.SubElement(xml_project, "sequence", attrib={"duration":GetXmlTimecode(end_frame-start_frame), "format":"r0", "tcStart":"0s"})
    xml_spine = gfg.SubElement(xml_sequence, "spine")
    xml_video = gfg.SubElement(xml_spine, "video", attrib={"start":GetXmlTimecodeSec(0), "offset":GetXmlTimecodeSec(start_frame), "ref":"r1", "name":"Solid Color", "duration":GetXmlTimecode(end_frame-start_frame), "enabled":"1"})

    xml_ts = 1

duplicate_check = []
audio_clip_count = len(audio_clip_datas)
for i, data in enumerate(audio_clip_datas):
    if outpub_debug_log:
        print("start_time:", data.start_time, "end_time:", data.end_time, "index:", data.index, "start_text:", data.start_text)
    
    timecode = IntToTimecode(data.start_time)
    if text_plus_output:
        if not timeline.SetCurrentTimecode(timecode):
            print("SetCurrentTimecode error", timecode)
            quit()
    
    # 適切な字幕の検索
    title_text = invalid_title
    subtitle_text = invalid_title
    match_text = [s for s in input_text_datas if s.start_text == data.start_text]
    if len(match_text) == 1:
        title_text = match_text[0].title_text
        subtitle_text = match_text[0].subtitle_text
        DuplicateCheck(duplicate_check, data, match_text[0], notice_list)
    else:
        match_text = [s for s in input_text_datas if s.start_text == data.start_text and s.index == data.index]
        if len(match_text) == 1:
            title_text = match_text[0].title_text
            subtitle_text = match_text[0].subtitle_text
            DuplicateCheck(duplicate_check, data, match_text[0], notice_list)
        else:
            notice_list.append("no match: " + data.start_text);
    
    end_time = data.end_time
    if i < audio_clip_count - 1 and  data.end_time + frame_rate * audio_track_continuous_time >= audio_clip_datas[i+1].start_time:
        end_time = audio_clip_datas[i+1].start_time
    
    if text_plus_output:
        titleText = timeline.InsertFusionTitleIntoTimeline("Text+")
        toolList = titleText.GetFusionCompByIndex(1).GetToolList()
        time.sleep(0.25)
        toolList[1].StyledText = title_text
        toolList[1].Font, toolList[1].Style = text_plus_font, text_plus_style
        toolList[1].Size = text_plus_size
        toolList[1].Center = text_plus_center
        time.sleep(0.25)
    
    if srt_output:
        srt_file.write(str(srt_index) + "\n")
        srt_file.write(IntToSrttime(data.start_time) + " --> " + IntToSrttime(end_time) + "\n")
        srt_file.write(subtitle_text + "\n")
        srt_file.write("\n")
        srt_index += 1

    if xml_output:
        xml_title = gfg.SubElement(xml_video, "title", attrib={"start":GetXmlTimecode(data.start_time), "offset":GetXmlTimecode(data.start_time - start_frame), "ref":"r2", "name":"Rich", "duration":GetXmlTimecode(end_time-data.start_time), "lane":"1", "enabled":"1"})
        xml_text = gfg.SubElement(xml_title, "text", attrib={"roll-up-height":"0"})
        xml_text_style0 = gfg.SubElement(xml_text, "text-style", attrib={"ref":"ts" + str(xml_ts)})
        xml_text_style0.text = title_text
        xml_text_style_def = gfg.SubElement(xml_title, "text-style-def", attrib={"id":"ts" + str(xml_ts)})
        xml_text_style1 = gfg.SubElement(xml_text_style_def, "text-style", attrib={"strokeWidth":"0", "font":xml_font, "lineSpacing":"0", "alignment":"center", "italic":"0", "fontColor":"1 1 1 1", "strokeColor":"0 0 0 1", "bold":xml_bold, "fontSize":xml_size})
        xml_ts += 1

if srt_output:
    srt_file.close()

if xml_output:
    with open (os.path.join(os.path.dirname(args[1]), xml_filename), "wb") as xml_files:
        tree = gfg.ElementTree(xml_root)
        gfg.indent(tree, '    ')
        tree.write(xml_files, encoding="utf-8", xml_declaration=True)

for notice in notice_list:
    print(notice)

