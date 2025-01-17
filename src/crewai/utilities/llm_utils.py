import os
from typing import Any, Dict, Optional, Union

from crewai.cli.constants import DEFAULT_LLM_MODEL, ENV_VARS, LITELLM_PARAMS
from crewai.llm import LLM


def create_llm(
    llm_value: Union[str, LLM, Any, None] = None,
) -> Optional[LLM]:
    """
    Creates or returns an LLM instance based on the given llm_value.

    Args:
        llm_value (str | LLM | Any | None):
            - str: The model name (e.g., "gpt-4").
            - LLM: Already instantiated LLM, returned as-is.
            - Any: Attempt to extract known attributes like model_name, temperature, etc.
            - None: Use environment-based or fallback default model.

    Returns:
        An LLM instance if successful, or None if something fails.
    """

    # 1) If llm_value is already an LLM object, return it directly
    if isinstance(llm_value, LLM):
        return llm_value

    # 2) If llm_value is a string (model name)
    if isinstance(llm_value, str):
        try:
            created_llm = LLM(model=llm_value)
            return created_llm
        except Exception as e:
            print(f"Failed to instantiate LLM with model='{llm_value}': {e}")
            return None

    # 3) If llm_value is None, parse environment variables or use default
    if llm_value is None:
        return _llm_via_environment_or_fallback()

    # 4) Otherwise, attempt to extract relevant attributes from an unknown object
    try:
        # Extract attributes with explicit types
        model = (
            getattr(llm_value, "model_name", None)
            or getattr(llm_value, "deployment_name", None)
            or str(llm_value)
        )
        temperature: Optional[float] = getattr(llm_value, "temperature", None)
        max_tokens: Optional[int] = getattr(llm_value, "max_tokens", None)
        logprobs: Optional[int] = getattr(llm_value, "logprobs", None)
        timeout: Optional[float] = getattr(llm_value, "timeout", None)
        api_key: Optional[str] = getattr(llm_value, "api_key", None)
        base_url: Optional[str] = getattr(llm_value, "base_url", None)

        created_llm = LLM(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            logprobs=logprobs,
            timeout=timeout,
            api_key=api_key,
            base_url=base_url,
        )
        return created_llm
    except Exception as e:
        print(f"Error instantiating LLM from unknown object type: {e}")
        return None


def _llm_via_environment_or_fallback() -> Optional[LLM]:
    """
    Helper function: if llm_value is None, we load environment variables or fallback default model.
    """
    model_name = os.environ.get(
        "OPENAI_MODEL_NAME", os.environ.get("MODEL", DEFAULT_LLM_MODEL)
    )

    # Initialize llm_params dictionary with default None values
    llm_params: Dict[str, Any] = {
        "model": model_name,
        "temperature": None,
        "max_tokens": None,
        "max_completion_tokens": None,
        "logprobs": None,
        "timeout": None,
        "api_key": None,
        "base_url": os.environ.get(
            "OPENAI_API_BASE", os.environ.get("OPENAI_BASE_URL")
        ),
        "api_version": None,
        "presence_penalty": None,
        "frequency_penalty": None,
        "top_p": None,
        "n": None,
        "stop": None,
        "logit_bias": None,
        "response_format": None,
        "seed": None,
        "top_logprobs": None,
        "callbacks": [],
    }

    UNACCEPTED_ATTRIBUTES = {
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_REGION_NAME",
    }

    set_provider = model_name.split("/")[0] if "/" in model_name else "openai"

    if set_provider in ENV_VARS:
        env_vars_for_provider = ENV_VARS[set_provider]
        if isinstance(env_vars_for_provider, (list, tuple)):
            for env_var in env_vars_for_provider:
                if isinstance(env_var, dict):
                    key_name = env_var.get("key_name")
                    if key_name and key_name not in UNACCEPTED_ATTRIBUTES:
                        env_value = os.environ.get(key_name)
                        if env_value:
                            # Map environment variable names to recognized parameters
                            param_key = _normalize_key_name(key_name.lower())
                            llm_params[param_key] = env_value
                    elif env_var.get("default", False):
                        llm_params.update(
                            {
                                k.lower(): v
                                for k, v in env_var.items()
                                if k not in {"prompt", "key_name", "default"}
                            }
                        )
                else:
                    print(
                        f"Expected env_var to be a dictionary, but got {type(env_var)}"
                    )

    # Remove None values
    llm_params = {k: v for k, v in llm_params.items() if v is not None}

    # Try creating the LLM
    try:
        new_llm = LLM(**llm_params)
        return new_llm
    except Exception as e:
        print(
            f"Error instantiating LLM from environment/fallback: {type(e).__name__}: {e}"
        )
        return None


def _normalize_key_name(key_name: str) -> str:
    """
    Maps environment variable names to recognized litellm parameter keys,
    using patterns from LITELLM_PARAMS.
    """
    return next(
        (pattern for pattern in LITELLM_PARAMS if pattern in key_name), key_name
    )
