# Julie Walin
# December, 2020

# Hash Table

# Create one entry for the hash table.
class HashTableEntry:
    def __init__(self, key, item):
        self.Key = key
        self.item = item


# This is a hash table.
class HashTable:
    def __init__(self):
        self.size = 40
        self.map = [None] * self.size

    def _get_hash(self, key):
        return int(key) % self.size

    # Insert a new entry aka a new package into the hash table  --->>O(1)
    def insert(self, key, value):
        key_hash = self._get_hash(key)
        key_value = [key, value]

        if self.map[key_hash] is None:
            self.map[key_hash] = list([key_value])
            return True
        else:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.map[key_hash].append(key_value)
            return True

    def update_value(self, key, value):
        key_hash = self._get_hash(key)
        if self.map[key_hash] is not None:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
        else:
            print('Error updating hash on key: ', key)

    # Lookup the package       --->> O(log n)
    def lookup_value(self, key):
        key_hash = self._get_hash(key)
        if self.map[key_hash] is not None:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    return pair[1]
        print('HashMap not found ', key)
        return None

    def delete(self, key):
        key_hash = self._get_hash(key)

        if self.map[key_hash] is None:
            return False
        for i in range (0, len(self.map[key_hash])):
            if self.map[key_hash][i][0] == key:
                self.map[key_hash].pop(i)
                return True
        return False

    def print(self):
        print('++++++++All Packages++++++++')
        for item in self.map:
            if item is not None:
                print(str(item))

