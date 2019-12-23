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
import json
import os
import urllib.parse
import urllib.request

def _get_endpoint(baseurl, testname, numberofruns):
    """Construct the endpoint that is required for getting test results.
    """

    _paramDict = {
        'testname': testname,
        'numberofruns': numberofruns
    }

    return '%s/services/apexrest/perform?%s' % (
        _args.baseurl, urllib.parse.urlencode(_paramDict))

def _get_result_file(testname):
    
    # Construct the path
    _out_dir = '.runner/out'
    _result_file = '%s/%s.csv' % (_out_dir, testname)

    # Create the file if it doesn't already exist
    if not os.path.exists(_result_file):
        os.makedirs(_out_dir)
        with open(_result_file, 'w') as f:
            f.writelines(['testname,rundatetime,duration (ms)'])

    # Return the file
    return _result_file

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

def _write_sample(sample, csvf):
    """Write a sample to the CSV file.
    """

    print('TODO: _write_sample')

# Let's run our script!
if __name__ == '__main__':
    _args = _parse_args()
    
    _endpoint = _get_endpoint(
        baseurl=_args.baseurl,
        testname=_args.testname,
        numberofruns=_args.numberofruns)
    
    print('endpoint: %s' % _endpoint)

    # Initialize the performance test result, then get the actual result
    _result = None

    with urllib.request.urlopen(_endpoint) as f:
        _result = json.loads(f.read().decode('utf-8'))

    # Create the results file if it doesn't already exist
    _result_file = _get_result_file(_args.testname)

    with open(_result_file) as f:
        for _sample in _result['samples']:
            _write_sample(_sample, f)
