#!/usr/bin/env python3
"""List the Claude Code sessions the VS Code extension still shows, or archive some of them.

  sessions.py list [repo]   one line per unarchived session of the repo (default: cwd)
  sessions.py archive ID…   write the IDs into the extension's archived list once VS Code has quit

The extension keeps its archived list in VS Code's global state, which VS Code holds in memory and
rewrites on exit: a write made while it runs is lost. `archive` therefore forks a waiter that
applies the change after the VS Code main process exits.
"""
import datetime
import glob
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import time

DB = os.path.expanduser('~/Library/Application Support/Code/User/globalStorage/state.vscdb')
KEY = 'Anthropic.claude-code'
VSCODE_BINARY_SUFFIX = '.app/Contents/MacOS/Code'
LOG = os.path.expanduser('~/.claude/archive-sessions.log')


def read_state():
    row = sqlite3.connect(f'file:{DB}?mode=ro', uri=True).execute('select value from ItemTable where key=?', (KEY,)).fetchone()
    return json.loads(row[0]) if row else {}


def get_project_dir(repo):
    return os.path.expanduser('~/.claude/projects/') + os.path.realpath(repo).replace('/', '-').replace('.', '-')


def to_text(content):
    if isinstance(content, list):
        content = ' '.join(c.get('text', '') for c in content if isinstance(c, dict) and c.get('type') == 'text')
    return content.strip().replace('\n', ' ') if isinstance(content, str) else ''


def describe(path):
    branches, title, first, last = [], None, None, ''
    with open(path) as f:
        for line in f:
            try:
                e = json.loads(line)
            except ValueError:
                continue
            branch = e.get('gitBranch')
            if branch and branch not in ('HEAD', 'main', 'master'):
                if branch in branches:
                    branches.remove(branch)
                branches.append(branch)
            if e.get('type') == 'custom-title':
                title = e.get('customTitle')
            elif e.get('type') == 'summary' and not title:
                title = e.get('summary')
            elif e.get('type') == 'user' and first is None and not e.get('isMeta'):
                text = to_text(e.get('message', {}).get('content'))
                if text and not text.startswith('<'):
                    first = text
            elif e.get('type') == 'assistant':
                last = to_text(e['message'].get('content')) or last
    return branches, title or first or '', last


def list_sessions(repo):
    archived = set(read_state().get('hiddenSessionIds', []))
    for path in sorted(glob.glob(get_project_dir(repo) + '/*.jsonl'), key=os.path.getmtime):
        sid = os.path.basename(path)[:-6]
        if sid in archived:
            continue
        branches, title, last = describe(path)
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M')
        print(f'{sid} | {mtime} | branches (last = current): {",".join(branches) or "-"}\n  title: {title[:100]}\n  last reply: {last[:200]}')


def is_vscode_running():
    out = subprocess.run(['ps', '-axo', 'comm'], capture_output=True, text=True).stdout
    return any(line.endswith(VSCODE_BINARY_SUFFIX) for line in out.splitlines())


def apply_archive(ids):
    shutil.copy2(DB, f'{DB}.bak-archive-sessions')
    con = sqlite3.connect(DB)
    state = json.loads(con.execute('select value from ItemTable where key=?', (KEY,)).fetchone()[0])
    archived = state.get('hiddenSessionIds', [])
    added = [i for i in ids if i not in archived]
    state['hiddenSessionIds'] = archived + added
    con.execute('update ItemTable set value=? where key=?', (json.dumps(state), KEY))
    con.commit()
    return added


def wait_then_archive(ids):
    while is_vscode_running():
        time.sleep(2)
    time.sleep(2)
    added = apply_archive(ids)
    with open(LOG, 'a') as log:
        log.write(f'{datetime.datetime.now():%Y-%m-%d %H:%M} archived {len(added)}: {" ".join(added)}\n')


def archive(ids):
    if not is_vscode_running():
        print(f'VS Code is not running: archived {len(apply_archive(ids))} sessions now.')
        return
    subprocess.Popen([sys.executable, '-I', __file__, '_wait', *ids], start_new_session=True,
                     stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f'Waiter started: {len(ids)} sessions will be archived once VS Code quits (log: {LOG}).')


if __name__ == '__main__':
    command, args = sys.argv[1], sys.argv[2:]
    if command == 'list':
        list_sessions(args[0] if args else os.getcwd())
    elif command == 'archive':
        archive(args)
    elif command == '_wait':
        wait_then_archive(args)
