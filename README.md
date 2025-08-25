# Master Psy Vignette Generator

A small project used for a master's thesis to generate value-based vignettes and questions using OpenAI models, and save them as PDFs.

## Quickstart

1. Python 3.10+
2. Install package (editable install is fine):

   pip install -e .

3. Configure environment:
   - Copy `.env.example` to `.env` and fill in `OPENAI_API_KEY`
   - Optionally set `OUTPUT_DIR`, `LOG_LEVEL`, `LOG_FILE`

4. Run via CLI:

   master-psy --output-dir output --log-level INFO

Or run the script directly:

   python main.py

## Configuration
- `OPENAI_API_KEY` (required): your OpenAI API key
- `OUTPUT_DIR` (optional): directory for generated PDFs (default `output/`)
- `LOG_LEVEL` (optional): DEBUG|INFO|WARNING|ERROR|CRITICAL (default INFO)
- `LOG_FILE` (optional): path to log file (default `vignette_generation.log`)

## Testing
- Install dev dependency pytest if needed: `python -m pip install pytest`
- Run tests from the project root:
  - `pytest -q`

## Notes
- The CLI is a thin wrapper over the original pipeline (now packaged under `master_psy.pipeline`).
- The repository contains modules under `analysis/`, `domain/`, `generator/`, `output/`, `prompts/`, and `utils/`.
- Large/binary files live in `data/` (ignored by Git) and should not be committed.

## Development
- Install dev tools and hooks:
  - `python -m pip install -e .[dev]`
  - `pre-commit install`
- Run linters/formatters:
  - `ruff . --fix`
  - `black .`

## Statistical analysis scripts
The `statistical_analysis/` folder contains self-contained research scripts (06–14). To run them, install analysis extras:

- `python -m pip install -e .[analysis]`

Typical inputs/outputs are described in each script header. They expect:
- Cleaned wide CSV: `data/interim/clean_phase1_phase2_raw.csv`
- Phase I summary CSV: `data/processed/phase1_btpooled.csv`
- Panel long: `data/processed/panel_long.parquet`
- Configs: `config/pairs.yaml`, `config/blocks.yaml`
- Tables will be written under `tables/` and processed data under `data/processed/`

## License
MIT

