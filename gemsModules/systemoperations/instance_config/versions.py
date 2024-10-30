# GEMS note: We should not modify production configuration files automatically. It should only run in a DevEnv.
import datetime
import json
import os
from pathlib import Path
import shutil
from typing import Dict
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)

class DateReversioner:
    """A class to version a json file based on a timestamp."""

    def __init__(
        self, active_config: Path, new_config: Path = None, new_config_data: Dict = None
    ):
        self.file_to_version = active_config
        self._old_version_data = None

        self._new_version = new_config
        self._new_version_data = new_config_data
        
    @property
    def old_version(self):
        """Return the old version data."""
        if self.file_to_version.exists() and self._old_version_data is None:
            with open(self.file_to_version) as f:
                self._old_version_data = json.load(f)

        return self._old_version_data

    @property
    def new_version(self):
        """Return the new version data."""
        if self._new_version_data is None and self._new_version is not None:
            with open(self._new_version) as f:
                self._new_version_data = json.load(f)

        return self._new_version_data

    def set_new_config_data(self, config: Dict):
        # Because this doesn't use a path, unset it.
        self._new_version = None
        self._new_version_data = config

    def set_new_config_path(self, config_path: Path):
        # Likewise, unset data so we can regenerate it from the path.
        self._new_version_data = None
        self._new_version = config_path

    @property
    def is_outdated(self) -> bool:
        """Return True if the file_to_version is older than the new_version."""
        is_outdated = False
        if not self.file_to_version.exists():
            is_outdated = True

        if "date" not in self.new_version:
            raise RuntimeError("Template file does not have a date, cannot update.")

        if self.old_version is None or "date" not in self.old_version:
            # if no date is found, lets update to a versioned file
            is_outdated = True
        else:
            # compare old and new version dates
            old_date = datetime.datetime.strptime(
                self.old_version["date"], "%Y-%m-%dT%H:%M:%S.%f"
            ).date()
            new_date = datetime.datetime.strptime(
                self.new_version["date"], "%Y-%m-%dT%H:%M:%S.%f"
            ).date()
            is_outdated = new_date > old_date
        
        log.debug(is_outdated)
        return is_outdated

    def update(self, force_update=False) -> bool:
        """Update the file_to_version with the current date."""
        needs_update = (force_update and not os.getenv("SWARM") == "true") or (
            self.is_outdated
            or os.getenv("GEMS_FORCE_INSTANCE_RECONFIGURATION") == "True"
        )

        if needs_update:
            # Backup the file_to_version.
            if self.file_to_version.exists():
                backup_file = self.file_to_version.with_suffix(
                    f".json.{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-git-ignore-me.bak"
                )
                shutil.copyfile(self.file_to_version, backup_file)

            # copy the new version in place of the file_to_version
            with self.file_to_version.open("w") as f:
                json.dump(self.new_version, f, indent=2)
                print(f"\nUpdated {self.file_to_version} with new date.")

            self._keep_most_recent_backups()
        else:
            print(f"\nNo update needed for {self.file_to_version}.")

        return needs_update

    def _keep_most_recent_backups(self):
        """Remove all but the most recent backup per run."""
        # sort backup files then group them by run and keep the most recent backup per run
        backup_files = sorted(
            self.file_to_version.parent.glob(
                f"{self.file_to_version.stem}.json.*-git-ignore-me.bak"
            ),
            key=lambda x: x.stat().st_mtime,
        )
        runs = self._group_by_runs(backup_files)

        for run in runs:
            for file in run[:-1]:
                file.unlink()

    def _group_by_runs(self, backup_files, run_period=24 * 3600):
        """Group backup files into runs."""
        runs = []
        current_run = []
        first_file_time = None

        for file in backup_files:
            file_time = datetime.datetime.fromtimestamp(file.stat().st_mtime)

            if not first_file_time:
                # Initialize the first file time and start the first run
                first_file_time = file_time
                current_run.append(file)
                continue

            # If the file is within the run period, add it to the current run
            if (first_file_time - file_time).total_seconds() < run_period:
                current_run.append(file)
            else:
                # Save the current run and start a new one
                runs.append(current_run)
                current_run = [file]
                first_file_time = file_time

        if current_run:
            runs.append(current_run)

        return runs
