# Releasing cdpify

Version 0.6.0 is prepared in `pyproject.toml` and `uv.lock`. Its
[changelog entry](CHANGELOG.md#060---unreleased) stays marked **Unreleased**
until the publication date is set.

## Validate the release candidate

Run from the repository root with Python 3.12 or newer:

```bash
uv sync --dev --extra orjson --locked
uv run --extra orjson pytest
uv run ruff check . --exclude cdpify/domains
uv run ruff format --check . --exclude cdpify/domains
uv run --locked smelt check --fail-on warning --show-hints
uv run --extra orjson pyright
uv run python scripts/check_generated.py
uv run --extra orjson pytest -m integration -v
uv run --extra orjson python benchmarks/runtime.py --iterations 1000 --samples 3
```

The unit suite exercises both JSON backends when `orjson` is installed. The
integration suite needs Chrome or Chromium; set `CHROME_PATH` if discovery does
not find it. Confirm that these tests run rather than skip. They launch a
headless browser with an isolated profile. CI additionally tests Python 3.12,
3.13 and 3.14 on Ubuntu, Windows and macOS; require those checks to pass on the
release commit.

Use the bundled-spec drift check above for release validation. The generator
CLI downloads the latest upstream specs and replaces its output directory;
review any protocol refresh separately before including it in a release.

Build both distributions and validate their package metadata:

```bash
uv build
uvx twine check --strict dist/cdpify-0.6.0-py3-none-any.whl dist/cdpify-0.6.0.tar.gz
```

Smoke-test the wheel from outside the source checkout in a clean environment.
Verify that the core imports without extras, that `cdpify.error` and generated
domains import, and that the wheel contains `cdpify/py.typed` and the generator's
`templates/*.jinja2` files. Install the `websocket` extra for a real connection
and the `generator` extra when testing generation. Check the source distribution
too: it must include the README, changelog and this checklist, and build a wheel
with the same version and package files. Verify the documentation links in the
README also work from the PyPI project description.

## Publish when ready

1. Review the [0.5.x to 0.6.0 migration guide](docs/migration.md#05x--060) and
   the complete 0.6.0 changelog against the changes since `v0.5.0`.
2. Replace `Unreleased` in the 0.6.0 changelog heading with the publication
   date (`YYYY-MM-DD`) and update this checklist's link and release status.
   Commit the release changes and merge them into `main` after CI passes.
3. Rebuild and validate both distributions from that exact commit. Use the
   explicit 0.6.0 filenames so older files in `dist/` are excluded.
4. Tag the validated commit and push the tag:

   ```bash
   git tag -a v0.6.0 -m "Release 0.6.0"
   git push origin v0.6.0
   ```

5. Publish the artifacts using the project's PyPI credentials:

   ```bash
   uv publish dist/cdpify-0.6.0-py3-none-any.whl dist/cdpify-0.6.0.tar.gz
   ```

6. Create a GitHub release for `v0.6.0` using the changelog's 0.6.0 section as
   release notes, with breaking changes first. Verify the installed version
   from PyPI in a clean environment with `pip install "cdpify[websocket]==0.6.0"`.

The repository currently has CI and weekly spec-update workflows; neither
publishes to PyPI. Pushing a tag alone does not publish the package.
