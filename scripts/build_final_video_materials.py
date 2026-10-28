"""Validate a 300-second edit and generate narration, subtitles and optional silent preview.

The preview has burned-in English captions and no narration audio. It is a review
artifact; record the supplied English script before final submission.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess
import textwrap

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'docs/final_video'


def timestamp(seconds, srt=False):
    ms = round(seconds*1000)
    hours, ms = divmod(ms, 3600000); minutes, ms = divmod(ms, 60000)
    sec, ms = divmod(ms, 1000)
    return f'{hours:02}:{minutes:02}:{sec:02}{"," if srt else "."}{ms:03}'


def prepare():
    data = json.loads((SOURCE/'storyboard.json').read_text(encoding='utf-8'))
    clips = {f'deliverables/editing_materials/{c["file"]}': c
             for c in json.loads((ROOT/'deliverables/editing_materials/CLIP_INDEX.json').read_text(encoding='utf-8'))['clips']}
    for label in ['chapters','shots']:
        end = 0
        for item in data[label]:
            if item['start'] != end or item['end'] <= item['start']:
                raise ValueError(f'Timeline gap/overlap in {label}: {item}')
            end = item['end']
        if end != data['duration_s'] or end != 300:
            raise ValueError('The edit must cover exactly 300 seconds')
    shot_rows = []
    for i, shot in enumerate(data['shots']):
        freeze = 0
        if shot['kind'] == 'video':
            clip = clips[shot['source']]
            if not 0 <= shot['in'] < shot['out'] <= clip['duration_s']+.001:
                raise ValueError(f'Out-of-range source trim: {shot}')
            if hashlib.sha256((ROOT/shot['source']).read_bytes()).hexdigest() != clip['sha256']:
                raise ValueError(f'Changed source clip: {shot["source"]}')
            freeze = (shot['end']-shot['start'])-(shot['out']-shot['in'])/shot['speed']
            if freeze < -.001 or freeze > 1.1:
                raise ValueError(f'Unexpected freeze/truncation: {shot}')
        elif shot['kind'] == 'image' and not (ROOT/shot['source']).is_file():
            raise FileNotFoundError(shot['source'])
        shot_rows.append({'shot':i+1, 'timeline_in':timestamp(shot['start']), 'timeline_out':timestamp(shot['end']),
                          'type':shot['kind'], 'source':shot['source'], 'source_in_s':shot.get('in',''),
                          'source_out_s':shot.get('out',''), 'playback_rate':shot.get('speed',1),
                          'freeze_tail_s':round(max(0,freeze),3)})
    with (SOURCE/'shot_list.csv').open('w',newline='',encoding='utf-8-sig') as stream:
        writer = csv.DictWriter(stream,fieldnames=list(shot_rows[0])); writer.writeheader(); writer.writerows(shot_rows)
    cues = data.get('cues')
    if not cues:
        raise ValueError('Explicit picture-aligned cues are required; word-count timing is not accepted')
    previous = 0
    for cue in cues:
        if abs(cue['start']-previous) > .001 or cue['end']-cue['start'] < 2.5:
            raise ValueError(f'Caption gap, overlap or unreadably short cue: {cue}')
        lines = textwrap.wrap(cue['text'], width=72, break_long_words=False, break_on_hyphens=False)
        if len(lines) > 2:
            raise ValueError(f'Caption exceeds two lines: {cue["text"]}')
        previous = cue['end']
    if previous != 300:
        raise ValueError('Picture-aligned captions must cover the complete 300 seconds')
    narration = ['# Five-minute English narration — picture-aligned revision', '',
                 'Read each timed cue within its allotted interval. Times were assigned to the reviewed pictures, not estimated from chapter word counts.', '',
                 'The generated preview is silent. Record this narration separately.', '']
    subtitles = []; number = 1; words_total = 0; timing_rows = []
    for chapter in data['chapters']:
        chapter_cues = [c for c in cues if chapter['start'] <= c['start'] < chapter['end']]
        if not chapter_cues or chapter_cues[-1]['end'] != chapter['end']:
            raise ValueError('Caption boundaries must agree with chapter boundaries')
        chapter['narration'] = ' '.join(c['text'] for c in chapter_cues)
        words = chapter['narration'].split(); words_total += len(words)
        wpm = len(words)*60/(chapter['end']-chapter['start'])
        narration.extend([f'## {timestamp(chapter["start"])[:8]}–{timestamp(chapter["end"])[:8]} | {chapter["title"]}', '',
                          chapter['narration'], '', f'*{len(words)} words; target {wpm:.0f} words/minute.*', '',
                          '| Time | Read this cue |', '|---|---|'])
        timing_rows.append({'start_s':chapter['start'],'end_s':chapter['end'],'words':len(words),'target_wpm':round(wpm,1)})
        for cue in chapter_cues:
            lines = textwrap.wrap(cue['text'],width=72,break_long_words=False,break_on_hyphens=False)
            subtitles.extend([str(number),f'{timestamp(cue["start"],True)} --> {timestamp(cue["end"],True)}','\n'.join(lines),''])
            begin_label=timestamp(cue['start']).rstrip('0').rstrip('.')
            end_label=timestamp(cue['end']).rstrip('0').rstrip('.')
            narration.append(f'| {begin_label}–{end_label} | {cue["text"]} |')
            number += 1
        narration.append('')
    narration.extend([f'**Total: {words_total} words in 300 seconds ({words_total/5:.1f} words/minute).**',''])
    if not 600 <= words_total <= 720:
        raise ValueError(f'Narration is outside the intended five-minute range: {words_total} words')
    (SOURCE/'NARRATION_EN.md').write_text('\n'.join(narration),encoding='utf-8')
    (SOURCE/'narration.srt').write_text('\n'.join(subtitles),encoding='utf-8')
    (SOURCE/'timing_check.json').write_text(json.dumps({'duration_s':300,'words':words_total,
        'overall_wpm':words_total/5,'captions':number-1,'shots':len(shot_rows),'chapters':timing_rows,
        'timing_method':'explicit_picture_aligned_cues','minimum_cue_s':min(c['end']-c['start'] for c in cues),
        'maximum_caption_lines':2},indent=2)+'\n')
    print(f'Validated 300 seconds, {len(shot_rows)} shots, {words_total} narration words, {number-1} captions')
    return data


def render(data, output):
    from PIL import Image, ImageDraw, ImageFont
    import imageio_ffmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    temporary = ROOT/'outputs/final_video/qa'; temporary.mkdir(parents=True,exist_ok=True)
    fonts = Path('C:/Windows/Fonts')
    def font(size,bold=False):
        return ImageFont.truetype(str(fonts/('arialbd.ttf' if bold else 'arial.ttf')),size)
    def wrapped(draw,xy,text,size=24,width=38,color='#e2eaf0',bold=False,spacing=8):
        x,y=xy
        for line in textwrap.wrap(text,width=width):
            draw.text((x,y),line,font=font(size,bold),fill=color); y+=size+spacing
        return y
    cards = {
        'title':('Beyond a successful grasp', ['A complete physical pipeline', 'Three bottlenecks:', '1. Blocked approaches', '2. Corrupted geometry', '3. Contact retention']),
        'gates':('Complete-task verification', ['Lift >80 mm; hold 1 second', 'Bilateral contact >=95%', 'Placement error <55 mm', 'Physical release + table support', 'Actuator force <=40 N']),
        'recovery':('One scene, two physical attempts', ['Attempt 1: controlled closure fault', 'Missing contacts -> GRASP_FAIL', 'Open -> checked retreat -> observe', 'Attempt 2: physical grasp and release', 'First: 0/6 | Final with retry: 6/6']),
        'sensor_limits':('Remaining failure: contact stability', ['Formal sensing results: 6/12, 1/12, 9/12', 'Three robust-method failures were wedges', 'These are separate from the successful clip', 'Geometry and contact errors are not isolated']),
        'closing':('Find the limiting stage', ['Geometry: bounded local alternatives', 'Sensing: consistent cross-packet support', 'Contact: retention / deformation tradeoff', 'Next: wedge stability, nonideal sensing', 'Runnable source + report + frozen evidence'])}
    rendered=[]
    for index,shot in enumerate(data['shots']):
        chapter=next(c for c in data['chapters'] if c['start']<=shot['start']<c['end'])
        duration=shot['end']-shot['start']
        overlay=Image.new('RGBA',(1280,720),(13,30,44,255)); draw=ImageDraw.Draw(overlay)
        draw.rectangle((0,0,1280,70),fill='#163746')
        draw.text((28,20),chapter['title'],font=font(28,True),fill='white')
        draw.text((1015,26),'EE5110 / Segment C',font=font(18),fill='#b7d5dc')
        draw.rounded_rectangle((920,91,1250,605),radius=12,fill='#183345')
        y=wrapped(draw,(940,112),'KEY POINTS',size=19,width=25,color='#62d4d0',bold=True)
        for point in chapter['points']:
            y=wrapped(draw,(940,y+18),point,size=22,width=24)
        provenance='Illustrative development footage | Excluded from formal evaluation denominators'
        if shot['start']>=245 and shot['start']<280:
            provenance='Frozen paired evaluation | 180 candidate episodes; 126 exploratory episodes (separate studies)'
        elif shot['source'].endswith('soft_trace.png'):
            provenance='Illustrative development trace | Not an experimental group average'
        elif shot['source'].endswith('corrupted_points.png'):
            provenance='Illustrative development observations | No target instance labels'
        elif shot['source']=='sensor_limits':
            provenance='Frozen sensing study | Residual wedge failures are different trials from the successful illustration'
        elif shot['start']==238:
            provenance='Single-view clutter illustration | Active-view placement failures belong to separate formal trials'
        draw.text((28,72),provenance,font=font(14),fill='#a9c5ce')
        speed=shot.get('speed',1)
        if shot['kind']=='video':
            draw.rectangle((28,87,892,603),fill=(0,0,0,0))
            freeze=duration-(shot['out']-shot['in'])/speed
            draw.text((940,565),f'{speed}x simulation playback',font=font(17,True),fill='#62d4d0')
        elif shot['kind']=='image':
            draw.rectangle((28,87,892,603),fill=(0,0,0,0));freeze=0
        else:
            freeze=0; title,items=cards[shot['source']]
            y=wrapped(draw,(55,120),title,size=35,width=36,color='white',bold=True)
            for item in items:
                y=wrapped(draw,(60,y+22),item,size=25,width=52)
        overlay_path=temporary/f'overlay_{index:02}.png';overlay.save(overlay_path)
        raw_segment=temporary/f'raw_{index:02}.mp4'
        segment=temporary/f'shot_{index:02}.mp4'
        if shot['kind']=='video':
            command=[ffmpeg,'-y','-v','error','-ss',str(shot['in']),'-i',str(ROOT/shot['source']),
                     '-loop','1','-i',str(overlay_path)]
            vf=f'[0:v]trim=duration={shot["out"]-shot["in"]},setpts=(PTS-STARTPTS)/{speed},scale=864:516:force_original_aspect_ratio=decrease,pad=1280:720:28+(864-iw)/2:87+(516-ih)/2:color=0x0d1e2c[base];[base][1:v]overlay=0:0:shortest=1,tpad=stop_mode=clone:stop_duration=2,fps=25'
            if freeze>.001:
                threshold=duration-freeze
                vf+=f",drawtext=text='freeze frame':fontfile='C\\:/Windows/Fonts/arial.ttf':fontcolor=white:fontsize=17:x=940:y=586:enable='gte(t,{threshold})'"
        elif shot['kind']=='image':
            command=[ffmpeg,'-y','-v','error','-loop','1','-i',str(ROOT/shot['source']),'-loop','1','-i',str(overlay_path)]
            vf='[0:v]scale=864:516:force_original_aspect_ratio=decrease,pad=1280:720:28+(864-iw)/2:87+(516-ih)/2:color=0x0d1e2c[base];[base][1:v]overlay=0:0:shortest=1'
        else:
            command=[ffmpeg,'-y','-v','error','-loop','1','-i',str(overlay_path)];vf='format=yuv420p'
        command+=['-filter_complex',vf,'-t',str(duration),'-frames:v',str(duration*25),'-r','25','-an','-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-threads','4',str(raw_segment)]
        subprocess.run(command,check=True)
        # Normalize in a single-input pass. Framesync with a looping PNG can
        # otherwise stop before tpad's EOF frames on some FFmpeg builds.
        normalize='tpad=stop_mode=clone:stop_duration=2,fps=25'
        if freeze>.001:
            normalize+=f",drawtext=text='freeze frame':fontfile='C\\:/Windows/Fonts/arial.ttf':fontcolor=white:fontsize=17:x=940:y=586:enable='gte(t,{duration-freeze})'"
        for event in data.get('annotations',[]):
            if shot['start']<=event['start']<shot['end']:
                if event['end']>shot['end']:
                    raise ValueError('Action annotation crosses a shot boundary')
                if not re.fullmatch(r'[A-Za-z0-9 /+()\-]+',event['label']):
                    raise ValueError('Unsupported action-label character')
                lo,hi=event['start']-shot['start'],event['end']-shot['start']
                normalize+=f",drawtext=text='{event['label']}':fontfile='C\\:/Windows/Fonts/arial.ttf':fontcolor=white:fontsize=16:x=30:y=600:box=1:boxcolor=0x163746@0.95:boxborderw=3:enable='gte(t,{lo})*lt(t,{hi})'"
        subprocess.run([ffmpeg,'-y','-v','error','-i',str(raw_segment),'-vf',normalize,
                        '-t',str(duration),'-frames:v',str(duration*25),'-an','-c:v','libx264',
                        '-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-threads','4',str(segment)],check=True)
        rendered.append(segment); print(f'Rendered shot {index+1}/{len(data["shots"])}',flush=True)
    concat=temporary/'concat.txt'
    concat.write_text('\n'.join("file '"+p.as_posix()+"'" for p in rendered)+'\n',encoding='utf-8')
    joined=temporary/'joined.mp4'
    subprocess.run([ffmpeg,'-y','-v','error','-f','concat','-safe','0','-i',str(concat),'-c','copy',str(joined)],check=True)
    output=output.resolve();output.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run([ffmpeg,'-y','-v','error','-i',str(joined),'-vf',
        "subtitles=docs/final_video/narration.srt:force_style='FontName=Arial,FontSize=15,MarginV=12,Outline=1,Alignment=2'",
        '-t','300','-an','-c:v','libx264','-preset','veryfast','-crf','22','-threads','4','-pix_fmt','yuv420p','-movflags','+faststart',str(output)],cwd=ROOT,check=True)
    metadata=subprocess.run([ffmpeg,'-hide_banner','-i',str(output)],capture_output=True,text=True).stderr
    duration_match=re.search(r'Duration: (\d+):(\d+):([\d.]+)',metadata)
    if not duration_match:
        raise ValueError('Unable to read preview duration')
    hours,minutes,seconds=map(float,duration_match.groups())
    if abs(hours*3600+minutes*60+seconds-300)>.04:
        raise ValueError('Rendered preview does not match the 300-second edit')
    if 'Audio:' in metadata:
        raise ValueError('Preview was expected to be silent')
    print(f'Verified 300-second silent captioned preview (record narration separately): {output}')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--render-preview',action='store_true')
    parser.add_argument('--output',type=Path,default=ROOT/'deliverables/EE5110_5min_reviewed_preview.mp4')
    args=parser.parse_args();data=prepare()
    if args.render_preview:render(data,args.output)
