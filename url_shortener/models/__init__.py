from pathlib import Path

from sqlalchemy import MetaData

metadata = MetaData()

# metadata.tables is only populated after all models are imported.
# see alembic/env.py for an usage example.
modules = Path(__file__).parent.glob('*.py')
__all__ = [p.stem for p in modules if p.is_file() and p.stem != '__init__']
