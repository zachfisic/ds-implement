# Implementing A Hash Table in Python

## Overview
Hash tables are one of the most useful data structures. Their quick and scalable insert, search and delete make them relevant to a large number of computer science problems. Features such as the dictionary in Python or the associative array in PHP are often implemented using a hash table. Even more straightforward is the HashTable class available in Java.

Why would we need such a structure? Well, sometimes a flat area just isn’t enough. To make sense of the problem at hand, you may need to store and access your data by a *key*, a definite step up from the rudimentary integer index provided by flat arrays.

Let’s look at the criteria for our hash table:
1. Insert data using an insert() method
2. Find data using find() method
3. Remove data with remove() method

The named keys we create for our hash table are converted to indices. These indices are used for storing and retrieving the data value from the hash table’s internal array.  These details will be hidden from the user - they just have to worry about insert(), find(), and remove().

```python
class HashTable:
	def __init__(self):
		self.capacity = INITIAL_CAP
		self.size = 0
		self.buckets = [None] * self.capacity
```

Our HashTable class needs a few fields to manage its elements…

1. *capacity*: this determines the size of our internal array. In a more complex hash table implementation (i.e. an open-addressed, double-hashed hash table), _it’s important that the capacity is prime, and that it can be changed_. On the other hand, our separate chaining hash table sets the capacity once and never changes it, regardless of how many elements are stored. This is good for simplicity, but bad for scalability.
2. *size*: the number of elements that have been inserted.
3. *buckets*: the internal array, where we store each inserted value based on the provided key.


## Collision Handling

Because the hash table uses separate chaining, each bucket will actually contain a LinkedList of nodes containing the objects stored at that index. This is one method of collision resolution. If the hash table just wrote the data into the location anyway, we would be losing the object that is already stored under a different key. With separate chaining, we create a LinkedList at each index of our buckets array, containing all keys for a given index. When we need to look up one of those items, we iterate the list until we find the Node matching the requested key.

There are other, far more efficient ways of handling collisions, but separate chaining is likely the simplest method.

```python
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
```

In a more complex hash table implementation (i.e. an open-addressed, double-hashed hash table), it’s important that the capacity is prime, and that it can be changed. On the other hand, our separate chaining hash table sets the capacity once and never changes it, regardless of how many elements are stored. This is good for simplicity, but bad for scalability.


## Producing the Index

Our hash method needs to take our key, which will be a string of any length, and produce an index for our internal buckets array. We will be creating a hash function to convert the string to an index. There are many properties of a good hash function, but for our purposes the most important characteristic for our function to have is *uniformity*. We want our hash values to be _as evenly distributed among our buckets as possible, to take full advantage of each bucket and avoid collisions_.

```
Bucket 1 => { key: ‘John’, value: 12 }, { key: 'Mary', value: '25' }
Bucket 2 => { key: ‘George’, value: 115 }, { key: 'Tom', value: '50' }
Bucket 3 => { key: ‘Hank’, value: 5 }, { key: 'Sam', value: '22' }
Bucket 4 => { key: ‘Jill’, value: 44 }, { key: 'Allie', value: '75' }
```

An uneven distribution will defeat the purpose of the hash table altogether, yielding nothing more than a bloated LinkedList. Consider an extreme case…

* Assume our hash function will be `h(x) = 1`. Each input produces the same constant value. So, every time we hash a key, the output is 1, meaning that we assign that node to bucket 1. The result would look something like this:

```
Bucket 1 => { key: ‘John’, value: 12 }, { key: 'Mary', value: '25' }, { key: ‘George’, value: 115 }, { key: 'Tom', value: '50' }, { key: ‘Hank’, value: 5 }, { key: 'Sam', value: '22' }, { key: ‘Jill’, value: 44 }, { key: 'Allie', value: '75' }
Bucket 2 => 
Bucket 3 =>
Bucket 4 =>
```

Our hash function must avoid this bottleneck and provide uniformity.

```python
def hash(self, key):
	hashsum = 0
	# For each character in the key...
	for idx, c in enumerate(key):
		# Add (index + length of key) ^ (current char code)
		hashsum += (idx + len(key)) ** ord(c)

		# Perform modulus to keep hashsum in range [0, self.capacity - 1]
		hashsum = hashsum % self.capacity
	return hashsum
```


## Creating the Methods

### Insert()

To insert a key/value pair into our hash table, we will follow these steps:
1. Increment size of hash table.
2. Compute index of key using hash function.
3. If the bucket at index is empty, create a new node and add it there.
4. Otherwise, a collision occurred: there is already a linked list of at least one node at this index. Iterate to the end of the list and add a new node there.

```python
def insert(self, key, value):

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
```


### Find()

We need a function to retrieve our stored data. To do this, we’ll perform the following steps:
1. Compute the index for the provided key using the hash function.
2. Go to the bucket for that index.
3. Iterate the nodes in that linked list until the key is found, or the end of the list is reached.
4. Return the value of the found node, or None if not found.

```python
def find(self, key):
	
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
```


### Remove()

Removing an element from a hash table is similar to removing an element from a linked list. This method will return the data value removed, or None if the requested node was not found.

1. Compute hash for the key to determine index.
2. Iterate linked list of nodes. Continue until end of list or until key is found.
3. If the key is not found, return None.
4. Otherwise, remove the node from the linked list and return the node value.

```python
def remove(self, key):

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
```
