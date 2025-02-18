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
    # Retrieve model names and API base URL from the environment efficiently
    model_name = (
        os.getenv("OPENAI_MODEL_NAME") or os.getenv("MODEL") or DEFAULT_LLM_MODEL
    )
    base_url = os.getenv("OPENAI_API_BASE") or os.getenv("OPENAI_BASE_URL")

    # Initialize llm_params dictionary with given defaults
    llm_params: Dict[str, Any] = {
        "model": model_name,
        "base_url": base_url,
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
                        env_value = os.getenv(key_name)
                        if env_value:
                            # Map environment variable names to recognized parameters
                            param_key = _normalize_key_name(key_name.lower())
                            llm_params[param_key] = env_value
                    elif env_var.get("default", False):
                        for key, value in env_var.items():
                            if (
                                key not in {"prompt", "key_name", "default"}
                                and value is not None
                            ):
                                llm_params[key.lower()] = value
        else:
            print(
                f"Expected env_vars_for_provider to be a list or tuple, but got {type(env_vars_for_provider)}"
            )

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
    for pattern in LITELLM_PARAMS:
        if pattern in key_name:
            return pattern
    return key_name
