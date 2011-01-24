"""
A tool that expects the input to be a file.  The two output variables are strings
containing the first and last 5 characters of the file.
"""

import os

class FileTest(object):
    def run(self, input_vars, **kwargs):
        print ' Entering FileTest.run()'
        file = input_vars['test_file']
        print '  File value is %s' % file
        start_str = file.read(5)
        file.seek(-5, os.SEEK_END)
        end_str = file.read(5)
        file.close()
        print 'Retrieved contents of %s' % str(file)
        return {'start_str': start_str, 'end_str': end_str}
