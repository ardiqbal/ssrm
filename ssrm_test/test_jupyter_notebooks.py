#     Copyright 2020 Optimizely Inc.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

import glob
import os
import shutil
from typing import Any, Union

import papermill as pm
import pytest

JUPYTER_NOTEBOOK_DIR: Union[bytes, str] = os.path.join(os.getcwd(), "notebooks")
INCLUDED_NOTEBOOK_GLOB = os.path.join(JUPYTER_NOTEBOOK_DIR, "*.ipynb")
JUPYTER_NOTEBOOK_TESTING_OUTPUT_DIR: Union[bytes, str] = os.path.join(
    os.getcwd(), "ssrm_test", "jupyter_notebook_testing_output"
)


@pytest.fixture
def generate_papermill_output_dir(tmpdir_factory: object) -> object:
    """Ensures directory exists for output notebooks. This is one of the
    required parameters for papermill.execute_notebook()
    """
    try:
        os.makedirs(JUPYTER_NOTEBOOK_TESTING_OUTPUT_DIR, exist_ok=True)
        yield JUPYTER_NOTEBOOK_TESTING_OUTPUT_DIR

        # Teardown: delete testing output dir.
        shutil.rmtree(JUPYTER_NOTEBOOK_TESTING_OUTPUT_DIR)
    except OSError as err:
        raise err


def test_all_jupyter_notebook(generate_papermill_output_dir, caplog):
    caplog.set_level("INFO", logger="papermill")
    for notebook_file_path in glob.glob(INCLUDED_NOTEBOOK_GLOB):
        this_notebook_file_name: Union[Union[bytes, str], Any] = os.path.basename(
            notebook_file_path
        )
        output_file_path = os.path.join(
            generate_papermill_output_dir, this_notebook_file_name
        )
        pm.execute_notebook(
            notebook_file_path,
            output_file_path,
            cwd=JUPYTER_NOTEBOOK_DIR,
            log_output=True,
        )
