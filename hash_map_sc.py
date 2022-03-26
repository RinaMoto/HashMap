# Name: Rina Easterday
# OSU Email: Easterdr@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 7
# Due Date: 3/11/22
# Description: Complete the HashMap implementations using Linked Lists


from a6_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
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
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        This method removes all the key/value pairs in the HashMap
        :return: None
        """

        # iterate though the HashMap and if there is a chain of key/value pairs at the index, assign the value to None
        for i in range(self.capacity):
            value_chain = self.buckets.get_at_index(i)
            while value_chain.length() > 0:
                node = value_chain.head
                value_chain.remove(node.key)

        self.size = 0


    def get(self, key: str) -> object:
        """
        This method returns the value associated with the given key. Returns None if key/value pair does
        not exist
        :param key: string value
        :return: object: value of key/value pair
        """

        # find the index in HashMap for storing value
        hash_key = self.hash_function(key)
        index = hash_key % self.capacity

        # find chain of key/value pairs for the index and if it contains the given key
        value_chain = self.buckets.get_at_index(index)
        find = value_chain.contains(key)

        # return its value if key is in the value chain
        if find is not None:
            return find.value

        return None


    def put(self, key: str, value: object) -> None:
        """
        Add the key/value pair in the Hashmap. If key already exists, replace its value
        :param key: string value
        :param value: object
        :return: None
        """

        # find the index in HashMap for storing value
        hash_key = self.hash_function(key)
        index = hash_key % self.capacity

        # find chain of key/value pairs for the index and if it contains the given key
        value_chain = self.buckets.get_at_index(index)
        find = value_chain.contains(key)

        # if key does not exist, insert key/value pair in the HashMap
        # otherwise overwrite the old value with the new value
        if not find:
            value_chain.insert(key, value)
            self.size += 1
        else:
            find.value = value



    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the hashMap. If key doesn't exist in the HashMap
        this method does nothing.
        :param key: string value
        :return: None
        """

        if self.contains_key(key):
            # find the index in HashMap for storing value
            hash_key = self.hash_function(key)
            index = hash_key % self.capacity

            # find chain of key/value pairs for the index
            value_chain = self.buckets.get_at_index(index)

            value_chain.remove(key)
            self.size -= 1


    def contains_key(self, key: str) -> bool:
        """
        if key is found in given HashMap this method returns True. Otherwise, returns False
        :param key: string value
        :return: Boolean: whether the key is in the hashmap
        """
        # base case
        if self.size == 0:
            return False

        # find the index in HashMap where value may be stored
        hash_key = self.hash_function(key)
        index = hash_key % self.capacity

        # find chain of key/value pairs for the index and if it contains the given key
        value_chain = self.buckets.get_at_index(index)
        find = value_chain.contains(key)

        # if key is contained in chain of key/value pairs return True. Otherwise, return False
        if find:
            return True
        else:
            return False



    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the HashMap
        :return: int: number of empty buckets
        """
        empty = 0
        for i in range(self.capacity):
            if self.buckets.get_at_index(i).length() == 0:
                empty += 1

        return empty


    def table_load(self) -> float:
        """
        This method returns the current HashTable load factor
        :return: float: table load factor
        """
        return self.size / self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        This method resizes the HashMap to the new capacity size. It rehashes the existing key/value pairs and adds it
        to the new HashMap
        :param new_capacity: int
        :return: None
        """
        # base case: method does nothing if new capacity is less than 1
        if new_capacity < 1:
            return

        # create new HashMap
        new_hash = HashMap(new_capacity, self.hash_function)

        # iterate through the old HashMap and rehash all key/value pairs
        # and add it to the new HashMap
        for i in range(self.capacity):
            if self.size == new_hash.size:
                break

            value_chain = self.buckets.get_at_index(i)
            cur = value_chain.head
            while cur is not None:
                new_hash.put(cur.key, cur.value)
                cur = cur.next

        self.capacity = new_capacity
        self.buckets = new_hash.buckets


    def get_keys(self) -> DynamicArray:
        """
        This method returns a DynamicArray with all the key values in the HashMap
        :return: DynamicArray with key values
        """
        count = DynamicArray()

        # iterate through the Hashmap and append all key values to the dynamic array
        for i in range(self.capacity):
            value_chain = self.buckets.get_at_index(i)

            cur = value_chain.head
            while cur is not None:
                count.append(cur.key)
                cur = cur.next

        return count




# BASIC TESTING
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
