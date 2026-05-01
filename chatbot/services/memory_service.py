import re
from chatbot.models import UserMemory


class MemoryService:

    @staticmethod
    def extract_and_store(user, message):
        message_lower = message.lower()

        patterns = {
            "name": [
                r"my name is (.+)",
                r"mera naam (.+) hai"
            ],
            "age": [
                r"i am (\d+) years old",
                r"meri age (\d+)"
            ],
            "city": [
                r"i live in (.+)",
                r"mai (.+) me rehta"
            ]
        }

        for key, regex_list in patterns.items():
            for regex in regex_list:
                match = re.search(regex, message_lower)
                if match:
                    value = match.group(1).strip()

                    UserMemory.objects.update_or_create(
                        user=user,
                        key=key,
                        defaults={"value": value}
                    )

    @staticmethod
    def get_memory_context(user):
        memories = UserMemory.objects.filter(user=user)

        return "\n".join([
            f"{memory.key}: {memory.value}"
            for memory in memories
        ])
