import boto
from moto.s3 import mock_s3
import pytest
from boto.exception import S3ResponseError
from boto.s3.key import Key
from click.testing import CliRunner
from s3_image_optimizer import cli
from s3_image_optimizer.cli import _optimize_image


@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner):
    result = runner.invoke(cli.main, ['bucket', '--id=ab', '--key=abc'])
    assert result.exit_code == -1
    assert result.exception
    assert isinstance(result.exception, S3ResponseError)
    # assert result.output.strip() == 'Done, 0 images optimized.'


def test_cli_no_args(runner):
    result = runner.invoke(cli.main)
    assert result.exit_code == 2
    assert result.exception

    result = runner.invoke(cli.main, ['bucket'])
    assert result.exit_code == 2
    assert result.exception

    result = runner.invoke(cli.main, ['bucket', '--key', '--id'])
    assert result.exit_code == 2
    assert result.exception


@mock_s3
def test_cli_optimize_image(runner):
    conn = boto.connect_s3()
    bucket = conn.create_bucket('test-bucket')

    mock_key = Key(bucket, name='test.jpg')
    mock_key.set_contents_from_string('test')
    # TODO write good test
    _optimize_image(mock_key, '/usr/local/bin/jpegoptim', 'public-read')
