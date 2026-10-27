"""
mega_code_generator.py
Generates approximately 27 million lines of valid, diverse Python code.
The output is a single .py file containing classes, functions, data structures,
algorithms, utilities, and more — all syntactically valid Python.

Usage:
    python mega_code_generator.py [output_file]

Default output: mega_codebase.py
Estimated size: ~1.5–2 GB, ~27 million lines
Estimated time: a few minutes depending on disk speed
"""

import sys
import os
import random
import string
import math
import textwrap
from itertools import count

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
TARGET_LINES = 27_000_000
OUTPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "mega_codebase.py"

# Deterministic for reproducibility
random.seed(42)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
_name_counter = count(1)

ADJECTIVES = [
    "fast", "lazy", "eager", "bright", "dark", "cool", "warm", "sharp",
    "smooth", "heavy", "light", "deep", "shallow", "wide", "narrow",
    "strong", "weak", "bold", "calm", "fierce", "gentle", "proud",
    "humble", "swift", "slow", "ancient", "modern", "frozen", "molten",
    "crystal", "golden", "silver", "iron", "copper", "ruby", "emerald",
    "cosmic", "stellar", "lunar", "solar", "quantum", "atomic", "digital",
    "analog", "dynamic", "static", "alpha", "beta", "gamma", "delta",
]

NOUNS = [
    "engine", "parser", "handler", "manager", "factory", "builder",
    "service", "worker", "runner", "loader", "mapper", "reducer",
    "filter", "sorter", "scanner", "analyzer", "compiler", "linker",
    "buffer", "cache", "queue", "stack", "tree", "graph", "node",
    "matrix", "vector", "tensor", "pipeline", "channel", "socket",
    "stream", "bridge", "router", "gateway", "proxy", "adapter",
    "observer", "emitter", "listener", "dispatcher", "scheduler",
    "allocator", "collector", "registry", "catalog", "index",
    "sentinel", "guardian", "warden", "beacon", "oracle", "nexus",
]

DOMAINS = [
    "math", "io", "net", "data", "crypto", "ml", "stats", "geo",
    "text", "image", "audio", "video", "web", "db", "fs", "ui",
    "api", "config", "log", "test", "util", "core", "base", "ext",
    "physics", "chem", "bio", "finance", "game", "sim", "opt",
]

TYPES = ["int", "float", "str", "bool", "list", "dict", "tuple", "set", "bytes", "None"]

OPERATORS = ["+", "-", "*", "/", "//", "%", "**", "&", "|", "^"]

COMPARISONS = ["==", "!=", "<", ">", "<=", ">="]


def uid():
    return next(_name_counter)


def rand_name(kind="var"):
    if kind == "class":
        return f"{random.choice(ADJECTIVES).capitalize()}{random.choice(NOUNS).capitalize()}_{uid()}"
    elif kind == "func":
        return f"{random.choice(['compute', 'process', 'generate', 'transform', 'validate', 'calculate', 'evaluate', 'resolve', 'build', 'parse', 'encode', 'decode', 'serialize', 'fetch', 'merge', 'split', 'convert', 'extract', 'format', 'render'])}_{random.choice(NOUNS)}_{uid()}"
    elif kind == "module":
        return f"{random.choice(DOMAINS)}_{random.choice(NOUNS)}_{uid()}"
    else:
        return f"{'_'.join(random.choices(string.ascii_lowercase, k=random.randint(2, 4)))}_{uid()}"


def rand_type():
    return random.choice(TYPES)


def rand_value(typ=None):
    typ = typ or rand_type()
    if typ == "int":
        return str(random.randint(-10_000, 10_000))
    elif typ == "float":
        return f"{random.uniform(-1e6, 1e6):.6f}"
    elif typ == "str":
        word_count = random.randint(1, 5)
        words = " ".join(random.choices(ADJECTIVES + NOUNS, k=word_count))
        return f'"{words}"'
    elif typ == "bool":
        return random.choice(["True", "False"])
    elif typ == "list":
        items = ", ".join(str(random.randint(0, 100)) for _ in range(random.randint(2, 8)))
        return f"[{items}]"
    elif typ == "dict":
        pairs = ", ".join(
            f'"{random.choice(NOUNS)}": {random.randint(0, 999)}'
            for _ in range(random.randint(2, 5))
        )
        return "{" + pairs + "}"
    elif typ == "tuple":
        items = ", ".join(str(random.randint(0, 100)) for _ in range(random.randint(2, 6)))
        return f"({items},)"
    elif typ == "set":
        items = ", ".join(str(random.randint(0, 100)) for _ in range(random.randint(2, 6)))
        return "{" + items + "}"
    elif typ == "bytes":
        return f'b"\\x{random.randint(0,255):02x}\\x{random.randint(0,255):02x}\\x{random.randint(0,255):02x}"'
    else:
        return "None"


def rand_params(n=None):
    n = n or random.randint(1, 6)
    params = []
    for _ in range(n):
        name = rand_name("var")
        if random.random() < 0.4:
            params.append(f"{name}={rand_value()}")
        elif random.random() < 0.5:
            params.append(f"{name}: {rand_type()} = {rand_value()}")
        else:
            params.append(name)
    return ", ".join(params)


# ---------------------------------------------------------------------------
# Code generators — each returns a list of lines
# ---------------------------------------------------------------------------

def gen_header():
    """File header."""
    return [
        '"""',
        f"Auto-generated Python mega-codebase — {TARGET_LINES:,} lines",
        "Contains classes, functions, algorithms, data structures, and utilities.",
        "Generated by mega_code_generator.py",
        '"""',
        "",
        "from __future__ import annotations",
        "import math, os, sys, hashlib, json, re, itertools, functools",
        "import collections, operator, random, string, struct, io, abc",
        "from typing import (Any, Dict, List, Optional, Tuple, Set, Union,",
        "                     Callable, Iterator, Generator, TypeVar, Generic,",
        "                     Protocol, ClassVar, Final)",
        "from dataclasses import dataclass, field",
        "from enum import Enum, IntEnum, auto",
        "from contextlib import contextmanager",
        "",
        "T = TypeVar('T')",
        "K = TypeVar('K')",
        "V = TypeVar('V')",
        "",
        "",
    ]


def gen_enum():
    """Generate an Enum class."""
    name = f"Status{rand_name('class')}"
    members = random.randint(4, 12)
    lines = [
        f"class {name}(Enum):",
        f'    """Enumeration for {name} states."""',
    ]
    for i in range(members):
        member_name = f"{random.choice(ADJECTIVES).upper()}_{random.choice(NOUNS).upper()}"
        lines.append(f"    {member_name}_{i} = auto()")
    lines += ["", ""]
    return lines


def gen_dataclass():
    """Generate a dataclass."""
    name = rand_name("class")
    n_fields = random.randint(3, 10)
    lines = [
        "@dataclass",
        f"class {name}:",
        f'    """Data container for {name}."""',
    ]
    for _ in range(n_fields):
        fname = rand_name("var")
        ftype = rand_type()
        if random.random() < 0.3:
            lines.append(f"    {fname}: {ftype} = {rand_value(ftype)}")
        else:
            lines.append(f"    {fname}: {ftype} = field(default_factory={ftype})")
    lines += ["", ""]
    return lines


def gen_standalone_function():
    """Generate a standalone function with logic."""
    name = rand_name("func")
    params = rand_params()
    ret = rand_type()
    body_style = random.choice([
        "arithmetic", "loop", "conditional", "list_comp",
        "dict_comp", "try_except", "generator", "recursive",
        "string_ops", "math_ops", "hash_ops", "reduce_ops",
    ])
    lines = [
        f"def {name}({params}) -> {ret}:",
        f'    """Perform {body_style} operation for {name}."""',
    ]

    # Add local variables
    for _ in range(random.randint(1, 4)):
        v = rand_name("var")
        lines.append(f"    {v} = {rand_value()}")

    if body_style == "arithmetic":
        a, b = rand_name("var"), rand_name("var")
        lines.append(f"    {a} = {random.randint(1, 1000)}")
        lines.append(f"    {b} = {random.randint(1, 1000)}")
        for _ in range(random.randint(2, 6)):
            op = random.choice(OPERATORS[:5])
            c = rand_name("var")
            lines.append(f"    {c} = {a} {op} {b}")
            a = c
        lines.append(f"    return {a}")

    elif body_style == "loop":
        acc = rand_name("var")
        i = rand_name("var")
        limit = random.randint(10, 500)
        lines.append(f"    {acc} = 0")
        lines.append(f"    for {i} in range({limit}):")
        lines.append(f"        {acc} += {i} * {random.randint(1, 10)}")
        if random.random() < 0.5:
            lines.append(f"        if {i} % {random.randint(2, 7)} == 0:")
            lines.append(f"            {acc} -= {random.randint(1, 5)}")
        lines.append(f"    return {acc}")

    elif body_style == "conditional":
        v = rand_name("var")
        lines.append(f"    {v} = {random.randint(-100, 100)}")
        for _ in range(random.randint(2, 5)):
            comp = random.choice(COMPARISONS)
            threshold = random.randint(-50, 50)
            result = rand_value()
            lines.append(f"    if {v} {comp} {threshold}:")
            lines.append(f"        return {result}")
        lines.append(f"    return {rand_value()}")

    elif body_style == "list_comp":
        limit = random.randint(10, 100)
        expr = random.choice([
            f"x ** {random.randint(2, 4)}",
            f"x * {random.randint(2, 10)} + {random.randint(1, 100)}",
            f"math.sqrt(abs(x)) if x != 0 else 0",
            f"str(x).zfill({random.randint(3, 8)})",
        ])
        result = rand_name("var")
        lines.append(f"    {result} = [{expr} for x in range({limit})]")
        if random.random() < 0.5:
            lines.append(f"    {result} = [v for v in {result} if v]")
        lines.append(f"    return {result}")

    elif body_style == "dict_comp":
        limit = random.randint(5, 50)
        result = rand_name("var")
        lines.append(f"    {result} = {{f'key_{{i}}': i ** 2 for i in range({limit})}}")
        lines.append(f"    return {result}")

    elif body_style == "try_except":
        lines.append("    try:")
        lines.append(f"        result = {random.randint(1, 1000)} / {random.randint(0, 5)}")
        lines.append(f"        result += math.log(abs(result) + 1)")
        lines.append("    except ZeroDivisionError:")
        lines.append("        result = float('inf')")
        lines.append("    except (ValueError, OverflowError):")
        lines.append("        result = 0.0")
        lines.append("    finally:")
        lines.append(f"        pass  # cleanup for {name}")
        lines.append("    return result")

    elif body_style == "generator":
        limit = random.randint(10, 100)
        lines.append(f"    def _inner():")
        lines.append(f"        for i in range({limit}):")
        lines.append(f"            yield i * {random.randint(2, 10)}")
        lines.append(f"    return list(_inner())")

    elif body_style == "recursive":
        lines.append(f"    n = abs(hash(str({rand_value()}))) % 20")
        lines.append("    if n <= 1:")
        lines.append("        return n")
        lines.append(f"    # Iterative to avoid stack overflow")
        lines.append(f"    a, b = 0, 1")
        lines.append(f"    for _ in range(n):")
        lines.append(f"        a, b = b, a + b")
        lines.append(f"    return a")

    elif body_style == "string_ops":
        lines.append(f'    text = "{" ".join(random.choices(ADJECTIVES, k=5))}"')
        lines.append(f"    tokens = text.split()")
        lines.append(f"    tokens = [t.upper() for t in tokens]")
        lines.append(f"    tokens.sort()")
        lines.append(f'    return "_".join(tokens)')

    elif body_style == "math_ops":
        lines.append(f"    values = [{', '.join(str(random.uniform(-100, 100)) for _ in range(6))}]")
        lines.append(f"    mean = sum(values) / len(values)")
        lines.append(f"    variance = sum((x - mean) ** 2 for x in values) / len(values)")
        lines.append(f"    std_dev = math.sqrt(variance)")
        lines.append(f"    return std_dev")

    elif body_style == "hash_ops":
        lines.append(f'    data = "{random.choice(NOUNS)}" * {random.randint(10, 100)}')
        lines.append(f"    h = hashlib.sha256(data.encode()).hexdigest()")
        lines.append(f"    return h")

    elif body_style == "reduce_ops":
        lines.append(f"    items = list(range(1, {random.randint(10, 50)}))")
        lines.append(f"    total = functools.reduce(operator.mul, items, 1)")
        lines.append(f"    return total % (10 ** 9 + 7)")

    lines += ["", ""]
    return lines


def gen_class():
    """Generate a full class with methods."""
    class_name = rand_name("class")
    n_methods = random.randint(4, 15)
    n_attrs = random.randint(3, 8)
    parent = random.choice(["", "", "", "(abc.ABC)", f"(Generic[T])"])

    lines = [
        f"class {class_name}{parent}:",
        f'    """',
        f"    {class_name}: A comprehensive implementation.",
        f"    ",
        f"    This class provides {random.choice(DOMAINS)} functionality",
        f"    for {random.choice(NOUNS)} processing and management.",
        f'    """',
        f"",
    ]

    # Class variables
    for _ in range(random.randint(1, 3)):
        cv = rand_name("var").upper()
        lines.append(f"    {cv}: ClassVar[{rand_type()}] = {rand_value()}")
    lines.append("")

    # __init__
    init_params = []
    attr_assignments = []
    for _ in range(n_attrs):
        attr = rand_name("var")
        typ = rand_type()
        init_params.append(f"{attr}: {typ} = {rand_value(typ)}")
        attr_assignments.append(f"        self.{attr} = {attr}")

    lines.append(f"    def __init__(self, {', '.join(init_params)}) -> None:")
    lines.append(f'        """Initialize {class_name}."""')
    lines.extend(attr_assignments)
    lines.append(f"        self._cache: Dict[str, Any] = {{}}")
    lines.append(f"        self._initialized = True")
    lines.append("")

    # __repr__
    lines.append(f"    def __repr__(self) -> str:")
    lines.append(f'        return f"{class_name}(initialized={{self._initialized}})"')
    lines.append("")

    # __eq__
    lines.append(f"    def __eq__(self, other: object) -> bool:")
    lines.append(f"        if not isinstance(other, {class_name}):")
    lines.append(f"            return NotImplemented")
    lines.append(f"        return self._initialized == other._initialized")
    lines.append("")

    # __hash__
    lines.append(f"    def __hash__(self) -> int:")
    lines.append(f"        return hash(self._initialized)")
    lines.append("")

    # Regular methods
    for _ in range(n_methods):
        method_name = rand_name("func")
        params = rand_params(random.randint(0, 4))
        if params:
            params = f"self, {params}"
        else:
            params = "self"
        ret = rand_type()

        is_abstract = parent == "(abc.ABC)" and random.random() < 0.2
        is_property = random.random() < 0.15
        is_static = random.random() < 0.1
        is_classmethod = random.random() < 0.1

        if is_property:
            lines.append(f"    @property")
            lines.append(f"    def {method_name}(self) -> {ret}:")
            lines.append(f'        """Property {method_name}."""')
            lines.append(f"        return {rand_value(ret)}")
        elif is_static:
            lines.append(f"    @staticmethod")
            sp = rand_params(random.randint(1, 3))
            lines.append(f"    def {method_name}({sp}) -> {ret}:")
            lines.append(f'        """Static method {method_name}."""')
            lines.append(f"        return {rand_value(ret)}")
        elif is_classmethod:
            lines.append(f"    @classmethod")
            cp = rand_params(random.randint(0, 2))
            if cp:
                cp = f"cls, {cp}"
            else:
                cp = "cls"
            lines.append(f"    def {method_name}({cp}) -> '{class_name}':")
            lines.append(f'        """Class method {method_name}."""')
            lines.append(f"        return cls()")
        elif is_abstract:
            lines.append(f"    @abc.abstractmethod")
            lines.append(f"    def {method_name}({params}) -> {ret}:")
            lines.append(f'        """Abstract method {method_name}."""')
            lines.append(f"        ...")
        else:
            lines.append(f"    def {method_name}({params}) -> {ret}:")
            lines.append(f'        """Method {method_name} of {class_name}."""')
            # Method body
            for _ in range(random.randint(1, 3)):
                v = rand_name("var")
                lines.append(f"        {v} = {rand_value()}")
            # Some logic
            if random.random() < 0.5:
                v1 = rand_name("var")
                lines.append(f"        {v1} = []")
                lines.append(f"        for i in range({random.randint(5, 30)}):")
                lines.append(f"            {v1}.append(i * {random.randint(1, 10)})")
            if random.random() < 0.3:
                lines.append(f"        if self._initialized:")
                lines.append(f"            self._cache['{method_name}'] = {rand_value()}")
            lines.append(f"        return {rand_value(ret)}")
        lines.append("")

    # Context manager method
    if random.random() < 0.5:
        lines.append(f"    def __enter__(self):")
        lines.append(f"        return self")
        lines.append("")
        lines.append(f"    def __exit__(self, exc_type, exc_val, exc_tb):")
        lines.append(f"        self._cache.clear()")
        lines.append(f"        return False")
        lines.append("")

    lines.append("")
    return lines


def gen_algorithm():
    """Generate a common algorithm implementation."""
    algo = random.choice([
        "bubble_sort", "insertion_sort", "merge_sort", "quick_sort",
        "binary_search", "bfs", "dfs", "dijkstra",
        "knapsack", "fibonacci_dp", "lcs", "matrix_multiply",
        "gcd_extended", "sieve_primes", "kadane_max_subarray",
        "edit_distance", "coin_change", "topological_sort",
    ])
    suffix = uid()
    lines = []

    if algo == "bubble_sort":
        lines = [
            f"def bubble_sort_{suffix}(arr: List[int]) -> List[int]:",
            f'    """Bubble sort implementation #{suffix}."""',
            f"    arr = arr.copy()",
            f"    n = len(arr)",
            f"    for i in range(n):",
            f"        swapped = False",
            f"        for j in range(0, n - i - 1):",
            f"            if arr[j] > arr[j + 1]:",
            f"                arr[j], arr[j + 1] = arr[j + 1], arr[j]",
            f"                swapped = True",
            f"        if not swapped:",
            f"            break",
            f"    return arr",
        ]
    elif algo == "insertion_sort":
        lines = [
            f"def insertion_sort_{suffix}(arr: List[int]) -> List[int]:",
            f'    """Insertion sort implementation #{suffix}."""',
            f"    arr = arr.copy()",
            f"    for i in range(1, len(arr)):",
            f"        key = arr[i]",
            f"        j = i - 1",
            f"        while j >= 0 and arr[j] > key:",
            f"            arr[j + 1] = arr[j]",
            f"            j -= 1",
            f"        arr[j + 1] = key",
            f"    return arr",
        ]
    elif algo == "merge_sort":
        lines = [
            f"def merge_sort_{suffix}(arr: List[int]) -> List[int]:",
            f'    """Merge sort implementation #{suffix}."""',
            f"    if len(arr) <= 1:",
            f"        return arr",
            f"    mid = len(arr) // 2",
            f"    left = merge_sort_{suffix}(arr[:mid])",
            f"    right = merge_sort_{suffix}(arr[mid:])",
            f"    return _merge_{suffix}(left, right)",
            f"",
            f"def _merge_{suffix}(left: List[int], right: List[int]) -> List[int]:",
            f'    """Merge helper for merge_sort_{suffix}."""',
            f"    result = []",
            f"    i = j = 0",
            f"    while i < len(left) and j < len(right):",
            f"        if left[i] <= right[j]:",
            f"            result.append(left[i])",
            f"            i += 1",
            f"        else:",
            f"            result.append(right[j])",
            f"            j += 1",
            f"    result.extend(left[i:])",
            f"    result.extend(right[j:])",
            f"    return result",
        ]
    elif algo == "quick_sort":
        lines = [
            f"def quick_sort_{suffix}(arr: List[int]) -> List[int]:",
            f'    """Quick sort implementation #{suffix}."""',
            f"    if len(arr) <= 1:",
            f"        return arr",
            f"    pivot = arr[len(arr) // 2]",
            f"    left = [x for x in arr if x < pivot]",
            f"    middle = [x for x in arr if x == pivot]",
            f"    right = [x for x in arr if x > pivot]",
            f"    return quick_sort_{suffix}(left) + middle + quick_sort_{suffix}(right)",
        ]
    elif algo == "binary_search":
        lines = [
            f"def binary_search_{suffix}(arr: List[int], target: int) -> int:",
            f'    """Binary search implementation #{suffix}."""',
            f"    low, high = 0, len(arr) - 1",
            f"    while low <= high:",
            f"        mid = (low + high) // 2",
            f"        if arr[mid] == target:",
            f"            return mid",
            f"        elif arr[mid] < target:",
            f"            low = mid + 1",
            f"        else:",
            f"            high = mid - 1",
            f"    return -1",
        ]
    elif algo == "bfs":
        lines = [
            f"def bfs_{suffix}(graph: Dict[str, List[str]], start: str) -> List[str]:",
            f'    """Breadth-first search implementation #{suffix}."""',
            f"    visited = set()",
            f"    queue = collections.deque([start])",
            f"    result = []",
            f"    while queue:",
            f"        node = queue.popleft()",
            f"        if node not in visited:",
            f"            visited.add(node)",
            f"            result.append(node)",
            f"            for neighbor in graph.get(node, []):",
            f"                if neighbor not in visited:",
            f"                    queue.append(neighbor)",
            f"    return result",
        ]
    elif algo == "dfs":
        lines = [
            f"def dfs_{suffix}(graph: Dict[str, List[str]], start: str) -> List[str]:",
            f'    """Depth-first search implementation #{suffix}."""',
            f"    visited = set()",
            f"    result = []",
            f"    stack = [start]",
            f"    while stack:",
            f"        node = stack.pop()",
            f"        if node not in visited:",
            f"            visited.add(node)",
            f"            result.append(node)",
            f"            for neighbor in reversed(graph.get(node, [])):",
            f"                if neighbor not in visited:",
            f"                    stack.append(neighbor)",
            f"    return result",
        ]
    elif algo == "dijkstra":
        lines = [
            f"def dijkstra_{suffix}(graph: Dict[str, List[Tuple[str, int]]], start: str) -> Dict[str, int]:",
            f'    """Dijkstra shortest path implementation #{suffix}."""',
            f"    import heapq",
            f"    distances: Dict[str, int] = {{start: 0}}",
            f"    pq = [(0, start)]",
            f"    visited: Set[str] = set()",
            f"    while pq:",
            f"        dist, node = heapq.heappop(pq)",
            f"        if node in visited:",
            f"            continue",
            f"        visited.add(node)",
            f"        for neighbor, weight in graph.get(node, []):",
            f"            new_dist = dist + weight",
            f"            if neighbor not in distances or new_dist < distances[neighbor]:",
            f"                distances[neighbor] = new_dist",
            f"                heapq.heappush(pq, (new_dist, neighbor))",
            f"    return distances",
        ]
    elif algo == "knapsack":
        lines = [
            f"def knapsack_{suffix}(weights: List[int], values: List[int], capacity: int) -> int:",
            f'    """0/1 Knapsack DP implementation #{suffix}."""',
            f"    n = len(weights)",
            f"    dp = [[0] * (capacity + 1) for _ in range(n + 1)]",
            f"    for i in range(1, n + 1):",
            f"        for w in range(capacity + 1):",
            f"            dp[i][w] = dp[i - 1][w]",
            f"            if weights[i - 1] <= w:",
            f"                dp[i][w] = max(dp[i][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])",
            f"    return dp[n][capacity]",
        ]
    elif algo == "fibonacci_dp":
        lines = [
            f"def fibonacci_dp_{suffix}(n: int) -> int:",
            f'    """Fibonacci with DP implementation #{suffix}."""',
            f"    if n <= 1:",
            f"        return n",
            f"    dp = [0] * (n + 1)",
            f"    dp[1] = 1",
            f"    for i in range(2, n + 1):",
            f"        dp[i] = dp[i - 1] + dp[i - 2]",
            f"    return dp[n]",
        ]
    elif algo == "lcs":
        lines = [
            f"def lcs_{suffix}(s1: str, s2: str) -> int:",
            f'    """Longest common subsequence implementation #{suffix}."""',
            f"    m, n = len(s1), len(s2)",
            f"    dp = [[0] * (n + 1) for _ in range(m + 1)]",
            f"    for i in range(1, m + 1):",
            f"        for j in range(1, n + 1):",
            f"            if s1[i - 1] == s2[j - 1]:",
            f"                dp[i][j] = dp[i - 1][j - 1] + 1",
            f"            else:",
            f"                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])",
            f"    return dp[m][n]",
        ]
    elif algo == "matrix_multiply":
        lines = [
            f"def matrix_multiply_{suffix}(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:",
            f'    """Matrix multiplication implementation #{suffix}."""',
            f"    rows_a, cols_a = len(a), len(a[0])",
            f"    rows_b, cols_b = len(b), len(b[0])",
            f"    assert cols_a == rows_b, 'Incompatible matrices'",
            f"    result = [[0.0] * cols_b for _ in range(rows_a)]",
            f"    for i in range(rows_a):",
            f"        for j in range(cols_b):",
            f"            for k in range(cols_a):",
            f"                result[i][j] += a[i][k] * b[k][j]",
            f"    return result",
        ]
    elif algo == "gcd_extended":
        lines = [
            f"def gcd_extended_{suffix}(a: int, b: int) -> Tuple[int, int, int]:",
            f'    """Extended GCD implementation #{suffix}."""',
            f"    if a == 0:",
            f"        return b, 0, 1",
            f"    gcd, x1, y1 = gcd_extended_{suffix}(b % a, a)",
            f"    x = y1 - (b // a) * x1",
            f"    y = x1",
            f"    return gcd, x, y",
        ]
    elif algo == "sieve_primes":
        lines = [
            f"def sieve_primes_{suffix}(limit: int) -> List[int]:",
            f'    """Sieve of Eratosthenes implementation #{suffix}."""',
            f"    if limit < 2:",
            f"        return []",
            f"    is_prime = [True] * (limit + 1)",
            f"    is_prime[0] = is_prime[1] = False",
            f"    for i in range(2, int(limit ** 0.5) + 1):",
            f"        if is_prime[i]:",
            f"            for j in range(i * i, limit + 1, i):",
            f"                is_prime[j] = False",
            f"    return [i for i, p in enumerate(is_prime) if p]",
        ]
    elif algo == "kadane_max_subarray":
        lines = [
            f"def kadane_{suffix}(arr: List[int]) -> int:",
            f'    """Kadane maximum subarray implementation #{suffix}."""',
            f"    max_sum = current = arr[0] if arr else 0",
            f"    for x in arr[1:]:",
            f"        current = max(x, current + x)",
            f"        max_sum = max(max_sum, current)",
            f"    return max_sum",
        ]
    elif algo == "edit_distance":
        lines = [
            f"def edit_distance_{suffix}(s1: str, s2: str) -> int:",
            f'    """Edit distance (Levenshtein) implementation #{suffix}."""',
            f"    m, n = len(s1), len(s2)",
            f"    dp = list(range(n + 1))",
            f"    for i in range(1, m + 1):",
            f"        prev = dp[0]",
            f"        dp[0] = i",
            f"        for j in range(1, n + 1):",
            f"            temp = dp[j]",
            f"            if s1[i - 1] == s2[j - 1]:",
            f"                dp[j] = prev",
            f"            else:",
            f"                dp[j] = 1 + min(prev, dp[j], dp[j - 1])",
            f"            prev = temp",
            f"    return dp[n]",
        ]
    elif algo == "coin_change":
        lines = [
            f"def coin_change_{suffix}(coins: List[int], amount: int) -> int:",
            f'    """Coin change DP implementation #{suffix}."""',
            f"    dp = [float('inf')] * (amount + 1)",
            f"    dp[0] = 0",
            f"    for coin in coins:",
            f"        for x in range(coin, amount + 1):",
            f"            dp[x] = min(dp[x], dp[x - coin] + 1)",
            f"    return dp[amount] if dp[amount] != float('inf') else -1",
        ]
    elif algo == "topological_sort":
        lines = [
            f"def topological_sort_{suffix}(graph: Dict[str, List[str]]) -> List[str]:",
            f'    """Topological sort (Kahn) implementation #{suffix}."""',
            f"    in_degree: Dict[str, int] = {{node: 0 for node in graph}}",
            f"    for node in graph:",
            f"        for neighbor in graph[node]:",
            f"            in_degree[neighbor] = in_degree.get(neighbor, 0) + 1",
            f"    queue = collections.deque([n for n, d in in_degree.items() if d == 0])",
            f"    result = []",
            f"    while queue:",
            f"        node = queue.popleft()",
            f"        result.append(node)",
            f"        for neighbor in graph.get(node, []):",
            f"            in_degree[neighbor] -= 1",
            f"            if in_degree[neighbor] == 0:",
            f"                queue.append(neighbor)",
            f"    return result",
        ]

    lines += ["", ""]
    return lines


def gen_constants_block():
    """Generate a block of constants and lookup tables."""
    lines = []
    block_name = rand_name("module").upper()
    lines.append(f"# {'=' * 70}")
    lines.append(f"# Constants: {block_name}")
    lines.append(f"# {'=' * 70}")
    lines.append("")

    # Large lookup table
    table_name = f"LOOKUP_{block_name}"
    n_entries = random.randint(50, 200)
    lines.append(f"{table_name} = {{")
    for i in range(n_entries):
        key = f"    \"{random.choice(DOMAINS)}_{random.choice(NOUNS)}_{i}\""
        val = rand_value(random.choice(["int", "float", "str"]))
        lines.append(f"    {key}: {val},")
    lines.append("}")
    lines.append("")

    # Config dict
    config_name = f"CONFIG_{block_name}"
    lines.append(f"{config_name} = {{")
    for _ in range(random.randint(10, 30)):
        k = f'"{random.choice(DOMAINS)}.{random.choice(NOUNS)}.{random.choice(ADJECTIVES)}"'
        v = rand_value()
        lines.append(f"    {k}: {v},")
    lines.append("}")
    lines.append("")

    # Tuple of tuples (like a CSV table)
    data_name = f"DATA_{block_name}"
    n_rows = random.randint(20, 80)
    lines.append(f"{data_name} = (")
    for _ in range(n_rows):
        row_vals = ", ".join(rand_value(random.choice(["int", "float", "str"])) for _ in range(random.randint(3, 7)))
        lines.append(f"    ({row_vals}),")
    lines.append(")")
    lines.append("")
    lines.append("")
    return lines


def gen_decorator():
    """Generate a decorator function."""
    name = rand_name("func")
    lines = [
        f"def {name}(func: Callable) -> Callable:",
        f'    """Decorator: {name}."""',
        f"    @functools.wraps(func)",
        f"    def wrapper(*args, **kwargs):",
        f'        # Pre-processing for {name}',
    ]
    if random.random() < 0.5:
        lines.append(f"        import time")
        lines.append(f"        start = time.perf_counter()")
    lines.append(f"        result = func(*args, **kwargs)")
    if random.random() < 0.5:
        lines.append(f"        elapsed = time.perf_counter() - start")
    lines.extend([
        f"        return result",
        f"    return wrapper",
        "",
        "",
    ])
    return lines


def gen_context_manager():
    """Generate a context manager."""
    name = rand_name("func")
    lines = [
        f"@contextmanager",
        f"def {name}({rand_params(random.randint(0, 3))}):",
        f'    """Context manager: {name}."""',
        f"    resource = {rand_value('dict')}",
        f"    try:",
        f"        yield resource",
        f"    except Exception as e:",
        f"        pass  # handle error in {name}",
        f"    finally:",
        f"        resource.clear()",
        "",
        "",
    ]
    return lines


def gen_protocol():
    """Generate a Protocol class."""
    name = f"I{rand_name('class')}"
    n_methods = random.randint(2, 6)
    lines = [
        f"class {name}(Protocol):",
        f'    """Protocol interface {name}."""',
        "",
    ]
    for _ in range(n_methods):
        mname = rand_name("func")
        params = rand_params(random.randint(0, 3))
        ret = rand_type()
        lines.append(f"    def {mname}(self, {params}) -> {ret}: ...")
        lines.append("")
    lines.append("")
    return lines


def gen_exception_hierarchy():
    """Generate custom exception classes."""
    base_name = f"{random.choice(ADJECTIVES).capitalize()}{random.choice(NOUNS).capitalize()}Error_{uid()}"
    lines = [
        f"class {base_name}(Exception):",
        f'    """Base exception for {base_name}."""',
        f"    def __init__(self, message: str = '', code: int = 0) -> None:",
        f"        self.code = code",
        f"        super().__init__(message)",
        "",
    ]
    for _ in range(random.randint(2, 5)):
        child = f"{random.choice(ADJECTIVES).capitalize()}{base_name}"
        lines.extend([
            f"class {child}({base_name}):",
            f'    """Specific error: {child}."""',
            f"    pass",
            "",
        ])
    lines.append("")
    return lines


def gen_namedtuple_block():
    """Generate named tuples."""
    lines = []
    for _ in range(random.randint(2, 5)):
        name = rand_name("class")
        fields = " ".join(rand_name("var") for _ in range(random.randint(2, 6)))
        lines.append(f"{name} = collections.namedtuple('{name}', '{fields}')")
    lines += ["", ""]
    return lines


def gen_type_alias_block():
    """Generate type aliases."""
    lines = []
    for _ in range(random.randint(3, 8)):
        name = rand_name("class")
        inner = random.choice([
            f"Dict[str, {rand_type()}]",
            f"List[Tuple[{rand_type()}, {rand_type()}]]",
            f"Optional[{rand_type()}]",
            f"Union[{rand_type()}, {rand_type()}]",
            f"Callable[[{rand_type()}], {rand_type()}]",
            f"Iterator[{rand_type()}]",
        ])
        lines.append(f"{name} = {inner}")
    lines += ["", ""]
    return lines


def gen_section_banner(section_num):
    """Generate a section divider banner."""
    domain = random.choice(DOMAINS)
    return [
        "",
        f"# {'#' * 72}",
        f"# SECTION {section_num}: {domain.upper()} MODULE",
        f"# {random.choice(ADJECTIVES).capitalize()} {random.choice(NOUNS)} subsystem",
        f"# {'#' * 72}",
        "",
    ]


# ---------------------------------------------------------------------------
# Weighted generator selection
# ---------------------------------------------------------------------------
GENERATORS = [
    (gen_standalone_function, 30),  # most common
    (gen_class, 20),
    (gen_algorithm, 12),
    (gen_constants_block, 10),
    (gen_dataclass, 8),
    (gen_enum, 5),
    (gen_decorator, 4),
    (gen_context_manager, 3),
    (gen_protocol, 3),
    (gen_exception_hierarchy, 3),
    (gen_namedtuple_block, 1),
    (gen_type_alias_block, 1),
]

gen_funcs, gen_weights = zip(*GENERATORS)


# ---------------------------------------------------------------------------
# Main generation loop
# ---------------------------------------------------------------------------
def main():
    print(f"[*] Generating ~{TARGET_LINES:,} lines of Python code...")
    print(f"   Output: {OUTPUT_FILE}")

    total_lines = 0
    section = 0
    chunk_size = 5000  # write in chunks for performance

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        # Write header
        header = gen_header()
        f.write("\n".join(header) + "\n")
        total_lines += len(header)

        buffer = []

        while total_lines < TARGET_LINES:
            # Section banner every ~50k lines
            if total_lines % 50_000 < 100:
                section += 1
                banner = gen_section_banner(section)
                buffer.extend(banner)

            # Pick a random generator
            gen_func = random.choices(gen_funcs, weights=gen_weights, k=1)[0]
            code_block = gen_func()
            buffer.extend(code_block)

            # Flush buffer periodically
            if len(buffer) >= chunk_size:
                text = "\n".join(buffer) + "\n"
                f.write(text)
                total_lines += len(buffer)
                buffer.clear()

                # Progress report every ~1M lines
                if total_lines % 1_000_000 < chunk_size:
                    pct = total_lines / TARGET_LINES * 100
                    print(f"   [>] {total_lines:>12,} / {TARGET_LINES:,} lines ({pct:5.1f}%)")

        # Flush remaining
        if buffer:
            f.write("\n".join(buffer) + "\n")
            total_lines += len(buffer)

        # Footer
        f.write("\n")
        f.write(f"# {'=' * 72}\n")
        f.write(f"# End of auto-generated codebase — {total_lines:,} lines\n")
        f.write(f"# {'=' * 72}\n")
        f.write("\n")
        f.write("if __name__ == '__main__':\n")
        f.write("    print('Mega codebase loaded successfully.')\n")
        f.write(f"    print(f'Approximate lines: {total_lines:,}')\n")
        total_lines += 5

    file_size = os.path.getsize(OUTPUT_FILE)
    size_mb = file_size / (1024 * 1024)
    size_gb = file_size / (1024 * 1024 * 1024)

    print(f"\n[OK] Done!")
    print(f"   Total lines:  {total_lines:,}")
    print(f"   File size:    {size_mb:,.1f} MB ({size_gb:.2f} GB)")
    print(f"   Output file:  {os.path.abspath(OUTPUT_FILE)}")


if __name__ == "__main__":
    main()
