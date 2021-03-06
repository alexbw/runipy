
import unittest
from glob import glob
from os import path
import re

from IPython.nbformat.current import read

from runipy.notebook_runner import NotebookRunner

class TestRunipy(unittest.TestCase):
    def prepare_cell(self, cell):
        cell = dict(cell)
        if 'metadata' in cell:
            del cell['metadata']
        if 'text' in cell:
            cell['text'] = re.sub('0x[0-9a-f]{9}', '<HEXADDR>', cell['text'])
        return cell


    def assert_notebooks_equal(self, expected, actual):
        self.assertEquals(len(expected['worksheets'][0]['cells']),
                len(actual['worksheets'][0]['cells']))

        for expected_out, actual_out in zip(expected['worksheets'][0]['cells'],
                actual['worksheets'][0]['cells']):
            for k in set(expected_out).union(actual_out):
                if k == 'outputs':
                    self.assertEquals(len(expected_out[k]), len(actual_out[k]))
                    for e, a in zip(expected_out[k], actual_out[k]):
                        e = self.prepare_cell(e)
                        a = self.prepare_cell(a)
                        self.assertEquals(e, a)
                    

    def testRunNotebooks(self):
        input_glob = path.join('tests', 'input', '*.ipynb')
        for notebook_file in glob(input_glob):
            notebook_file_base = path.basename(notebook_file)
            print notebook_file_base
            expected_file = path.join('tests', 'expected', notebook_file_base)
            runner = NotebookRunner(read(open(notebook_file), 'json'))
            runner.run_notebook(True)
            expected = read(open(expected_file), 'json')
            self.assert_notebooks_equal(expected, runner.nb)


if __name__ == '__main__':
    unittest.main()

