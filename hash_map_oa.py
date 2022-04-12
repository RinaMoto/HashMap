# Name: Rina Easterday
# Description: Complete the HashMap implementations using Open Addressing and Quadratic Probing


from a6_include import *


class HashEntry:

    def __init__(self, key: str, value: object):
        """
        Initializes an entry for use in a hash map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.key = key
        self.value = value
        self.is_tombstone = False

    def __str__(self):
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return f"K: {self.key} V: {self.value} TS: {self.is_tombstone}"


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses Quadratic Probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()

        for _ in range(capacity):
            self.buckets.append(None)

        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            out += str(i) + ': ' + str(self.buckets[i]) + '\n'
        return out

    def clear(self) -> None:
        """
        This method clears the HashMap
        :return: None
        """

        # iterate through the HashMap and set value to None for the buckets with a key/value pair
        for i in range(self.capacity):
            if self.buckets.get_at_index(i) is not None:
                self.buckets.set_at_index(i, None)
        self.size = 0

    def get(self, key: str) -> object:
        """
        This method takes the given key and returns the associated value if it exists in the HashMap
        otherwise returns None
        :param key: string
        :return: an object
        """

        # find the index value and store the initial index value
        hash_key = self.hash_function(key)
        index = hash_key % self.capacity
        initial = index

        # find the key/value pair at the index. If the given key matches the key then return its value. Otherwise,
        # use quadratic probing until matching key is found or return None if not found.
        for j in range(self.capacity):
            if self.buckets.get_at_index(index) is None:
                return None
            elif self.buckets.get_at_index(index).key == key and self.buckets.get_at_index(index).is_tombstone is False:
                return self.buckets.get_at_index(index).value
            else:
                index = (initial + (j ** 2)) % self.capacity

    def put(self, key: str, value: object) -> None:
        """
        This method adds the key/value pair in the hashMap. If given key already exists, its associated value
        gets replaced.
        :param key: string
        :param value: object
        :return: None
        """

        # if the load factor is greater than or equal to 0.5, resize the table
        if self.table_load() >= 0.5:
            self.resize_table(self.capacity * 2)

        # find the index value and store the initial index value
        hash_key = self.hash_function(key)
        index = hash_key % self.capacity
        initial = index

        # assign the given key/value pair to the index if it is empty or has a tombstone value. Override the value
        # if the given key matches the existing key. Otherwise, use quadratic probing to find an empty bucket.
        for j in range(self.capacity):
            if self.buckets.get_at_index(index) is None:
                node = HashEntry(key, value)
                self.buckets.set_at_index(index, node)
                self.size += 1
                break

            elif self.buckets.get_at_index(index).key == key:
                node = HashEntry(key, value)
                self.buckets.set_at_index(index, node)
                break

            elif self.buckets.get_at_index(index).is_tombstone is True:
                node = HashEntry(key, value)
                self.buckets.set_at_index(index, node)
                self.size += 1
                break

            else:
                index = (initial + (j**2)) % self.capacity


    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value by updating its tombstone value to True. If
        the given key is not found, this method does nothing.
        :param key: string
        :return: None
        """

        # find the index value and store the initial index value
        hash_key = self.hash_function(key)
        index = hash_key % self.capacity
        initial = index

        # if the key at the index matches the given key and the tombstone value is False,
        # remove the key/value pair by assigning the tombstone variable to True. Otherwise use quadratic probing
        for j in range(self.capacity):
            if self.buckets.get_at_index(index) is None:
                break
            elif self.buckets.get_at_index(index).key == key and self.buckets.get_at_index(index).is_tombstone is False:
                self.buckets.get_at_index(index).is_tombstone = True
                self.size -= 1
                break
            else:
                index = (initial + (j ** 2)) % self.capacity

    def contains_key(self, key: str) -> bool:
        """
        This method returns True if given key is in the HashMap. Otherwise, this method returns False
        :param key: string
        :return: boolean
        """

        # base case
        if self.size == 0:
            return False

        # find the index value and store the initial index value
        hash_key = self.hash_function(key)
        index = hash_key % self.capacity
        initial = index

        # return True if existing key matches given key. Return False if the bucket at the index is empty or has a
        # tombstone value of True. Otherwise, use quadratic probing to find the index with the matching key.
        for j in range(self.capacity):
            if self.buckets.get_at_index(index) is None:
                return False
            elif self.buckets.get_at_index(index).is_tombstone is True:
                return False
            elif self.buckets.get_at_index(index).key == key:
                return True
            else:
                index = (initial + j ** 2) % self.capacity

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the HashMap
        :return: integer
        """
        return self.capacity - self.size

    def table_load(self) -> float:
        """
        This method returns the current Hash Table load factor
        :return: float
        """
        return self.size / self.capacity


    def resize_table(self, new_capacity: int) -> None:
        """
        This method changes the Hash table capacity. The existing key / value pairs are rehashed and
        added to the new Hash table. If the new_capacity is less than 1, this method does nothing
        :param new_capacity: integer
        :return: None
        """

        # base case
        if new_capacity < 1 or new_capacity < self.size:
            return

        # create new hash map
        new_hash = HashMap(new_capacity, self.hash_function)

        # rehash the non-deleted key/value pairs in the existing hash table and add them to the new hash
        for i in range(self.capacity):
            if self.size == 0:
                break
            if self.buckets.get_at_index(i) is not None and self.buckets.get_at_index(i).is_tombstone is False:
                new_hash.put(self.buckets.get_at_index(i).key, self.buckets.get_at_index(i).value)

        self.capacity = new_hash.capacity
        self.buckets = new_hash.buckets

    def get_keys(self) -> DynamicArray:
        """
        This method returns a Dynamic Array with all the keys stored in the HashMap.
        :return: DynamicArray
        """
        all_keys = DynamicArray()

        # iterate through the Hashmap and append each key value to the array
        for i in range(self.capacity):
            if self.buckets.get_at_index(i) is not None and self.buckets.get_at_index(i).is_tombstone is False:
                all_keys.append(self.buckets.get_at_index(i).key)

        return all_keys


if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    # this test assumes that put() has already been correctly implemented
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):

        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
