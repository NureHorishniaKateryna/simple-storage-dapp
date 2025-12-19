import hashlib
import json
import time


class Block:
    """
    Клас блоку.
    Містить номер, мітку часу, дані транзакції,
    хеш попереднього блоку, nonce і власний хеш.
    """

    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self):
        """
        Обчислення SHA-256 хешу блоку.
        Хешує словник зі всіма полями (index, timestamp, data, previous_hash, nonce).
        """
        block_dict = {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }
        block_string = json.dumps(block_dict, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


class Blockchain:
    """
    Клас блокчейну, що містить список блоків
    та реалізує алгоритм Proof-of-Work.
    """

    difficulty = 4  # Кількість нулів, з яких має починатися хеш

    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Створення генезис-блоку — першого блоку в ланцюгу.
        """
        genesis_block = Block(0, {"message": "Genesis block"}, "0")
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        """
        Реалізація алгоритму Proof of Work.
        Змінює nonce, поки хеш не починатиметься з difficulty нулів.
        """
        prefix = "0" * self.difficulty

        while not block.hash.startswith(prefix):
            block.nonce += 1
            block.hash = block.compute_hash()

        return block.hash

    def add_block(self, data):
        """
        Створення нового блоку та його додавання до блокчейну.
        """
        new_block = Block(len(self.chain), data, self.last_block.hash)
        self.proof_of_work(new_block)
        self.chain.append(new_block)
        return new_block

    def is_valid(self):
        """
        Перевірка цілісності всього ланцюжка.
        """
        prefix = "0" * self.difficulty

        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Перевірка коректності хеша
            if current.hash != current.compute_hash():
                return False

            # Перевірка зв'язку між блоками
            if current.previous_hash != previous.hash:
                return False

            # Перевірка Proof of Work
            if not current.hash.startswith(prefix):
                return False

        return True


if __name__ == "__main__":
    blockchain = Blockchain()

    print("\nДодаємо блок 1...")
    blockchain.add_block({"from": "Alice", "to": "Bob", "amount": 10})

    print("\nДодаємо блок 2...")
    blockchain.add_block({"from": "Bob", "to": "Charlie", "amount": 5})

    print("\n--- Вивід блоків ---\n")
    for block in blockchain.chain:
        print(f"Блок {block.index}")
        print(f"Час: {block.timestamp}")
        print(f"Дані: {block.data}")
        print(f"Попередній хеш: {block.previous_hash}")
        print(f"Nonce: {block.nonce}")
        print(f"Хеш: {block.hash}")
        print("-" * 40)

    print("\nЦілісність ланцюжка:", blockchain.is_valid())

    print("\n--- Перевірка незмінності блокчейну ---")
    blockchain.chain[1].data["amount"] = 999  # штучна зміна даних
    print("Цілісність після зміни даних:", blockchain.is_valid())
