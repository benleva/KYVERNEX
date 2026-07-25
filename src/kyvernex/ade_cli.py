from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Sequence

from .autonomous_development import AutonomousDevelopmentEngine, DevelopmentPolicy, build_m3_backlog
from .program_manager import KyvernexGovernanceOrchestrator, KyvernexProgramManager, Milestone


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create the next policy-bounded KYVERNEX autonomous development cycle.")
    parser.add_argument("--artifact-directory", type=Path, default=Path("artifacts"))
    parser.add_argument("--checkpoint", type=Path, default=Path("artifacts/ADE_GOVERNANCE_CHECKPOINT.json"))
    parser.add_argument("--max-story-points", type=int, default=8)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    manager = KyvernexProgramManager(
        milestones=(Milestone("M3", "Autonomous Development", "0.2.0"),),
        items=build_m3_backlog(),
    )
    orchestrator = KyvernexGovernanceOrchestrator(
        manager=manager,
        target_version="0.2.0",
        checkpoint_path=args.checkpoint,
    )
    engine = AutonomousDevelopmentEngine(
        orchestrator=orchestrator,
        policy=DevelopmentPolicy(max_story_points_per_cycle=args.max_story_points),
        artifact_directory=args.artifact_directory,
    )
    plan = engine.plan_next_cycle(milestone_id="M3")
    print(json.dumps(asdict(plan), indent=2, sort_keys=True))
    return 0 if plan.stop_reason is None else 2


if __name__ == "__main__":
    raise SystemExit(main())
