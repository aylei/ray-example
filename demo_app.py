"""A Ray Serve LLM application, shaped as an application builder.

Ray Serve resolves an application from an import path of the form
``module:attribute``. When the attribute is callable it is a *builder*: Ray
hands it the application's ``args`` as a single argument and expects an
``Application`` back. That is the contract this module implements, and the
same one ``serveConfigV2`` uses.

``build_openai_app`` does the real work; the wrapper exists so the import
comes from this file, which is how a deployment proves its ``working_dir``
was fetched and put on the path.
"""

import logging

from ray.serve.llm import build_openai_app

logger = logging.getLogger('ray.serve')


def build_app(args):
    """Build the OpenAI-compatible application from ``args``.

    ``args`` is the ``llm_serving_args`` mapping: ``{"llm_configs": [...]}``.
    """
    configs = args.get('llm_configs', []) if isinstance(args, dict) else []
    logger.info('demo_app.build_app: %d LLM config(s) from working_dir', len(configs))
    return build_openai_app(args)
