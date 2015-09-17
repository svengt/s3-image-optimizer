import mimetypes
import click
import re
import subprocess
from boto.s3.connection import S3Connection
from tempfile import NamedTemporaryFile


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    '--id', '-i', required=True,
    help='AWS IAM Access Key Id ____________________.')
@click.option(
    '--key', '-k', required=True,
    help='AWS IAM Access Key ________________________________________.')
@click.option(
    '--jpeg-optimizer', default='/usr/local/bin/jpegoptim --strip-all',
    required=True, help='Command that can optimize JPEGs.')
@click.option(
    '--png-optimizer', default='/usr/local/bin/optipng', required=True,
    help='Command that can optimize PNGs.')
@click.option(
    '--policy', default='public-read', required=True,
    help='S3 policy / permission for updated file.')
@click.option(
    '--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.option(
    '--force', '-f', is_flag=True, help='Forces optimization and skips check '
                                        'if image is already optimized.')
@click.argument('bucket', metavar='<bucket_name>')
def main(bucket, id, key, jpeg_optimizer, png_optimizer, policy, verbose,
         force):
    """
    S3 Image Optimizer optimizes all images found in an Amazon S3 bucket.
    """

    conn = S3Connection(id, key)
    bucket = conn.get_bucket(bucket)

    result = bucket.list()
    count = 0

    for key in result:
        optimizer = None

        if key.content_type == 'image/jpeg' or \
                re.search(r'\.jpe?g$', key.name, flags=re.IGNORECASE):
            optimizer = jpeg_optimizer
        elif key.content_type == 'image/png' or \
                re.search(r'\.png$', key.name, flags=re.IGNORECASE):
            optimizer = png_optimizer

        if optimizer is not None:
            # Fetch complete key for metadata
            key = bucket.get_key(key.name)
            # Not yet optimized
            if not key.get_metadata('optimized') or force:
                if verbose:
                    click.echo('Optimizing: {0}'.format(key.name))

                if _optimize_image(key, optimizer, policy, verbose):
                    count += 1
            elif verbose:
                click.echo('Already optimized: {0}'.format(key.name))

    click.echo('Done, {0} images optimized.'.format(count))


def _optimize_image(key, optimizer, policy, verbose=False):
    with NamedTemporaryFile() as temp:
        key.get_file(temp)

        result = subprocess.Popen(
            '{0} {1}'.format(optimizer, temp.name),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        (stdout, stderr) = result.communicate()

        if verbose:
            stdout and click.echo(stdout)
            stderr and click.echo(stderr)

        with open(temp.name, 'rb') as f:
            content_type = mimetypes.guess_type(key.name)[0]
            if content_type:
                key.set_metadata('Content-Type', content_type)

            key.set_metadata('optimized', 1)
            return bool(key.set_contents_from_file(
                f, policy=policy,
            ))
