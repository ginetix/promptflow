# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

# this file is different from other files in this folder
# functions (APIs) defined in this file follows OTLP 1.1.0
# https://opentelemetry.io/docs/specs/otlp/#otlphttp-request
# to provide OTLP/HTTP endpoint as OTEL collector

import logging
from typing import Callable, Optional

from flask import request
from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import ExportTraceServiceRequest

from promptflow._sdk._tracing import process_otlp_trace_request


def trace_collector(
    get_created_by_info_with_cache: Callable,
    logger: logging.Logger,
    cloud_trace_only: bool = False,
    credential: Optional[object] = None,
):
    """Collect traces from OTLP/HTTP endpoint and write to local/remote storage.

    This function is target to be reused in other places, so pass in get_created_by_info_with_cache and logger to avoid
    app related dependencies.

    :param get_created_by_info_with_cache: A function that retrieves information about the creator of the trace.
    :type get_created_by_info_with_cache: Callable
    :param logger: The logger object used for logging.
    :type logger: logging.Logger
    :param cloud_trace_only: If True, only write trace to cosmosdb and skip local trace. Default is False.
    :type cloud_trace_only: bool
    :param credential: The credential object used to authenticate with cosmosdb. Default is None.
    :type credential: Optional[object]
    """
    content_type = request.headers.get("Content-Type")
    # binary protobuf encoding
    if "application/x-protobuf" in content_type:
        trace_request = ExportTraceServiceRequest()
        trace_request.ParseFromString(request.data)
        process_otlp_trace_request(
            trace_request=trace_request,
            get_created_by_info_with_cache=get_created_by_info_with_cache,
            logger=logger,
            cloud_trace_only=cloud_trace_only,
            credential=credential,
        )
        return "Traces received", 200

    # JSON protobuf encoding
    elif "application/json" in content_type:
        raise NotImplementedError
