#!/usr/bin/env python
"""Tests for `lna` package."""
from os import path as lib_path
import pytest

from click.testing import CliRunner

from lna import lna
from lna import cli

from lna.utils import corpus_to_vocab
from lna.algorithms import *

# TODO: write a data tools to process path or file handling.
DATA_FD = './data'


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'lna.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


def test_bpe():
    # Notice that in the first iteration,
    # that 'r _' has the same frequency as 'e r'.
    path = lib_path.join(DATA_FD, 'bpe.txt')
    vocab = corpus_to_vocab(path)
    vocab, best_bigrams = byte_pair_encoding(vocab)
    assert (vocab, best_bigrams) == (
        {
            'lo w _': 5,
            'lo w e s t _': 2,
            'new _': 2,
            'new er_': 6,
            'w i d er_': 3
        },
        [
            'er',
            'er_',
            'ne',
            'new',
            'lo',
        ],
    )


def test_med():
    # Test minimum edit distance,
    # and augmented minimum edit distance.
    source = 'leda'
    target = 'deal'
    result = min_edit_distance(source, target)
    result_aug, aligment = min_edit_distance_pro(source, target)
    assert result == 4
    assert (result_aug, aligment) == (
        4,
        [
            ('l', '*', 'd'),
            ('e', '*', 'd'),
            ('d', 'd', ' '),
            ('*', 'e', 'i'),
            ('a', 'a', ' '),
            ('*', 'l', 'i'),
        ],
    )
