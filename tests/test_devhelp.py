"""Test for devhelp extension."""
from time import sleep

import pytest


@pytest.mark.sphinx('devhelp', testroot='basic')
def test_basic(app, status, warning):
    app.builder.build_all()


@pytest.mark.sphinx('devhelp', testroot='basic', freshenv=True)
def test_basic_deterministic_build(app):
    app.config.devhelp_basename, output_filename = 'testing', 'testing.devhelp.gz'

    app.builder.build_all()
    output_initial = (app.outdir / output_filename).read_bytes()

    sleep(2)

    app.builder.build_all()
    output_repeat = (app.outdir / output_filename).read_bytes()

    msg = f"Content of '{output_filename}' differed between builds."
    assert output_repeat == output_initial, msg
