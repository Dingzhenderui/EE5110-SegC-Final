"""Build report figures/tables from frozen evidence and compile the LaTeX report.

Does not alter engine files, frozen evidence, or historical reports.
Usage: python scripts/build_final_report.py --engine /path/to/tectonic
Also supports pdflatex and xelatex; use --figures-only to prepare Overleaf sources.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs/final_report'


def prepare_figures():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    destination = SOURCE / 'figures'
    destination.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'savefig.bbox': 'tight', 'pdf.fonttype': 42})
    snapshots = {
        'workcell.png': 'ycb_place.png',
        'rejected.png': 'baseline_failure_v2.1.0.png',
        'inclined.png': 'local_recovery_v2.1.0.png',
        'soft_grasp.png': 'exploration_soft_adaptive_grasp.png',
        'soft_trace.png': 'exploration_soft_trace.png',
        'corrupted_points.png': 'exploration_corrupted_points.png',
        'recovery_place.png': 'exploration_recovery_retry_place.png',
    }
    for name, original in snapshots.items():
        shutil.copyfile(ROOT / 'docs/images' / original, destination / name)

    v2 = json.loads((ROOT / 'docs/validation/v2.1.0/comparison.json').read_text())
    v3 = json.loads((ROOT / 'docs/validation/v3.0.0/comparison.json').read_text())
    # Read complete episode files rather than inferring group data from a chart.
    rows2 = {}
    for group in ['baseline_clutter', 'local_clutter', 'baseline_dense', 'local_dense']:
        paths = list((ROOT / 'docs/validation/v2.1.0' / group).glob('*.jsonl'))
        if len(paths) != 1:
            raise ValueError(f'Expected one frozen JSONL for {group}: {paths}')
        rows = [json.loads(line) for line in paths[0].read_text().splitlines() if line.strip()]
        rows2[group] = (sum(bool(row['success']) for row in rows), len(rows))

    def wilson(k, n):
        z = 1.959963984540054
        p = k/n; divisor = 1+z*z/n
        center = (p+z*z/(2*n))/divisor
        radius = z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/divisor
        return center-radius, center+radius

    fig, ax = plt.subplots(figsize=(7.0, 2.7))
    for method, color, shift in [('baseline', '#9aa9b4', -.17), ('local', '#087e8b', .17)]:
        names = [method+'_clutter', method+'_dense']
        rates = np.array([rows2[n][0]/rows2[n][1] for n in names])*100
        bounds = np.array([wilson(*rows2[n]) for n in names])*100
        ax.bar(np.arange(2)+shift, rates, width=.30, color=color,
               label='Original candidates' if method == 'baseline' else 'Local alternatives')
        ax.errorbar(np.arange(2)+shift, rates, yerr=[rates-bounds[:, 0], bounds[:, 1]-rates],
                    fmt='none', capsize=4, color='#253946', lw=1.2)
        for x, name in zip(np.arange(2)+shift, names):
            k, n = rows2[name]
            ax.text(x, 5, f'{k}/{n}', ha='center', color='white', weight='bold')
    ax.set_xticks([0, 1], ['Three distractors (60/method)', 'Five distractors (30/method)'])
    ax.set_ylim(0, 108); ax.set_ylabel('Complete pick-and-place (%)')
    ax.legend(loc='upper center', bbox_to_anchor=(.5, 1.18), ncol=2, frameon=False)
    ax.grid(axis='y', alpha=.15); ax.set_axisbelow(True)
    fig.savefig(destination/'candidate_results.pdf'); fig.savefig(destination/'candidate_results.png', dpi=180)
    plt.close(fig)

    groups = v3['groups']
    labels = {'crowding_single':'Crowding / single', 'crowding_active':'Crowding / active',
              'articulated':'Passive hinge', 'soft_fixed':'Soft / fixed preload',
              'soft_adaptive':'Soft / force regulation', 'novel_prior':'Novel / box prior',
              'novel_points':'Novel / measured points', 'force_fixed':'Rigid / fixed preload',
              'force_adaptive':'Rigid / force regulation', 'recovery_single':'Fault / one attempt',
              'recovery_retry':'Fault / checked retry', 'sensor_single':'Depth / single packet',
              'sensor_raw_fusion':'Depth / raw fusion', 'sensor_robust':'Depth / robust fusion'}
    fig, ax = plt.subplots(figsize=(8.8, 5.2))
    for i, (name, g) in enumerate(groups.items()):
        k, n = g['successes'], g['trials']; p = k/n*100
        lo, hi = np.array(g['success_rate_95pct_interval'])*100
        color = '#087e8b' if name.endswith(('adaptive','robust','retry','points')) else '#728691'
        ax.errorbar(p, i, xerr=[[max(0, p-lo)], [max(0, hi-p)]], fmt='o', color=color,
                    capsize=3, ms=5, lw=1.5)
        ax.text(104, i, f'{k}/{n}', va='center', fontsize=9)
    ax.set_yticks(range(len(groups)), [labels[n] for n in groups]); ax.invert_yaxis()
    ax.set_xlim(-3, 115); ax.set_xticks([0,25,50,75,100]); ax.set_xlabel('Complete task success (%) with 95% Wilson intervals')
    ax.grid(axis='x', alpha=.18); fig.tight_layout()
    fig.savefig(destination/'exploration_results.pdf'); fig.savefig(destination/'exploration_results.png', dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 2.3)); ax.axis('off'); ax.set_xlim(0, 9); ax.set_ylim(0, 2.1)
    stages = [('Observe', 'points / geometry'), ('Propose', 'bounded candidates'),
              ('Preflight', 'IK + collisions'), ('Execute', 'contact dynamics'), ('Verify', 'independent gates')]
    for i, (title, detail) in enumerate(stages):
        x = .02+i*1.80
        ax.add_patch(FancyBboxPatch((x, .8), 1.65, .85, boxstyle='round,pad=.025',
                                   facecolor='#edf6f6', edgecolor='#087e8b', lw=1.2))
        ax.text(x+.825, 1.36, title, ha='center', weight='bold', color='#123746')
        ax.text(x+.825, 1.02, detail, ha='center', fontsize=8)
        if i < 4:
            ax.add_patch(FancyArrowPatch((x+1.66, 1.23), (x+1.80, 1.23), arrowstyle='->', mutation_scale=10))
    ax.annotate('Permitted failure: open, checked withdrawal, reobserve; same evolving scene',
                xy=(.8, .68), xytext=(4.5, .15), ha='center', fontsize=9,
                arrowprops=dict(arrowstyle='->', connectionstyle='angle,angleA=0,angleB=-90,rad=8', color='#d17a28'))
    fig.savefig(destination/'pipeline.pdf'); plt.close(fig)

    lines = []
    for name, g in groups.items():
        lo, hi = g['success_rate_95pct_interval']
        failure = ', '.join(f'{k.replace("_", " ").lower()}: {v}' for k, v in g['failures'].items()) or 'None'
        lines.append(f"{labels[name]} & {g['successes']}/{g['trials']} & {100*lo:.1f}--{100*hi:.1f} & {failure} \\\\")
    table = (r'\begin{tabularx}{\linewidth}{@{}p{45mm}cp{25mm}Y@{}}'+'\n'
             +r'\toprule Condition & Complete & 95\% Wilson (\%) & Failure counts \\'+'\n'
             +r'\midrule'+'\n'+'\n'.join(lines)+'\n'
             +r'\bottomrule'+'\n'+r'\end{tabularx}'+'\n')
    (SOURCE/'results_table.tex').write_text(table, encoding='utf-8')
    (SOURCE/'evidence_summary.json').write_text(json.dumps({'v2': rows2,
         'v3': {n: {'successes':g['successes'], 'trials':g['trials'], 'wilson95':g['success_rate_95pct_interval']}
                for n,g in groups.items()}, 'v2_source_sha256':v2['source_sha256'],
         'v3_source_sha256':v3['source_sha256']}, indent=2)+'\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine', help='Tectonic, pdflatex or xelatex executable')
    parser.add_argument('--figures-only', action='store_true')
    parser.add_argument('--source-zip', action='store_true', help='Export self-contained Overleaf sources under output/packages')
    args = parser.parse_args()
    prepare_figures()
    if args.source_zip:
        target = ROOT/'output/packages/EE5110_LaTeX_Source.zip'
        target.parent.mkdir(parents=True, exist_ok=True)
        files = [SOURCE/name for name in ['report.tex', 'results_table.tex', 'README.md', 'evidence_summary.json']]
        files.extend(p for p in (SOURCE/'figures').rglob('*') if p.is_file())
        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(files):
                archive.write(path, path.relative_to(SOURCE).as_posix())
        with zipfile.ZipFile(target) as archive:
            if archive.testzip() is not None:
                raise ValueError('LaTeX source ZIP CRC check failed')
        print(f'Exported Overleaf source: {target}')
    if args.figures_only:
        print(f'Prepared figures and evidence tables: {SOURCE}'); return
    engine = args.engine or next((shutil.which(n) for n in ['tectonic','pdflatex','xelatex'] if shutil.which(n)), None)
    if not engine:
        parser.error('Install a LaTeX engine or pass --engine; Overleaf can compile docs/final_report/report.tex')
    build = ROOT/'outputs/report_build'
    build.mkdir(parents=True, exist_ok=True)
    if 'tectonic' in Path(engine).name.lower():
        command = [engine, '--keep-logs', '--untrusted', '--outdir', str(build), 'report.tex']
        subprocess.run(command, cwd=SOURCE, check=True)
    else:
        for _ in range(2):
            subprocess.run([engine, '-interaction=nonstopmode', '-halt-on-error', '-output-directory', str(build), 'report.tex'], cwd=SOURCE, check=True)
    output = ROOT/'output/pdf/EE5110_Final_Report.pdf'; output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(build/'report.pdf', output)
    # Optional local rendering library; PDF creation itself does not depend on it.
    try:
        import pymupdf
        with pymupdf.open(output) as document:
            if len(document) != 10:
                raise ValueError(f'Expected 10 substantive pages, found {len(document)}')
            for i, page in enumerate(document):
                if len(page.get_text().strip()) < 250:
                    raise ValueError(f'Unexpectedly sparse report page {i+1}')
            print(f'Compiled and checked {len(document)} pages: {output}')
    except ImportError:
        print(f'Compiled report: {output}. Verify the 10-page limit in a PDF viewer.')


if __name__ == '__main__':
    main()
