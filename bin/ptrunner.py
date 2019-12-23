# This is the script used to collect performance test data from Salesforce
# by executing a test with various parameters.
#
#   ptrunner.py \
#       -t PerformLoopLocalVariableSingleUse \
#       -n 1000 \
#       -p number_of_accounts=100 \
#       -r https://example.my.salesforce.com/
#
# The example above runs the `PtLoopLocalVariableSingleUse` performance test
# 1,000 times, where the number of accounts used in the test is 100. The
# endpoint for the HTTP GET request is specified by the `-r` argument.

import argparse
import collections
import urllib.parse
import urllib.request

def _parse_args():
    """Parse command line arguments from script execution.
    """

    _parser = argparse.ArgumentParser(
        description='Run performance tests against Salesforce.')
    
    _parser.add_argument('-t', '--testname', type=str,
                         required=True,
                         help='the name of the test to run')
    
    _parser.add_argument('-r', '--baseurl', type=str,
                         required=True,
                         help=('the base URL on which to build '
                               'the full endpoint with parameters'))

    _parser.add_argument('-p', '--parameters', type=str,
                         help='URL parameters to add to further definethe test')

    _parser.add_argument('-n', '--numberofruns', type=int,
                         default=10,
                         help='the number of times to run the test')

    return _parser.parse_args()

# Let's run our script!
if __name__ == '__main__':
    _args = _parse_args()

    # Prepare to collect the results
    _samples = []

    _paramDict = {
        'testname': _args.testname,
        'numberofruns': _args.numberofruns
    }

    # Build the URL
    UnparseParam = collections.namedtuple(
        'UnparseParam',
        ['scheme', 'netloc', 'url']
    )

    _endpoint = '%s/services/apexrest/perform?%s' % (
        _args.baseurl, urllib.parse.urlencode(_paramDict))
    
    print('endpoint: %s' % _endpoint)

    # Get the result
    with urllib.request.urlopen(_endpoint) as f:
        print(f.read().decode('utf-8'))
