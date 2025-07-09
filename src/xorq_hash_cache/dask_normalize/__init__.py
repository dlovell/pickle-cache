import dask

import xorq_hash_cache.dask_normalize.dask_normalize_function  # noqa: F401
import xorq_hash_cache.dask_normalize.dask_normalize_other  # noqa: F401


dask.config.set({"tokenize.ensure-deterministic": True})


@dask.base.normalize_token.register(object)
def raise_generic_object(obj):
    if hasattr(obj, "__dask_tokenize__"):
        return dask.base.normalize_token((type(obj), obj.__dask_tokenize__()))
    else:
        raise ValueError(f"Object {obj!r} cannot be deterministically hashed")
