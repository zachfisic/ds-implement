INITIAL_CAP = 50

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

# Hash table with chaining

class HashTable:
    def __init__(self):
        self.capacity = INITIAL_CAP # define the size of our internal array
        self.size = 0 # monitor the number of elements that have been inserted into the table
        self.buckets = [None] * self.capacity # the internal array, where we store each inserted value based on the provided key.

    def insert(self, key, value):
        """Inserts a value at a provided key

        :param key: The identifier for the node
        :type key: str
        :param value: The value for the new node
        :type value: str
        :returns: None
        :rtype: None
        """
        # increment the size
        self.size += 1

        # compute the index
        index = self.hash(key)

        # go to the node corresponding to the hash
        node = self.buckets[index]

        # if the bucket is empty...
        if node is None:
            # create our node, add it and return
            self.buckets[index] = Node(key, value)
            return

        # we have a collision! Iterate to the end of the linked list at provided index
        prev = node
        while node is not None:
            prev = node
            node = node.next
        # add a new node at the end of the list with provided key/value
        prev.next = Node(key, value)

    def find(self, key):
        """Finds the value at a provided key, if it exists.

        :param key: The identifier for the node
        :type key: str
        :returns: value of node if it exists
        :rtype: str | None
        """
        # compute hash
        index = self.hash(key)

        # go to first node in list at bucket
        node = self.buckets[index]

        # traverse the linked list at this node
        while node is not None and node.key != key:
            node = node.next

        # node is now the requested key/value pair or None
        if node is None:
            return None
        else:
            return node.value


    def remove(self, key):
        """Removes the node if it exists.

        :param key: The identifier for the node to remove from the hash table
        :type key: str
        :returns: value of removed node if it exists
        :rtype: str | None
        """
  
        # compute the hash
        index = self.hash(key)

        node = self.buckets[index]
        prev = None

        # iterate to the requested node
        while node is not None and node.key != key:
            prev = node
            node = node.next

        # node is now either the requested node or none
        if node is None:
            return None
        else:
            # decrement the size
            self.size -= 1

            result = node.value

            # delete the element in the linked list
            if prev is None:
                node = None
            else:
                prev.next = prev.next.next

            # return the deleted element
            return result