"""Default Contacts settings."""

import os

PLUGIN_BASE_DIR = os.path.dirname(__file__)

CALENDAR_STATS_FILE = os.path.join(
    PLUGIN_BASE_DIR, "static/modoboa_radicale/webpack-stats.json")


def apply(settings):
    """Modify settings."""
    DEBUG = settings['DEBUG']
    if "webpack_loader" not in settings["INSTALLED_APPS"]:
        settings["INSTALLED_APPS"] += ("webpack_loader", )
    wpl_config = {
        "CALENDAR": {
            "CACHE": not DEBUG,
            "BUNDLE_DIR_NAME": "modoboa_radicale/",
            "STATS_FILE": CALENDAR_STATS_FILE,
            "IGNORE": [".+\.hot-update.js", ".+\.map"]
        }
    }
    if "WEBPACK_LOADER" in settings:
        settings["WEBPACK_LOADER"].update(wpl_config)
    else:
        settings["WEBPACK_LOADER"] = wpl_config
