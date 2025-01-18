from typing import Any, Dict, Optional

from crewai.memory import EntityMemory, LongTermMemory, ShortTermMemory, UserMemory


class ContextualMemory:
    def __init__(
        self,
        memory_config: Optional[Dict[str, Any]],
        stm: ShortTermMemory,
        ltm: LongTermMemory,
        em: EntityMemory,
        um: UserMemory,
    ):
        if memory_config is not None:
            self.memory_provider = memory_config.get("provider")
        else:
            self.memory_provider = None
        self.stm = stm
        self.ltm = ltm
        self.em = em
        self.um = um

    def build_context_for_task(self, task, context) -> str:
        """
        Automatically builds a minimal, highly relevant set of contextual information
        for a given task.
        """
        query = f"{task.description} {context}".strip()
        if not query:
            return ""

        context_data = []

        ltm_data = self._fetch_ltm_context(task.description)
        if ltm_data:
            context_data.append(ltm_data)

        stm_data = self._fetch_stm_context(query)
        if stm_data:
            context_data.append(stm_data)

        entity_data = self._fetch_entity_context(query)
        if entity_data:
            context_data.append(entity_data)

        if self.memory_provider == "mem0":
            user_data = self._fetch_user_context(query)
            if user_data:
                context_data.append(user_data)

        return "\n".join(context_data)

    def _fetch_stm_context(self, query) -> str:
        """
        Fetches recent relevant insights from STM related to the task's description and expected_output,
        formatted as bullet points.
        """
        stm_results = self.stm.search(query)
        if not stm_results:
            return ""

        if self.memory_provider == "mem0":
            formatted_results = "\n".join(
                f"- {result['memory']}" for result in stm_results
            )
        else:
            formatted_results = "\n".join(
                f"- {result['context']}" for result in stm_results
            )

        return f"Recent Insights:\n{formatted_results}"

    def _fetch_ltm_context(self, task) -> Optional[str]:
        """
        Fetches historical data or insights from LTM that are relevant to the task's description and expected_output,
        formatted as bullet points.
        """
        ltm_results = self.ltm.search(task, latest_n=2)
        if not ltm_results:
            return None

        suggestions = set()
        for result in ltm_results:
            suggestions.update(result.get("metadata", {}).get("suggestions", []))

        if not suggestions:
            return None

        formatted_results = "\n".join(f"- {suggestion}" for suggestion in suggestions)
        return f"Historical Data:\n{formatted_results}"

    def _fetch_entity_context(self, query) -> str:
        """
        Fetches relevant entity information from Entity Memory related to the task's description and expected_output,
        formatted as bullet points.
        """
        em_results = self.em.search(query)
        if not em_results:
            return ""

        if self.memory_provider == "mem0":
            formatted_results = "\n".join(
                f"- {result['memory']}" for result in em_results
            )
        else:
            formatted_results = "\n".join(
                f"- {result['context']}" for result in em_results
            )

        return f"Entities:\n{formatted_results}"

    def _fetch_user_context(self, query: str) -> str:
        """
        Fetches and formats relevant user information from User Memory.
        Args:
            query (str): The search query to find relevant user memories.
        Returns:
            str: Formatted user memories as bullet points, or an empty string if none found.
        """
        user_memories = self.um.search(query)
        if not user_memories:
            return ""

        formatted_memories = "\n".join(
            f"- {result['memory']}" for result in user_memories
        )
        return f"User memories/preferences:\n{formatted_memories}"
