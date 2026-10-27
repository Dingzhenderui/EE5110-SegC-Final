"""Build the offline submission ZIP using an explicit allowlist."""
from pathlib import Path
import zipfile
import argparse
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]


def package_current(video, review_kit=False):
    """Package the integrated report/current GUI without altering historical ZIPs."""
    if video is None:
        raise ValueError('Version 3.1.0 requires --video PATH. Use the final recorded video, or explicitly --review-kit with the silent preview.')
    video = video.resolve()
    if not video.is_file():
        raise FileNotFoundError(video)
    if 'preview' in video.name.lower() and not review_kit:
        raise ValueError('The preview has no narration. Use --review-kit, or record narration and pass the final video.')
    report = ROOT/'output/pdf/EE5110_Final_Report.pdf'
    required = [report, ROOT/'docs/final_report/report.tex', ROOT/'docs/final_video/NARRATION_EN.md',
                ROOT/'docs/final_video/narration.srt', ROOT/'docs/final_video/shot_list.csv',
                ROOT/'assets/panda/panda.xml', ROOT/'assets/ycb/ycb/foam_brick.xml']
    for path in required:
        if not path.is_file():
            raise FileNotFoundError(path)
    sys.path.insert(0, str(ROOT/'scripts'))
    from check_completion_evidence import audit
    from check_exploration_evidence import audit as audit_explorations
    comparisons = [ROOT/f'docs/validation/{version}/comparison.json' for version in ['v2.1.0','v3.0.0']]
    originals = {path:path.read_bytes() for path in comparisons}
    try:
        audit(ROOT/'docs/validation/v2.1.0'); audit_explorations(ROOT/'docs/validation/v3.0.0')
    finally:
        # Audits recompute these files; preserve their original bytes/newlines.
        for path,data in originals.items():
            if path.read_bytes()!=data: path.write_bytes(data)
    root_names = ['main.py','challenge_main.py','sensing_main.py','clutter_main.py','exploration_main.py',
                  'demo_viewer.py','OPEN_DEMO.cmd','打开演示界面.cmd','RUN_PROJECT.ps1','README.md',
                  '开始使用.md','requirements.txt','requirements-video.txt','requirements-report.txt',
                  'CHANGELOG.md','PROGRESS.md','CONTRIBUTING.md']
    files = [ROOT/name for name in root_names]
    for directory in ['robot_manipulation','exploration','scripts','tests','assets','docs/images',
                      'docs/validation/v2.1.0','docs/validation/v3.0.0','docs/final_report','docs/final_video',
                      'deliverables/editing_materials']:
        files.extend(p for p in (ROOT/directory).rglob('*') if p.is_file()
                     and '__pycache__' not in p.parts and p.suffix not in ('.pyc','.log','.aux','.xdv','.out','.synctex'))
    files.extend([report, ROOT/'docs/ASSET_ATTRIBUTION.md', ROOT/'docs/FINAL_DELIVERY.md',
                  ROOT/'docs/DEMO_EDITING_GUIDE.md', ROOT/'docs/FILE_GUIDE.md'])
    # A project-wide inventory would be misleading in a curated submission ZIP;
    # this package gets its own exact manifest instead.
    entries = {p.relative_to(ROOT).as_posix(): p for p in sorted(set(files))}
    entries['deliverables/'+video.name] = video
    kind = 'review_kit' if review_kit else 'submission'
    target = ROOT/f'deliverables/EE5110SegC_{kind}_v3.1.0.zip'
    status = ('This is a review kit. The 300-second captioned preview has no narration audio.\n'
              'Record docs/final_video/NARRATION_EN.md before the final video submission.\n') if review_kit else 'Final video explicitly supplied by the team.\n'
    guide = ('EE5110 Segment C - Integrated project deliverables\n\n'+status+'\n'
             'Main report: output/pdf/EE5110_Final_Report.pdf (10 pages)\n'
             f'Demo video: deliverables/{video.name}\n'
             'Report source: docs/final_report/report.tex and figures/\n'
             'Video script/edit: docs/final_video/\n'
             'Run instructions: README.md and docs/FINAL_DELIVERY.md\n'
             'Windows GUI: OPEN_DEMO.cmd (install Python requirements first)\n'
             'Core: main.py, clutter_main.py, exploration_main.py\n'
             'Evidence: docs/validation/v2.1.0 and v3.0.0\n'
             'Python 3.12 and dependencies are required; .venv is not bundled.\n'
             'The SHA-256 manifest covers this curated ZIP; the full-branch inventory is intentionally omitted.\n')
    # Use the concise current handover as the curated ZIP's README, instead of
    # full-branch navigation that refers to intentionally omitted historical ZIPs.
    readme = (ROOT/'docs/FINAL_DELIVERY.md').read_bytes()
    entries.pop('README.md')
    manifest = {name: hashlib.sha256(path.read_bytes()).hexdigest() for name,path in entries.items()}
    manifest['README.md'] = hashlib.sha256(readme).hexdigest()
    manifest['START_HERE.txt'] = hashlib.sha256(guide.encode('utf-8')).hexdigest()
    target.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
        for name,path in entries.items(): archive.write(path,name)
        archive.writestr('README.md',readme)
        archive.writestr('START_HERE.txt',guide)
        archive.writestr('SUBMISSION_MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None: raise ValueError('CRC verification failed')
        if set(archive.namelist()) != set(manifest)|{'SUBMISSION_MANIFEST.json'}:
            raise ValueError('Manifest membership differs from archive')
        for name,expected in manifest.items():
            if hashlib.sha256(archive.read(name)).hexdigest()!=expected:
                raise ValueError('Hash mismatch: '+name)
    print(f'{target}: {len(manifest)} verified entries; {target.stat().st_size/1e6:.1f} MB')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', choices=['1.0.0', '1.1.0', '1.2.0', '1.3.0', '1.4.0', '2.0.0', '2.1.0', '3.0.0', '3.1.0'], default='3.0.0')
    parser.add_argument('--video', type=Path, help='Explicit final video for version 3.1.0')
    parser.add_argument('--review-kit', action='store_true', help='Explicitly package an unvoiced review preview')
    args = parser.parse_args(); version = args.version
    if version == '3.1.0':
        package_current(args.video, args.review_kit)
        return
    if args.video or args.review_kit:
        parser.error('--video and --review-kit apply only to version 3.1.0')
    final_submission = version in ('2.1.0', '3.0.0')
    target = ROOT / f'deliverables/EE5110SegC_{"submission" if final_submission else "baseline"}_v{version}.zip'
    report, video = {
        '1.0.0': ('baseline_report.pdf', 'baseline_demo.mp4'),
        '1.1.0': ('reliability_report_v1.1.0.pdf', 'reliability_demo_v1.1.0.mp4'),
        '1.2.0': ('obstacle_report_v1.2.0.pdf', 'obstacle_demo_v1.2.0.mp4'),
        '1.3.0': ('obstacle_reliability_v1.3.0.pdf', 'obstacle_demo_v1.3.0.mp4'),
        '1.4.0': ('transparent_sensing_v1.4.0.pdf', 'transparent_sensing_v1.4.0.mp4'),
        '2.0.0': ('clutter_v2.0.0.pdf', 'clutter_v2.0.0.mp4'),
        '2.1.0': ('final_report_v2.1.0.pdf', 'demo_v2.1.0.mp4'),
        '3.0.0': ('exploration_report_v3.0.0.pdf', 'explorations_v3.0.0.mp4'),
    }[version]
    report_path = ROOT / ('output/pdf' if final_submission else 'docs/report') / report
    required = [report_path, ROOT / 'deliverables' / video,
                ROOT / 'assets/panda/panda.xml', ROOT / 'assets/ycb/ycb/foam_brick.xml']
    for path in required:
        if not path.is_file():
            raise FileNotFoundError(path)
    if final_submission:
        sys.path.insert(0, str(ROOT / 'scripts'))
        from check_completion_evidence import audit
        audit(ROOT / 'docs/validation/v2.1.0')
    if version == '3.0.0':
        from check_exploration_evidence import audit as audit_explorations
        audit_explorations(ROOT / 'docs/validation/v3.0.0')
    files = [ROOT / name for name in ['main.py', 'challenge_main.py', 'sensing_main.py', 'clutter_main.py', 'README.md', 'requirements.txt',
             'requirements-video.txt', 'CHANGELOG.md', 'PROGRESS.md', 'CONTRIBUTING.md']]
    for directory in ['robot_manipulation', 'scripts', 'tests', 'docs', 'assets']:
        files.extend(p for p in (ROOT / directory).rglob('*') if p.is_file()
                     and '__pycache__' not in p.parts and p.suffix != '.pyc')
    if version == '3.0.0':
        files.append(ROOT / 'exploration_main.py')
        files.extend((ROOT / 'exploration').glob('*.py'))
        files.append(ROOT / 'output/pdf/final_report_v2.1.0.pdf')
    files.append(ROOT / 'deliverables' / video)
    if final_submission:
        files.extend([report_path, ROOT / 'RUN_PROJECT.ps1', ROOT / 'requirements-report.txt',
                      ROOT / 'docs/FINAL_HANDOVER.md'])
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in sorted(set(files)):
            archive.write(path, path.relative_to(ROOT).as_posix())
        if final_submission:
            manifest = {path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                        for path in sorted(set(files))}
            archive.writestr('SUBMISSION_MANIFEST.json', json.dumps(manifest, indent=2) + '\n')
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
        for name in archive.namelist():
            parts = Path(name).parts
            if Path(name).is_absolute() or '..' in parts or any(p in parts for p in ('.git', '.venv', '.env', '__pycache__')):
                raise ValueError(f'Unexpected archive entry: {name}')
        print(f'{target}: {len(archive.namelist())} files, {target.stat().st_size / 1e6:.1f} MB')


if __name__ == '__main__':
    main()
