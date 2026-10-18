import json
import os
import random


class Chain:
    def __init__(self, base_path: str = "data", start_word_type: str = "freq") -> None:
        self.chains: dict[str, dict[str, dict[str, int]]] = {}
        self.base_path = base_path
        self.start_word_type = start_word_type

    def get_chain(self, guild_id: str) -> dict[str, dict[str, int]]:
        if guild_id not in self.chains:
            self.load(guild_id)

        return self.chains[guild_id]

    def process_words(self, words: list[str], guild_id: str) -> None:
        if not words:
            return

        chain = self.get_chain(guild_id)

        for i, word in enumerate(words):
            if not word.strip() or word == "__START__" or word == "__END__":
                continue

            if not word in chain:
                chain[word] = {}

            if i == 0:
                chain["__START__"][word] = chain["__START__"].get(word, 0) + 1

            if i < len(words) - 1:
                next_word = words[i + 1]
                chain[word][next_word] = chain[word].get(next_word, 0) + 1
            else:
                chain[word]["__END__"] = chain[word].get("__END__", 0) + 1

        self.save(guild_id, chain)

    def generate_message(self, max_length: int, guild_id: str) -> str:
        self.load(guild_id)
        chain = self.get_chain(guild_id)

        if max_length < 1:
            raise ValueError("max_length must be at least 1")

        start_choices = chain.get("__START__", {})
        if not start_choices:
            raise ValueError("The word chain is empty")

        if self.start_word_type == "freq":
            first_word = random.choices(
                list(start_choices.keys()),
                weights=list(start_choices.values()),
                k=1,
            )[0]
        elif self.start_word_type == "random":
            words = list(chain.keys())
            words.remove("__START__")
            first_word = random.choice(words)
        else:
            raise ValueError("start_word_type must be either freq or random")

        message = [first_word]
        max_steps = 100

        for _ in range(max_steps):
            current_word = message[-1]
            next_choices = chain.get(current_word, {})

            if not next_choices:
                break

            next_word = random.choices(
                list(next_choices),
                weights=list(next_choices.values()),
                k=1,
            )[0]

            if next_word == "__END__" or next_word in message:
                break

            message.append(next_word)
        else:
            raise RuntimeError(f"Generation exceeded {max_steps} steps")

        if len(message) > max_length:
            left = (max_length + 1) // 2
            right = max_length // 2
            message = message[:left] + (message[-right:] if right else [])

        return " ".join(message)

    def get_words_count(self, guild_id: str) -> int:
        self.load(guild_id)
        chain = self.get_chain(guild_id)
        return len(chain) - 1

    def get_links_count(self, guild_id: str) -> int:
        self.load(guild_id)
        chain = self.get_chain(guild_id)
        return sum(len(inner) for inner in chain.values())

    def save(self, guild_id: str, chain: dict[str, dict[str, int]]) -> None:
        path = f"{self.base_path}/{guild_id}/words.json"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf8") as f:
            json.dump(chain, f, indent=2, ensure_ascii=False)

    def load(self, guild_id: str) -> None:
        path = f"{self.base_path}/{guild_id}/words.json"

        if not os.path.isfile(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            chain = {"__START__": {}}
            self.save(guild_id, chain)
        else:
            with open(path, "r", encoding="utf8") as f:
                chain = json.load(f)

        self.chains[guild_id] = chain
