#!/usr/bin/env python3
"""Collect Psi4 test timing data into the dashboard data repository."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


FILENAMES = ("timer.json", "scf_iterations.json")


def parse_args() -> argparse.Namespace:
    script_path = Path(__file__).resolve()
    dashboard_data_dir = script_path.parents[1]
    workspace_dir = dashboard_data_dir.parent

    parser = argparse.ArgumentParser(
        description=(
            "Copy timer.json and scf_iterations.json from a Psi4 build tree "
            "into psi4dashboard-data/data/<version>/<test_name>/ds2/."
        )
    )
    parser.add_argument(
        "build_dir",
        help=(
            "Psi4 build directory name under the fixed hrw-master checkout, "
            "for example objdir_py313_master."
        ),
    )
    parser.add_argument(
        "version",
        help="Dashboard data version directory, for example 1.12a1.dev7.",
    )
    parser.add_argument(
        "--psi4-dir",
        default=workspace_dir / "hrw-master",
        type=Path,
        help="Psi4 source checkout containing the build directory. Default: %(default)s",
    )
    parser.add_argument(
        "--dashboard-data-dir",
        default=dashboard_data_dir,
        type=Path,
        help="psi4dashboard-data checkout. Default: %(default)s",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be copied without writing files.",
    )
    return parser.parse_args()


def collect_files(
    build_dir_name: str,
    version: str,
    psi4_dir: Path,
    dashboard_data_dir: Path,
    dry_run: bool,
) -> int:
    tests_dir = psi4_dir / build_dir_name / "tests"
    destination_root = dashboard_data_dir / "data" / version

    if not tests_dir.is_dir():
        raise SystemExit(f"Tests directory not found: {tests_dir}")

    if not dashboard_data_dir.is_dir():
        raise SystemExit(f"Dashboard data directory not found: {dashboard_data_dir}")

    test_dirs = sorted(path for path in tests_dir.iterdir() if path.is_dir())
    copied = 0
    missing = 0
    tests_with_data = 0

    for test_dir in test_dirs:
        destination_dir = destination_root / test_dir.name.replace("-", "_") / "ds2"
        copied_for_test = 0

        for filename in FILENAMES:
            source = test_dir / filename
            if not source.is_file():
                missing += 1
                continue

            destination = destination_dir / filename
            if dry_run:
                print(f"Would copy {source} -> {destination}")
            else:
                destination_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
                print(f"Copied {source} -> {destination}")

            copied += 1
            copied_for_test += 1

        if copied_for_test:
            tests_with_data += 1

    action = "would copy" if dry_run else "copied"
    print(
        f"Summary: scanned {len(test_dirs)} test directories; "
        f"{action} {copied} files from {tests_with_data} tests; "
        f"missing {missing} expected files."
    )

    return 0


def main() -> int:
    args = parse_args()
    return collect_files(
        build_dir_name=args.build_dir,
        version=args.version,
        psi4_dir=args.psi4_dir.resolve(),
        dashboard_data_dir=args.dashboard_data_dir.resolve(),
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    raise SystemExit(main())
