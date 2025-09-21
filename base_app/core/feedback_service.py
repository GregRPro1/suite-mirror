
from __future__ import annotations
import zipfile, datetime, json, urllib.parse, pathlib
from pathlib import Path

DEFAULT_RESULTS = Path('_results')
DEFAULT_CORE = Path('base_app')/'core'

class FeedbackService:
    def __init__(self, results_dir: Path | None = None):
        self.results_dir = Path(results_dir) if results_dir else DEFAULT_RESULTS
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.core_dir = DEFAULT_CORE; self.core_dir.mkdir(parents=True, exist_ok=True)
    def bundle(self, name: str = 'feedback_bundle') -> Path:
        ts = datetime.datetime.now(datetime.UTC).strftime('%Y%m%d_%H%M%S')
        zip_path = self.results_dir / f"{name}_{ts}.zip"
        artifacts = []
        logs_dir = Path('tmp')/'logs'
        if logs_dir.exists():
            for p in logs_dir.glob('**/*'):
                if p.is_file(): artifacts.append(p)
        for p in [self.core_dir/'crash.marker']:
            if p.exists(): artifacts.append(p)
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
            for p in artifacts: z.write(p, p.as_posix())
        return zip_path
    def set_crash_marker(self, reason: str = 'unknown') -> Path:
        marker = self.core_dir / 'crash.marker'; marker.write_text(reason, encoding='utf-8'); return marker
    def clear_crash_marker(self):
        marker = self.core_dir / 'crash.marker'; 
        if marker.exists(): marker.unlink()

class FileTransport:
    def __init__(self, out_dir: str | Path = '_results'):
        self.out_dir = Path(out_dir); self.out_dir.mkdir(parents=True, exist_ok=True)
    def send(self, path: str | Path) -> Path:
        return Path(path)

class WebhookTransport:
    """Stub: supports file://<path> to simulate network post by copying metadata."""
    def __init__(self, url: str):
        self.url = url
    def send(self, path: str | Path) -> Path:
        u = urllib.parse.urlparse(self.url)
        if u.scheme == 'file':
            out = Path(u.path)
            out.parent.mkdir(parents=True, exist_ok=True)
            data = {'sent': True, 'artifact': str(Path(path).as_posix())}
            out.write_text(json.dumps(data), encoding='utf-8')
            return out
        # For http/https we would issue a real POST; omitted in smoke tests
        return Path(str(path))
