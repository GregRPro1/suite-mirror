
from __future__ import annotations
import sys, os, pathlib, yaml, traceback, inspect

from PyQt6.QtWidgets import QApplication

# Prefer package imports; fall back to shims if any import fails
def _try_import(path, name):
    try:
        mod = __import__(path, fromlist=[name])
        return getattr(mod, name, None)
    except Exception:
        return None

# ---- Shims (used only if real classes unavailable or fail to construct) ----
class _ActionRegistryShim:
    def __init__(self): self._actions = {}
    def attach_recorder(self, observer): setattr(self, "_observer", observer)
    def register(self, spec: dict): self._actions[spec.get("id","?")] = spec

class _JobRunnerShim:
    def __init__(self): pass

class _ThemeManagerShim:
    def __init__(self, project=None): self._project = project or {}
    def apply_brand(self, *a, **k): pass
    def apply_layout(self, *a, **k): pass

class _PluginManagerShim:
    def __init__(self): pass
    def load_builtin_panels(self, *a, **k): pass
    def toggle_panel(self, *a, **k): pass

class _ProjectManagerShim:
    def __init__(self, project=None): self.current = project or {}
    def open_project(self, path): 
        try:
            p = pathlib.Path(path)
            y = p/"project.yaml" if p.is_dir() else p
            self.current = yaml.safe_load(y.read_text(encoding="utf-8")) or {}
        except Exception:
            self.current = {}

class _SettingsManagerShim:
    def __init__(self, project=None): self.project = project or {}

# Resolve classes (or None)
ActionRegistry = _try_import("base_app.services.action_registry", "ActionRegistry") or _ActionRegistryShim
JobRunner      = _try_import("base_app.services.job_runner", "JobRunner") or _JobRunnerShim
ThemeManager   = _try_import("base_app.services.theme_manager", "ThemeManager")                  or _try_import("base_app.services.theme_manager", "ThemeService") or _ThemeManagerShim
PluginManager  = _try_import("base_app.services.plugin_manager", "PluginManager") or _PluginManagerShim
ProjectManager = _try_import("base_app.services.project_manager", "ProjectManager")                  or _try_import("base_app.services.project_manager", "ProjectService") or _ProjectManagerShim
SettingsManager= _try_import("base_app.services.settings_manager", "SettingsManager") or _SettingsManagerShim

# MainWindow resolver
def _get_mainwindow():
    try:
        from base_app.core.main_window import MainWindow
        return MainWindow
    except Exception as e:
        print("ERROR importing MainWindow:", e, file=sys.stderr)
        raise

def _load_project(project_arg: str | None) -> dict | None:
    if not project_arg:
        return None
    p = pathlib.Path(project_arg)
    y = p / "project.yaml" if p.is_dir() else p
    if y.exists():
        try:
            return yaml.safe_load(y.read_text(encoding="utf-8")) or {}
        except Exception:
            traceback.print_exc()
            return {}
    return None

def _safe_construct(cls, *args, **kwargs):
    # Try provided args first, then no-arg, then with single project kw if available
    try:
        return cls(*args, **kwargs)
    except TypeError:
        # try no-arg
        try:
            return cls()
        except Exception:
            # try with project kw
            try:
                return cls(kwargs.get("project", None))
            except Exception:
                pass
    except Exception:
        pass
    # fall back to shim instance if class itself is shim
    try:
        return cls()
    except Exception:
        return None

def _construct_services(project_dict: dict | None):
    # Attempt sensible constructor args for each
    actions  = _safe_construct(ActionRegistry)
    jobs     = _safe_construct(JobRunner)
    themes   = _safe_construct(ThemeManager, project=project_dict)
    plugins  = _safe_construct(PluginManager)
    # Prefer zero-arg for ProjectManager in many skeletons
    projects = _safe_construct(ProjectManager) or _safe_construct(ProjectManager, project=project_dict)
    settings = _safe_construct(SettingsManager, project=project_dict)

    return actions, jobs, themes, plugins, projects, settings

def _instantiate_main_window(project_dict: dict | None):
    MainWindow = _get_mainwindow()
    actions, jobs, themes, plugins, projects, settings = _construct_services(project_dict)

    # 1) Positional 6-arg
    try:
        return MainWindow(actions, jobs, themes, plugins, projects, settings)
    except Exception as e1:
        print("MainWindow 6-arg failed:", repr(e1), file=sys.stderr)

    # 2) kwargs by signature
    try:
        sig = inspect.signature(MainWindow.__init__)
        kwargs = {}
        mapping = {
            "actions": actions, "action_registry": actions,
            "jobs": jobs, "job_runner": jobs, "runner": jobs,
            "themes": themes, "theme_manager": themes, "theme_service": themes,
            "plugins": plugins, "plugin_manager": plugins,
            "projects": projects, "project_manager": projects, "project_service": projects,
            "settings": settings, "settings_manager": settings,
            "project": project_dict, "config": project_dict,
        }
        for name, p in sig.parameters.items():
            if name == "self": continue
            if name in mapping:
                kwargs[name] = mapping[name]
        return MainWindow(**kwargs)
    except Exception as e2:
        print("MainWindow kwargs failed:", repr(e2), file=sys.stderr)

    # 3) Legacy fallbacks
    for attempt in (
        lambda: MainWindow(project=project_dict),
        lambda: MainWindow(projects=projects),
        lambda: MainWindow(),
    ):
        try:
            return attempt()
        except Exception as e3:
            print("MainWindow legacy attempt failed:", repr(e3), file=sys.stderr)
            continue

    raise RuntimeError("Unable to instantiate MainWindow with available services. "
                       "Tried positional, kwargs by signature, and legacy fallbacks.")

def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    project = None
    if "--project" in argv:
        try:
            idx = argv.index("--project")
            project_path = argv[idx+1]
        except Exception:
            project_path = None
        project = _load_project(project_path)

    if "QT_QPA_PLATFORM" not in os.environ:
        os.environ["QT_QPA_PLATFORM"] = "windows" if os.name == "nt" else "xcb"

    app = QApplication.instance() or QApplication(sys.argv)
    win = _instantiate_main_window(project)
    win.show()
    return app.exec()
