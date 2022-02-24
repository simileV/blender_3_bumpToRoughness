#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

# <pep8 compliant>

import unittest

from check_utils import (sliceCommandLineArguments,
                         SceiptUnitTesting)


class UnitTesting(SceiptUnitTesting):
    def test_numpyImports(self):
        self.checkScript("numpy_import")

    def test_numpyBasicOperation(self):
        self.checkScript("numpy_basic_operation")


def main():
    # Slice command line arguments by '--'
    unittest_args, parser_args = sliceCommandLineArguments()
    # Construct and run unit tests.
    unittest.main(argv=unittest_args)


if __name__ == "__main__":
    main()
