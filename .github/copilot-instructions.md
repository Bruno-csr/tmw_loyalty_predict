# Copilot / AI Agent Instructions for this repo

Purpose: give an AI coding agent the minimum, actionable context to be productive.

- **Project overview:** This repo builds a loyalty/engagement ML pipeline (feature store → training → inference). See [README.md](README.md) for author intent and high-level goals.
- **Where code lives:** core scripts are under [src/analytics](src/analytics) and utility/experiments under [src/Outros](src/Outros).
- **Primary data locations:** CSVs and small DBs live under `data/` (notably `data/analytics/` and `data/loyalty-system/`).

Key patterns and actionable notes
- Conda-based environment: use `environment.yml` and the conda env `loyalty-predict`. Commands:
  - `conda env create -f environment.yml`
  - `conda activate loyalty-predict`
- Scripts are written as runnable Python files with interactive `# %%` cells (designed for VS Code/interactive runs). Run them from project root, e.g.: `python src/analytics/train.py`.
- SQLite DB usage: many scripts connect via relative SQLite URIs. Examples:
  - `src/analytics/train.py` creates engine `sqlite:///../../data/analytics/database.db` and expects table `abt_fiel`.
  - `src/Outros/frequencia_valor.py` uses `sqlite:///../../data/loyalty-system/database.db` and the SQL file `src/Outros/frequencia_valor.sql`.
  Be careful to run scripts with the project root as CWD so relative DB paths resolve.

Conventions and idioms discovered
- Variable names and comments are in Portuguese (e.g., `flFiel`, `qtdePontosPos`, `descLifeCycleAtual`). Preserve original naming when modifying code unless refactoring broadly.
- Small, exploratory scripts are common (plots, ad-hoc clustering). Favor minimal invasive changes and keep exploratory outputs (plots/prints) unless asked to formalize.
- No test framework found: avoid adding assumptions about CI/test runners; ask before introducing tests or CI.

Integration and external dependencies
- No MLFlow or external deployment configs were found in the repository, although `README.md` mentions MLFlow—treat MLFlow as an aspirational integration unless the user points to its config.
- The code expects a local sqlite-backed dataset; do not attempt to run remote DB migrations or cloud services.

Helpful examples for common agent tasks
- To inspect feature engineering and train flow: open [src/analytics/train.py](src/analytics/train.py).
- To reproduce the `frequencia/valor` clustering experiment: run `src/Outros/frequencia_valor.py` from project root; it reads `src/Outros/frequencia_valor.sql` to build the dataset.

When changing code
- Keep changes minimal and localized. Many scripts are exploratory; prefer to add new files rather than edit original notebooks/scripts unless consolidating or refactoring intentionally.
- If adding Python CLI behavior, follow the existing simple-run pattern (no packaging) and document usage in `README.md`.

If you need more context
- Ask the human owner if they expect MLFlow, app deployment, or tests to be present—these are referenced in docs but not implemented.
- Confirm intended current working directory and dataset availability before running scripts (use the Conda environment).

Files worth checking first
- [README.md](README.md)
- [environment.yml](environment.yml)
- [src/analytics/train.py](src/analytics/train.py)
- [src/Outros/frequencia_valor.py](src/Outros/frequencia_valor.py)

End of instructions — please ask for clarification or to iterate on any missing details.
