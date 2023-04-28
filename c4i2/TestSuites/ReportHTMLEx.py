import io
import os
import unittest
from Libraries.Plugins import HtmlTestRunner
from Libraries.Framework.Paths import BasePaths

from TestCases.Web.FunctionEx import TestCaseEx
from TestCases.Web.FunctionEx import TestPhanQuyen


class MyHTMLTestRunner(HtmlTestRunner.HTMLTestRunner):
    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.stream.writeln("FAILED")


if __name__ == '__main__':
    test_cases = [TestCaseEx]
    suite = unittest.TestSuite()
    for test_case in test_cases:
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPhanQuyen.TestPhanQuyen))
    runner = MyHTMLTestRunner(report_name='TestScript_PhanQuyen4', report_title='Report Phân Quyền',
                              output=BasePaths().getPathReportForWeb(), descriptions=True, combine_reports=True)
    runner.run(suite)
