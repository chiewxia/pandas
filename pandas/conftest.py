import pytest

import numpy
import pandas
import pandas.util._test_decorators as td


def pytest_addoption(parser):
    parser.addoption("--skip-slow", action="store_true",
                     help="skip slow tests")
    parser.addoption("--skip-network", action="store_true",
                     help="skip network tests")
    parser.addoption("--run-high-memory", action="store_true",
                     help="run high memory tests")
    parser.addoption("--only-slow", action="store_true",
                     help="run only slow tests")


def pytest_runtest_setup(item):
    if 'slow' in item.keywords and item.config.getoption("--skip-slow"):
        pytest.skip("skipping due to --skip-slow")

    if 'slow' not in item.keywords and item.config.getoption("--only-slow"):
        pytest.skip("skipping due to --only-slow")

    if 'network' in item.keywords and item.config.getoption("--skip-network"):
        pytest.skip("skipping due to --skip-network")

    if 'high_memory' in item.keywords and not item.config.getoption(
            "--run-high-memory"):
        pytest.skip(
            "skipping high memory test since --run-high-memory was not set")


# Configurations for all tests and all test modules

@pytest.fixture(autouse=True)
def configure_tests():
    pandas.set_option('chained_assignment', 'raise')


# For running doctests: make np and pd names available

@pytest.fixture(autouse=True)
def add_imports(doctest_namespace):
    doctest_namespace['np'] = numpy
    doctest_namespace['pd'] = pandas


@pytest.fixture(params=['bsr', 'coo', 'csc', 'csr', 'dia', 'dok', 'lil'])
def spmatrix(request):
    from scipy import sparse
    return getattr(sparse, request.param + '_matrix')


@pytest.fixture
def ip():
    """
    Get an instance of IPython.InteractiveShell.

    Will raise a skip if IPython is not installed.
    """

    pytest.importorskip('IPython', minversion="6.0.0")
    from IPython.core.interactiveshell import InteractiveShell
    return InteractiveShell()


@pytest.fixture(params=[None, 'gzip', 'bz2', 'zip',
                        pytest.param('xz', marks=td.skip_if_no_lzma)])
def compression(request):
    """
    Fixture for trying common compression types in compression tests
    """
    return request.param


@pytest.fixture(params=[None, 'gzip', 'bz2',
                        pytest.param('xz', marks=td.skip_if_no_lzma)])
def compression_no_zip(request):
    """
    Fixture for trying common compression types in compression tests
    except zip
    """
    return request.param


@pytest.fixture(scope='module')
def datetime_tz_utc():
    from datetime import timezone
    return timezone.utc
