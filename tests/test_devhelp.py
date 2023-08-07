"""Test for devhelp extension."""

import pytest


@pytest.mark.sphinx('devhelp', testroot='basic')
def test_basic(app, status, warning):
    app.builder.build_all()
