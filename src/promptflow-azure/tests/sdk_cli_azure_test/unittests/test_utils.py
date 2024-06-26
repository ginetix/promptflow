# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from unittest.mock import MagicMock, patch

import pytest

from promptflow.exceptions import UserErrorException


@pytest.mark.unittest
class TestUtils:
    def test_url_parse(self):
        from promptflow.azure._utils._url_utils import BulkRunId, BulkRunURL

        flow_id = (
            "azureml://experiment/3e123da1-f9a5-4c91-9234-8d9ffbb39ff5/flow/"
            "0ab9d2dd-3bac-4b68-bb28-12af959b1165/bulktest/715efeaf-b0b4-4778-b94a-2538152b8766/"
            "run/f88faee6-e510-45b7-9e63-08671b30b3a2"
        )
        flow_id = BulkRunId(flow_id)
        assert flow_id.experiment_id == "3e123da1-f9a5-4c91-9234-8d9ffbb39ff5"
        assert flow_id.flow_id == "0ab9d2dd-3bac-4b68-bb28-12af959b1165"
        assert flow_id.bulk_test_id == "715efeaf-b0b4-4778-b94a-2538152b8766"

        flow_run_url = (
            "https://ml.azure.com/prompts/flow/3e123da1-f9a5-4c91-9234-8d9ffbb39ff5/"
            "0ab9d2dd-3bac-4b68-bb28-12af959b1165/bulktest/715efeaf-b0b4-4778-b94a-2538152b8766/"
            "details?wsid=/subscriptions/96aede12-2f73-41cb-b983-6d11a904839b/resourcegroups/promptflow/"
            "providers/Microsoft.MachineLearningServices/workspaces/promptflow-eastus"
        )
        flow_url = BulkRunURL(flow_run_url)
        assert flow_url.experiment_id == "3e123da1-f9a5-4c91-9234-8d9ffbb39ff5"
        assert flow_url.flow_id == "0ab9d2dd-3bac-4b68-bb28-12af959b1165"
        assert flow_url.bulk_test_id == "715efeaf-b0b4-4778-b94a-2538152b8766"

    def test_forbidden_new_caller(self):
        from promptflow.azure._restclient.flow_service_caller import FlowServiceCaller

        with pytest.raises(UserErrorException) as e:
            FlowServiceCaller(MagicMock(), MagicMock(), MagicMock())
        assert "_FlowServiceCallerFactory" in str(e.value)

    def test_user_specified_azure_cli_credential(self):
        from azure.identity import AzureCliCredential

        from promptflow._sdk._constants import EnvironmentVariables
        from promptflow.azure._cli._utils import get_credentials_for_cli

        with patch.dict("os.environ", {EnvironmentVariables.PF_USE_AZURE_CLI_CREDENTIAL: "true"}):
            cred = get_credentials_for_cli()
            assert isinstance(cred, AzureCliCredential)
