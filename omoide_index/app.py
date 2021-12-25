# -*- coding: utf-8 -*-
"""Index server.

This component encapsulate search logic inside.
Initially, all of it were placed inside application. But since it used
Gunicorn with four workers, total launch time started to grow. At some moment
server restart stated taking too long from Gunicorn point of view, so
application could not even start. Separate server makes possible to contain
index only in a single exemplar for any amount of workers and also can easily
make hot reload of the index without downtime.

There is a possibility of a race condition. Request can happen in the same
exact moment as index reload, this is considered as non critical situation.
On the next search request user will get new version of the content.
"""
from functools import partial

import fastapi

from omoide_index import domain
from omoide_index import infra
from omoide_index import use_cases
from omoide_index.version import __version__

INDEX = use_cases.CreateIndexOnStartUseCase().execute()

STATUS = use_cases.CreateStatusOnStartUseCase(
    index=INDEX,
    clock=infra.Clock(),
    memory_calculator=infra.MemoryCalculator(),
    version=__version__,
).execute()


def quietly_reload_index_on_start(index: domain.Index,
                                  status: domain.Status) -> None:
    """Initialize search index."""
    config = infra.Config()

    if config.is_on('OMOIDE_INDEX_RELOAD_ON_START'):
        use_cases.RebuildIndexUseCase(
            index=index,
            status=status,
            clock=infra.Clock(),
            memory_calculator=infra.MemoryCalculator(),
            version=__version__,
        ).execute()


app = fastapi.FastAPI(
    openapi_url=None,
    docs_url=None,
    redoc_url=None,
    on_startup=[
        partial(quietly_reload_index_on_start, INDEX, STATUS)
    ],
)


def get_status() -> domain.Status:
    """Get actual instance of the server status."""
    return STATUS


def get_index() -> domain.Index:
    """Get actual instance of the server index."""
    return INDEX


@app.get('/')
def healthcheck() -> dict[str, str]:
    """Return something that can be used as service health check."""
    return {'result': f'omoide-index {__version__}'}


@app.get('/status')
def describe_status(
        status: domain.Status = fastapi.Depends(get_status),
) -> domain.VerboseStatus:
    """Describe current state of the server.

    Example response:
    {
        "version": "2021.10.04",
        "server_last_restart": "2021-10-05 20:15:21+00:00",
        "server_uptime": "15s",
        "server_size": "99.6 MiB",
        "index_status": "active",
        "index_last_reload": "2021-10-05 20:15:24+00:00",
        "index_last_reload_duration": "3s",
        "index_uptime": "11s",
        "index_comment": "",
        "index_records": 19733,
        "index_buckets": 20289,
        "index_avg_bucket": 0.97,
        "index_min_bucket": 1,
        "index_max_bucket": 17846,
        "index_size": "46.8 MiB"
    }
    """
    use_case = use_cases.DescribeExistingStatusUseCase(
        status=status,
        clock=infra.Clock(),
        memory_calculator=infra.MemoryCalculator(),
    )
    return use_case.execute()


@app.get('/search')
def search_items_for_user(
        query: domain.Query,
        index: domain.Index = fastapi.Depends(get_index),
) -> domain.SearchResult:
    """Perform search on the in-memory database."""

    if query:
        result = use_cases.SearchRandomItemsUseCase(query, index).execute()
    else:
        result = use_cases.SearchSpecificItemsUseCase(query, index).execute()

    return result


@app.post('/reload')
def reload_index(
        index: domain.Index = fastapi.Depends(get_index),
        status: domain.Status = fastapi.Depends(get_status),
) -> domain.IndexActionModel:
    """Reload whole index silently, so users wont notice."""
    # TODO --------------------------------------------------------------------
    assert index
    assert status
    # TODO --------------------------------------------------------------------
    return domain.IndexActionModel(
        action='reloading index',
    )


@app.post('/refresh')
def partially_refresh_index(
        model: domain.IndexRefreshModel,
        index: domain.Index = fastapi.Depends(get_index),
        status: domain.Status = fastapi.Depends(get_status),
) -> domain.IndexActionModel:
    """Reload some parts of the index silently, so users wont notice."""
    # TODO --------------------------------------------------------------------
    assert model
    assert index
    assert status
    # TODO --------------------------------------------------------------------
    return domain.IndexActionModel(
        action='refreshing index',
    )


@app.post('/user')
def refresh_user(
        model: domain.RefreshUserModel,
        index: domain.Index = fastapi.Depends(get_index),
        status: domain.Status = fastapi.Depends(get_status),
) -> domain.UserActionModel:
    """Update or create records for this user."""
    # TODO --------------------------------------------------------------------
    assert index
    assert status
    # TODO --------------------------------------------------------------------
    return domain.UserActionModel(
        user_uuid=model.user_uuid,
        action='refreshing user',
    )


@app.delete('/user')
def drop_user(
        model: domain.DropUserModel,
        index: domain.Index = fastapi.Depends(get_index),
        status: domain.Status = fastapi.Depends(get_status),
) -> domain.UserActionModel:
    """Delete all records for this user."""
    # TODO --------------------------------------------------------------------
    assert index
    assert status
    # TODO --------------------------------------------------------------------
    return domain.UserActionModel(
        user_uuid=model.user_uuid,
        action='deleting user',
    )
