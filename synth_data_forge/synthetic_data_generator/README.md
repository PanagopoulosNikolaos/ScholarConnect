## Directory Summary
This directory houses the modular components of the synthetic data generation system. Each file implements a specialized generator class that targets a specific entity or relationship within the ScholarConnect database schema, utilizing the Faker library to ensure data realism and variety.

## Documentation Index
- [`__init__.py`](../../docs/synth_data_forge_docs/synthetic_data_generator_docs/__init___synthetic_data_generator_doc.md) — Exposes the generator classes for easier access.
- [`base_generator.py`](../../docs/synth_data_forge_docs/synthetic_data_generator_docs/base_generator_doc.md) — Abstract base class providing common utilities like seeding and ID generation.
- [`course_generator.py`](../../docs/synth_data_forge_docs/synthetic_data_generator_docs/course_generator_doc.md) — Logic for generating synthetic course records.
- [`professor_generator.py`](../../docs/synth_data_forge_docs/synthetic_data_generator_docs/professor_generator_doc.md) — Logic for generating synthetic professor records.
- [`relationship_generator.py`](../../docs/synth_data_forge_docs/synthetic_data_generator_docs/relationship_generator_doc.md) — Logic for generating complex relationship tables like Enrollments and Evaluations.
- [`student_generator.py`](../../docs/synth_data_forge_docs/synthetic_data_generator_docs/student_generator_doc.md) — Logic for generating synthetic student records.
