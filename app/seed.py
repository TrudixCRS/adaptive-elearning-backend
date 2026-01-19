import json
from sqlalchemy import select
from .db import SessionLocal, Base, engine
from . import models


def md(*lines: str) -> str:
    return "\n".join(lines).strip() + "\n"


def quiz_json(questions: list[dict]) -> str:
    """
    The frontend Quiz UI expects:
    {"questions":[{"q":"...","options":[...],"answerIndex":0,"explain":"..."}]}
    """
    return json.dumps({"questions": questions}, ensure_ascii=False)


def make_text(title: str, difficulty: int, sort_order: int, content_lines: list[str]):
    return {
        "title": title,
        "lesson_type": "text",
        "difficulty": difficulty,
        "sort_order": sort_order,
        "content": md(*content_lines),
    }


def make_quiz(title: str, difficulty: int, sort_order: int, questions: list[dict]):
    return {
        "title": title,
        "lesson_type": "quiz",
        "difficulty": difficulty,
        "sort_order": sort_order,
        "content": quiz_json(questions),
    }


def course_template(title: str, description: str, modules: list[dict]):
    return {"title": title, "description": description, "modules": modules}


COURSES = [
    # 1) Intro to Python (FULL)
    course_template(
        "Intro to Python",
        "A complete beginner-friendly Python course: fundamentals → control flow → functions → collections → files. Includes a final quiz.",
        [
            {
                "title": "Foundations",
                "sort_order": 1,
                "lessons": [
                    make_text(
                        "Welcome & Setup",
                        1,
                        1,
                        [
                            "# Welcome to Python",
                            "",
                            "Python is popular because it’s readable, versatile, and fast to build with.",
                            "",
                            "## What you’ll build during this course",
                            "- Small scripts (calculators, checkers, mini tools)",
                            "- Data handling with lists/dicts",
                            "- Functions you can reuse",
                            "",
                            "## How to practice",
                            "Use this loop:",
                            "1. Read the example",
                            "2. Type it yourself (don’t copy/paste)",
                            "3. Change one thing and predict the output",
                            "",
                            "✅ Tip: keep a file named `practice.py` for experiments.",
                        ],
                    ),
                    make_text(
                        "Variables, Types & Input",
                        1,
                        2,
                        [
                            "# Variables, Types & Input",
                            "",
                            "A variable stores a value:",
                            "```py",
                            "name = 'Cristian'",
                            "age = 21",
                            "price = 19.99",
                            "is_active = True",
                            "```",
                            "",
                            "## Input from user",
                            "```py",
                            "name = input('Your name: ')",
                            "print('Hello', name)",
                            "```",
                            "",
                            "## Convert types",
                            "```py",
                            "age = int(input('Age: '))",
                            "height = float(input('Height: '))",
                            "```",
                            "",
                            "Mini task: ask user for 2 numbers and print the sum.",
                        ],
                    ),
                ],
            },
            {
                "title": "Control Flow",
                "sort_order": 2,
                "lessons": [
                    make_text(
                        "If / Elif / Else",
                        2,
                        1,
                        [
                            "# If / Elif / Else",
                            "",
                            "Conditionals let your program decide:",
                            "```py",
                            "score = 72",
                            "if score >= 90:",
                            "    grade = 'A'",
                            "elif score >= 70:",
                            "    grade = 'B'",
                            "else:",
                            "    grade = 'C'",
                            "print(grade)",
                            "```",
                            "",
                            "## Comparison operators",
                            "- `== != < > <= >=`",
                            "- Combine with `and`, `or`, `not`",
                            "",
                            "Mini task: build a simple login check (email + password).",
                        ],
                    ),
                    make_text(
                        "Loops (for / while) + range",
                        2,
                        2,
                        [
                            "# Loops (for / while)",
                            "",
                            "## for + range",
                            "```py",
                            "for i in range(5):",
                            "    print(i)",
                            "```",
                            "",
                            "## while",
                            "```py",
                            "x = 0",
                            "while x < 3:",
                            "    print('x is', x)",
                            "    x += 1",
                            "```",
                            "",
                            "## break / continue",
                            "```py",
                            "for i in range(10):",
                            "    if i == 5:",
                            "        break",
                            "```",
                            "",
                            "Mini task: keep asking for a password until correct.",
                        ],
                    ),
                ],
            },
            {
                "title": "Functions, Collections & Files",
                "sort_order": 3,
                "lessons": [
                    make_text(
                        "Functions (Clean Code Basics)",
                        2,
                        1,
                        [
                            "# Functions",
                            "",
                            "Functions package reusable logic.",
                            "```py",
                            "def add(a, b):",
                            "    return a + b",
                            "",
                            "print(add(2, 3))",
                            "```",
                            "",
                            "## Good habits",
                            "- Name functions clearly: `calculate_tax()`",
                            "- Keep functions small",
                            "- One function = one purpose",
                            "",
                            "Mini task: write `is_even(n)` and `clamp(n, low, high)`.",
                        ],
                    ),
                    make_text(
                        "Lists, Dicts + Reading/Writing Files",
                        2,
                        2,
                        [
                            "# Lists & Dicts",
                            "",
                            "Lists are ordered:",
                            "```py",
                            "nums = [1, 2, 3]",
                            "nums.append(4)",
                            "```",
                            "",
                            "Dicts are key-value maps:",
                            "```py",
                            "user = {'name': 'Cristian', 'role': 'student'}",
                            "print(user['name'])",
                            "```",
                            "",
                            "# Files",
                            "Write:",
                            "```py",
                            "with open('notes.txt', 'w', encoding='utf-8') as f:",
                            "    f.write('Hello')",
                            "```",
                            "Read:",
                            "```py",
                            "with open('notes.txt', 'r', encoding='utf-8') as f:",
                            "    print(f.read())",
                            "```",
                            "",
                            "Mini task: store a list of tasks into a file and read it back.",
                        ],
                    ),
                    make_quiz(
                        "Final Quiz: Intro to Python",
                        2,
                        3,
                        [
                            {
                                "q": "What does `input()` return?",
                                "options": ["int", "float", "str", "bool"],
                                "answerIndex": 2,
                                "explain": "`input()` returns a string; convert it with int()/float() when needed.",
                            },
                            {
                                "q": "Which operator means 'equal to'?",
                                "options": ["=", "==", "!=", "<="],
                                "answerIndex": 1,
                                "explain": "`==` checks equality; `=` assigns a value.",
                            },
                            {
                                "q": "What does `range(3)` generate?",
                                "options": ["1,2,3", "0,1,2", "0,1,2,3", "3 only"],
                                "answerIndex": 1,
                                "explain": "range(3) is 0,1,2.",
                            },
                            {
                                "q": "Which structure maps keys to values?",
                                "options": ["list", "dict", "tuple", "set"],
                                "answerIndex": 1,
                                "explain": "A dict stores key-value pairs.",
                            },
                            {
                                "q": "Best way to open a file safely?",
                                "options": ["open()", "with open(...) as f:", "file.open()", "readfile()"],
                                "answerIndex": 1,
                                "explain": "`with open` auto-closes the file even on errors.",
                            },
                            {
                                "q": "What does `return` do in a function?",
                                "options": ["Prints output", "Stops loop", "Sends value back to caller", "Imports a module"],
                                "answerIndex": 2,
                                "explain": "`return` returns a value to where the function was called.",
                            },
                        ],
                    ),
                ],
            },
        ],
    ),

    # 2) Python OOP
    course_template(
        "Python OOP (Object-Oriented Programming)",
        "Learn classes, objects, methods, inheritance, composition, and clean design patterns.",
        [
            {
                "title": "OOP Basics",
                "sort_order": 1,
                "lessons": [
                    make_text(
                        "Classes & Objects",
                        2,
                        1,
                        [
                            "# Classes & Objects",
                            "",
                            "A class is a blueprint. An object is an instance.",
                            "```py",
                            "class User:",
                            "    def __init__(self, name):",
                            "        self.name = name",
                            "",
                            "u = User('Cristian')",
                            "print(u.name)",
                            "```",
                            "",
                            "✅ Practice: Create a `Book` class with `title` and `author`.",
                        ],
                    ),
                    make_text(
                        "Methods, self, and state",
                        2,
                        2,
                        [
                            "# Methods & `self`",
                            "",
                            "`self` is the current instance.",
                            "```py",
                            "class Counter:",
                            "    def __init__(self):",
                            "        self.value = 0",
                            "    def inc(self):",
                            "        self.value += 1",
                            "```",
                            "",
                            "✅ Practice: add `dec()` and `reset()`.",
                        ],
                    ),
                ],
            },
            {
                "title": "Inheritance & Composition",
                "sort_order": 2,
                "lessons": [
                    make_text(
                        "Inheritance (when to use it)",
                        2,
                        1,
                        [
                            "# Inheritance",
                            "",
                            "Use inheritance to express **is-a** relationships.",
                            "```py",
                            "class Animal:",
                            "    def speak(self):",
                            "        return '...'",
                            "",
                            "class Dog(Animal):",
                            "    def speak(self):",
                            "        return 'woof'",
                            "```",
                            "",
                            "✅ Practice: Make `Cat` and override `speak()`.",
                        ],
                    ),
                    make_text(
                        "Composition (often better)",
                        3,
                        2,
                        [
                            "# Composition",
                            "",
                            "Composition is **has-a** relationships.",
                            "Example: `Car` has an `Engine`.",
                            "",
                            "Composition is often more flexible than inheritance.",
                            "",
                            "✅ Practice: Create `Car` + `Engine` objects.",
                        ],
                    ),
                ],
            },
            {
                "title": "Clean Design",
                "sort_order": 3,
                "lessons": [
                    make_text(
                        "Encapsulation & Properties",
                        3,
                        1,
                        [
                            "# Encapsulation",
                            "",
                            "Protect internal state and provide safe methods:",
                            "```py",
                            "class BankAccount:",
                            "    def __init__(self):",
                            "        self._balance = 0",
                            "    def deposit(self, amount):",
                            "        if amount > 0:",
                            "            self._balance += amount",
                            "```",
                            "",
                            "✅ Practice: add `withdraw()` with validation.",
                        ],
                    ),
                    make_text(
                        "Basic Patterns (Factory idea)",
                        3,
                        2,
                        [
                            "# Basic Patterns",
                            "",
                            "Patterns are reusable designs. Example: a simple factory function.",
                            "```py",
                            "def make_user(role):",
                            "    if role == 'admin':",
                            "        return {'role':'admin'}",
                            "    return {'role':'user'}",
                            "```",
                            "",
                            "✅ Practice: Convert to class-based factory.",
                        ],
                    ),
                    make_quiz(
                        "Final Quiz: Python OOP",
                        3,
                        3,
                        [
                            {
                                "q": "What is `self`?",
                                "options": ["The module", "The current instance", "The parent class", "A global variable"],
                                "answerIndex": 1,
                                "explain": "`self` refers to the instance the method is called on.",
                            },
                            {
                                "q": "Inheritance is best for…",
                                "options": ["has-a relationship", "is-a relationship", "random reuse", "file handling"],
                                "answerIndex": 1,
                                "explain": "Inheritance models is-a relationships.",
                            },
                            {
                                "q": "Composition is best for…",
                                "options": ["is-a relationship", "has-a relationship", "loops", "printing"],
                                "answerIndex": 1,
                                "explain": "Composition models has-a relationships.",
                            },
                            {
                                "q": "Encapsulation means…",
                                "options": ["Hiding internal state + exposing safe methods", "Making everything public", "Removing classes", "Using only dicts"],
                                "answerIndex": 0,
                                "explain": "Encapsulation protects state and controls access.",
                            },
                        ],
                    ),
                ],
            },
        ],
    ),

    # 3) Data Structures in Python
    course_template(
        "Data Structures in Python",
        "Master lists, stacks, queues, sets, dicts, and how to choose the right structure.",
        [
            {
                "title": "Core Structures",
                "sort_order": 1,
                "lessons": [
                    make_text(
                        "Lists & Tuples",
                        2,
                        1,
                        [
                            "# Lists & Tuples",
                            "",
                            "Lists are mutable; tuples are immutable.",
                            "```py",
                            "a = [1,2,3]",
                            "b = (1,2,3)",
                            "```",
                            "",
                            "Use tuple for fixed data (e.g., coordinates).",
                        ],
                    ),
                    make_text(
                        "Sets & Dicts",
                        2,
                        2,
                        [
                            "# Sets & Dicts",
                            "",
                            "Sets are unique items:",
                            "```py",
                            "s = {1,2,2,3}  # {1,2,3}",
                            "```",
                            "",
                            "Dicts map keys to values:",
                            "```py",
                            "d = {'a':1, 'b':2}",
                            "```",
                        ],
                    ),
                ],
            },
            {
                "title": "Choosing the Right Tool",
                "sort_order": 2,
                "lessons": [
                    make_text(
                        "Big-O intuition",
                        3,
                        1,
                        [
                            "# Big-O intuition",
                            "",
                            "You don’t need to be a mathematician — just learn how operations scale.",
                            "",
                            "- list search is often O(n)",
                            "- dict lookup is often O(1) average",
                            "",
                            "Practical rule: choose structure based on the **operation you do most**.",
                        ],
                    ),
                    make_text(
                        "Common patterns",
                        3,
                        2,
                        [
                            "# Common patterns",
                            "",
                            "Patterns you will use constantly:",
                            "- counting frequencies with dict",
                            "- deduping with set",
                            "- ordering with list + sort",
                            "",
                            "Mini task: count word frequency in a sentence.",
                        ],
                    ),
                ],
            },
            {
                "title": "Real Use Cases",
                "sort_order": 3,
                "lessons": [
                    make_text(
                        "Stacks & Queues (simple)",
                        3,
                        1,
                        [
                            "# Stacks & Queues",
                            "",
                            "Stack = LIFO (last in first out).",
                            "Queue = FIFO (first in first out).",
                            "",
                            "Python stack with list:",
                            "```py",
                            "stack = []",
                            "stack.append(1)",
                            "stack.pop()",
                            "```",
                        ],
                    ),
                    make_quiz(
                        "Final Quiz: Data Structures",
                        3,
                        2,
                        [
                            {
                                "q": "Best structure for unique values?",
                                "options": ["list", "tuple", "set", "dict"],
                                "answerIndex": 2,
                                "explain": "A set stores unique elements.",
                            },
                            {
                                "q": "Average dict lookup complexity is often…",
                                "options": ["O(1)", "O(n)", "O(n^2)", "O(log n) always"],
                                "answerIndex": 0,
                                "explain": "Hash tables usually give O(1) average lookup.",
                            },
                            {
                                "q": "Stack is…",
                                "options": ["FIFO", "LIFO", "Random", "Sorted"],
                                "answerIndex": 1,
                                "explain": "Stack is LIFO.",
                            },
                        ],
                    ),
                ],
            },
        ],
    ),

    # 4) HTML & CSS Foundations
    course_template(
        "HTML & CSS Foundations",
        "Build modern webpages: semantic HTML, layouts, responsive design, and accessibility basics.",
        [
            {
                "title": "HTML Essentials",
                "sort_order": 1,
                "lessons": [
                    make_text(
                        "Semantic HTML",
                        1,
                        1,
                        [
                            "# Semantic HTML",
                            "",
                            "Semantic tags improve SEO + accessibility:",
                            "- `<header> <main> <section> <article> <footer>`",
                            "",
                            "Example structure:",
                            "```html",
                            "<main>",
                            "  <section>",
                            "    <h1>Title</h1>",
                            "    <p>Text...</p>",
                            "  </section>",
                            "</main>",
                            "```",
                        ],
                    ),
                    make_text(
                        "Forms & Inputs",
                        2,
                        2,
                        [
                            "# Forms & Inputs",
                            "",
                            "Forms collect data.",
                            "```html",
                            "<form>",
                            "  <input type='email' />",
                            "  <button>Submit</button>",
                            "</form>",
                            "```",
                            "",
                            "✅ Always use labels for accessibility.",
                        ],
                    ),
                ],
            },
            {
                "title": "CSS Layout",
                "sort_order": 2,
                "lessons": [
                    make_text(
                        "Flexbox (everyday layout)",
                        2,
                        1,
                        [
                            "# Flexbox",
                            "",
                            "Used for rows/columns alignment:",
                            "```css",
                            ".row { display:flex; gap:12px; align-items:center; }",
                            "```",
                            "",
                            "Common properties: `justify-content`, `align-items`, `gap`.",
                        ],
                    ),
                    make_text(
                        "Grid + Responsive",
                        2,
                        2,
                        [
                            "# Grid + Responsive Design",
                            "",
                            "Grid is perfect for 2D layout.",
                            "```css",
                            ".grid { display:grid; grid-template-columns: repeat(3, 1fr); gap:16px; }",
                            "@media (max-width: 800px) { .grid { grid-template-columns: 1fr; } }",
                            "```",
                        ],
                    ),
                ],
            },
            {
                "title": "Accessibility & Polish",
                "sort_order": 3,
                "lessons": [
                    make_text(
                        "Accessibility basics",
                        2,
                        1,
                        [
                            "# Accessibility basics",
                            "",
                            "- Use contrast",
                            "- Use labels for inputs",
                            "- Use semantic tags",
                            "- Keyboard navigation matters",
                        ],
                    ),
                    make_quiz(
                        "Final Quiz: HTML & CSS",
                        2,
                        2,
                        [
                            {
                                "q": "Why use semantic HTML?",
                                "options": ["Makes pages heavier", "Helps SEO & accessibility", "Removes CSS", "Stops JavaScript"],
                                "answerIndex": 1,
                                "explain": "Semantic tags help screen readers and search engines.",
                            },
                            {
                                "q": "Best tool for one-dimensional layout?",
                                "options": ["Grid", "Flexbox", "Canvas", "SQL"],
                                "answerIndex": 1,
                                "explain": "Flexbox is great for rows/columns alignment.",
                            },
                        ],
                    ),
                ],
            },
        ],
    ),

    # 5) JavaScript Fundamentals
    course_template(
        "JavaScript Fundamentals",
        "Core JavaScript: variables, functions, DOM, async basics, and clean coding habits.",
        [
            {
                "title": "Language Basics",
                "sort_order": 1,
                "lessons": [
                    make_text(
                        "Variables & Types (JS)",
                        1,
                        1,
                        [
                            "# JS Variables & Types",
                            "",
                            "`let` and `const` are modern.",
                            "```js",
                            "const name = 'Cristian';",
                            "let count = 0;",
                            "```",
                            "",
                            "Avoid `var` unless you know why.",
                        ],
                    ),
                    make_text(
                        "Functions & Arrays",
                        1,
                        2,
                        [
                            "# Functions & Arrays",
                            "",
                            "```js",
                            "function add(a,b){ return a+b; }",
                            "const nums = [1,2,3];",
                            "nums.map(x => x*2);",
                            "```",
                        ],
                    ),
                ],
            },
            {
                "title": "DOM & Events",
                "sort_order": 2,
                "lessons": [
                    make_text(
                        "DOM basics",
                        2,
                        1,
                        [
                            "# DOM basics",
                            "",
                            "The DOM is the browser document tree.",
                            "```js",
                            "const btn = document.querySelector('button');",
                            "btn.addEventListener('click', () => alert('Hi'));",
                            "```",
                        ],
                    ),
                    make_text(
                        "Fetch & JSON",
                        2,
                        2,
                        [
                            "# Fetch & JSON",
                            "",
                            "```js",
                            "const res = await fetch('/api');",
                            "const data = await res.json();",
                            "```",
                            "",
                            "Common errors: CORS, wrong URL, missing headers.",
                        ],
                    ),
                ],
            },
            {
                "title": "Async & Quality",
                "sort_order": 3,
                "lessons": [
                    make_text(
                        "Promises & async/await",
                        2,
                        1,
                        [
                            "# async/await",
                            "",
                            "```js",
                            "async function load(){",
                            "  const res = await fetch('/data');",
                            "  return await res.json();",
                            "}",
                            "```",
                        ],
                    ),
                    make_quiz(
                        "Final Quiz: JavaScript Fundamentals",
                        2,
                        2,
                        [
                            {
                                "q": "Which keyword declares a constant?",
                                "options": ["let", "const", "var", "fixed"],
                                "answerIndex": 1,
                                "explain": "`const` declares a constant binding.",
                            },
                            {
                                "q": "How do you parse JSON from a fetch response?",
                                "options": ["res.text()", "res.json()", "JSON.parse(res)", "res.parse()"],
                                "answerIndex": 1,
                                "explain": "Use `await res.json()`.",
                            },
                        ],
                    ),
                ],
            },
        ],
    ),

    # 6) React Essentials
    course_template(
        "React Essentials",
        "Build modern frontends with components, state, effects, and clean UI patterns.",
        [
            {
                "title": "React Basics",
                "sort_order": 1,
                "lessons": [
                    make_text(
                        "Components & Props",
                        2,
                        1,
                        [
                            "# Components & Props",
                            "",
                            "Components are UI building blocks.",
                            "```jsx",
                            "function Card({title}){ return <h3>{title}</h3>; }",
                            "```",
                        ],
                    ),
                    make_text(
                        "State (useState)",
                        2,
                        2,
                        [
                            "# State",
                            "",
                            "```jsx",
                            "const [count, setCount] = useState(0);",
                            "```",
                            "",
                            "State updates cause re-render.",
                        ],
                    ),
                ],
            },
            {
                "title": "Effects & Data",
                "sort_order": 2,
                "lessons": [
                    make_text(
                        "useEffect",
                        2,
                        1,
                        [
                            "# useEffect",
                            "",
                            "Runs after render — perfect for fetching data.",
                            "```jsx",
                            "useEffect(() => { load(); }, []);",
                            "```",
                        ],
                    ),
                    make_text(
                        "Forms & controlled inputs",
                        2,
                        2,
                        [
                            "# Forms",
                            "",
                            "Controlled input:",
                            "```jsx",
                            "const [email, setEmail] = useState('');",
                            "<input value={email} onChange={e=>setEmail(e.target.value)} />",
                            "```",
                        ],
                    ),
                ],
            },
            {
                "title": "UI Patterns",
                "sort_order": 3,
                "lessons": [
                    make_text(
                        "Loading states & errors",
                        3,
                        1,
                        [
                            "# Loading & errors",
                            "",
                            "A real app always handles:",
                            "- loading states",
                            "- empty states",
                            "- errors",
                        ],
                    ),
                    make_quiz(
                        "Final Quiz: React Essentials",
                        3,
                        2,
                        [
                            {
                                "q": "What triggers a re-render?",
                                "options": ["console.log", "state update", "CSS change only", "HTML comment"],
                                "answerIndex": 1,
                                "explain": "Updating state triggers re-render.",
                            },
                            {
                                "q": "What is `useEffect` used for most commonly?",
                                "options": ["Styling", "Side effects like fetching data", "Defining routes", "SQL queries"],
                                "answerIndex": 1,
                                "explain": "useEffect handles side effects such as data fetching.",
                            },
                        ],
                    ),
                ],
            },
        ],
    ),

    # 7) FastAPI APIs
    course_template(
        "FastAPI API Development",
        "Build backend APIs with routing, validation, database sessions, and auth-aware endpoints.",
        [
            {
                "title": "FastAPI Core",
                "sort_order": 1,
                "lessons": [
                    make_text(
                        "Routes & Status Codes",
                        2,
                        1,
                        [
                            "# Routes & Status Codes",
                            "",
                            "```py",
                            "@app.get('/ping', status_code=200)",
                            "def ping(): return {'ok': True}",
                            "```",
                            "",
                            "Use correct status codes for professional APIs.",
                        ],
                    ),
                    make_text(
                        "Schemas (Pydantic)",
                        2,
                        2,
                        [
                            "# Pydantic Schemas",
                            "",
                            "```py",
                            "class UserIn(BaseModel):",
                            "    email: str",
                            "    password: str",
                            "```",
                        ],
                    ),
                ],
            },
            {
                "title": "Database Integration",
                "sort_order": 2,
                "lessons": [
                    make_text(
                        "DB sessions with dependency",
                        3,
                        1,
                        [
                            "# DB Sessions",
                            "",
                            "You already have:",
                            "- `engine`, `SessionLocal`",
                            "- `get_db()` generator",
                            "",
                            "This is the standard pattern in FastAPI.",
                        ],
                    ),
                    make_text(
                        "CRUD patterns",
                        3,
                        2,
                        [
                            "# CRUD Patterns",
                            "",
                            "Standard endpoints:",
                            "- list",
                            "- get by id",
                            "- create",
                            "- update",
                            "- delete",
                        ],
                    ),
                ],
            },
            {
                "title": "Auth & Security",
                "sort_order": 3,
                "lessons": [
                    make_text(
                        "JWT basics",
                        3,
                        1,
                        [
                            "# JWT Basics",
                            "",
                            "JWT lets your frontend authenticate API calls.",
                            "Your frontend stores token in localStorage and sends `Authorization: Bearer ...`",
                        ],
                    ),
                    make_quiz(
                        "Final Quiz: FastAPI API Development",
                        3,
                        2,
                        [
                            {
                                "q": "FastAPI uses which library for validation?",
                                "options": ["pydantic", "numpy", "requests", "pytest"],
                                "answerIndex": 0,
                                "explain": "FastAPI uses Pydantic models for validation.",
                            },
                            {
                                "q": "Where does the JWT token go in requests?",
                                "options": ["Query string only", "Cookie only", "Authorization header", "HTML title"],
                                "answerIndex": 2,
                                "explain": "Authorization: Bearer <token>.",
                            },
                        ],
                    ),
                ],
            },
        ],
    ),
]


def add_course(title, description, lesson_topics, quiz_questions):
    """
    lesson_topics: list of tuples for 3 modules * 2 lessons => 6 topics.
    quiz_questions: list of dicts (q/options/answerIndex/explain).
    """
    return course_template(
        title,
        description,
        [
            {
                "title": "Core Concepts",
                "sort_order": 1,
                "lessons": [
                    make_text(lesson_topics[0][0], lesson_topics[0][1], 1, lesson_topics[0][2]),
                    make_text(lesson_topics[1][0], lesson_topics[1][1], 2, lesson_topics[1][2]),
                ],
            },
            {
                "title": "Practical Skills",
                "sort_order": 2,
                "lessons": [
                    make_text(lesson_topics[2][0], lesson_topics[2][1], 1, lesson_topics[2][2]),
                    make_text(lesson_topics[3][0], lesson_topics[3][1], 2, lesson_topics[3][2]),
                ],
            },
            {
                "title": "Project & Checkpoint",
                "sort_order": 3,
                "lessons": [
                    make_text(lesson_topics[4][0], lesson_topics[4][1], 1, lesson_topics[4][2]),
                    make_text(lesson_topics[5][0], lesson_topics[5][1], 2, lesson_topics[5][2]),
                    make_quiz(f"Final Quiz: {title}", 3, 3, quiz_questions),
                ],
            },
        ],
    )


COURSES += [
    add_course(
        "SQL & PostgreSQL Mastery",
        "Design databases, write real queries, understand joins, indexes, and transactions.",
        [
            ("Tables, Keys & Relationships", 2, ["# Tables, Keys & Relationships", "", "- primary keys", "- foreign keys", "- normalization idea", "", "Mini: model Courses → Modules → Lessons."]),
            ("SELECT, WHERE, ORDER BY", 2, ["# SELECT basics", "", "```sql", "SELECT * FROM courses WHERE title ILIKE '%python%';", "```"]),
            ("Joins (INNER/LEFT)", 3, ["# Joins", "", "```sql", "SELECT c.title, m.title", "FROM courses c", "JOIN modules m ON m.course_id=c.id;", "```"]),
            ("Aggregations (COUNT/GROUP BY)", 3, ["# Aggregations", "", "```sql", "SELECT course_id, COUNT(*)", "FROM modules GROUP BY course_id;", "```"]),
            ("Indexes & Performance", 3, ["# Indexes", "", "Indexes speed up reads but cost writes. Use them on columns used in WHERE/JOIN."]),
            ("Transactions & Integrity", 3, ["# Transactions", "", "Use transactions to keep data consistent (all succeed or rollback)."]),
        ],
        [
            {"q": "What does a foreign key do?", "options": ["Encrypts data", "Links a row to another table", "Deletes tables", "Makes queries slower always"], "answerIndex": 1, "explain": "FK enforces a relationship to another table."},
            {"q": "Which join keeps rows from the left table even without matches?", "options": ["INNER", "LEFT", "RIGHT only", "CROSS only"], "answerIndex": 1, "explain": "LEFT JOIN keeps left rows."},
            {"q": "Why add an index?", "options": ["To format SQL", "To speed up lookups on common filters/joins", "To remove tables", "To break queries"], "answerIndex": 1, "explain": "Indexes speed up reads for specific access patterns."},
        ],
    ),
    add_course(
        "Git & GitHub Workflow",
        "Real developer workflow: commits, branches, PRs, releases, and clean history.",
        [
            ("Commits that matter", 2, ["# Commits", "", "Good commits are small, meaningful, and described clearly.", "", "Example: `feat: add lesson viewer`"]),
            ("Branching strategy", 2, ["# Branching", "", "Use feature branches: `feature/quiz-ui`", "Merge via PR."]),
            ("Pull Requests & Code Review", 3, ["# PRs", "", "PRs communicate what changed, why, and how to test it."]),
            ("Merge conflicts", 3, ["# Conflicts", "", "Resolve by understanding intent, not by random choosing."]),
            ("Releases & tags", 3, ["# Releases", "", "Tag versions: `v1.0.0` and write release notes."]),
            ("Project hygiene", 3, ["# Hygiene", "", ".gitignore, README, env examples, consistent formatting."]),
        ],
        [
            {"q": "Best description of a good commit?", "options": ["Huge changes in one commit", "Small change with clear message", "No message", "Only screenshots"], "answerIndex": 1, "explain": "Small + meaningful + clear message wins."},
            {"q": "Why use feature branches?", "options": ["To break builds", "To isolate work and review safely", "To delete history", "To avoid collaboration"], "answerIndex": 1, "explain": "Branches isolate work and enable PR review."},
            {"q": "What is a merge conflict?", "options": ["Virus", "Two changes touch same lines differently", "Slow internet", "Bad monitor"], "answerIndex": 1, "explain": "Conflict happens when Git can’t auto-merge edits."},
        ],
    ),
    add_course(
        "Linux for Developers",
        "Command line, processes, permissions, SSH, and real-world troubleshooting.",
        [
            ("Filesystem & navigation", 2, ["# Navigation", "", "`ls`, `cd`, `pwd`, `cat`, `less`", "", "Practice: explore project folders quickly."]),
            ("Permissions (chmod/chown)", 3, ["# Permissions", "", "rwx for user/group/other. Understand 755 vs 644."]),
            ("Processes & services", 3, ["# Processes", "", "`ps`, `top`, `kill`, services. Find what runs on port 8000."]),
            ("Networking basics", 3, ["# Networking", "", "`curl`, `ping`, `netstat`, `ss`", "", "Check if backend is reachable."]),
            ("SSH & keys", 3, ["# SSH", "", "Use keys not passwords for production servers."]),
            ("Debug checklist", 3, ["# Debug checklist", "", "Logs → ports → env vars → permissions → DNS"]),
        ],
        [
            {"q": "What does `chmod 755 file` typically mean?", "options": ["Everyone can write", "Owner rwx, others rx", "No one can execute", "It deletes file"], "answerIndex": 1, "explain": "755 = owner rwx, group rx, other rx."},
            {"q": "Command to see running processes?", "options": ["mkdir", "ps", "rm", "echo"], "answerIndex": 1, "explain": "`ps` shows processes."},
        ],
    ),
    add_course(
        "Networking Basics for Web Apps",
        "Understand HTTP, ports, DNS, CORS, and how browsers talk to APIs.",
        [
            ("IP, ports, localhost", 2, ["# IP & Ports", "", "Frontend on 5173, backend on 8000. Ports matter."]),
            ("HTTP methods", 2, ["# HTTP", "", "GET/POST/PUT/DELETE + status codes like 200/401/404."]),
            ("DNS & domains", 3, ["# DNS", "", "Domain points to frontend; api subdomain points to backend."]),
            ("CORS explained", 3, ["# CORS", "", "Browser blocks cross-origin unless backend allows it."]),
            ("Cookies vs Bearer tokens", 3, ["# Auth transport", "", "Your platform uses Bearer tokens in Authorization header."]),
            ("Debugging requests", 3, ["# Debugging", "", "Use DevTools → Network tab: URL, status, headers, response."]),
        ],
        [
            {"q": "What is CORS?", "options": ["A database", "A browser security policy for cross-origin requests", "A CSS framework", "A Git feature"], "answerIndex": 1, "explain": "CORS controls cross-origin browser requests."},
            {"q": "Where does your API token go?", "options": ["URL hash", "Authorization header", "HTML body only", "DNS records"], "answerIndex": 1, "explain": "Authorization: Bearer <token>."},
        ],
    ),
    add_course(
        "Docker & Containers",
        "Run Postgres, deploy services, understand images, containers, volumes, networks.",
        [
            ("Images vs containers", 2, ["# Images vs Containers", "", "Image = blueprint, container = running instance."]),
            ("Volumes (persist data)", 3, ["# Volumes", "", "Use volumes for Postgres so data survives restarts."]),
            ("Networking (ports)", 3, ["# Ports", "", "5432:5432 maps container port to host."]),
            ("Compose basics", 3, ["# docker-compose", "", "Define db + backend together in one file."]),
            ("Environment variables", 3, ["# ENV", "", "DATABASE_URL points to postgres container host."]),
            ("Production mindset", 3, ["# Production", "", "Logs, restart policies, health checks."]),
        ],
        [
            {"q": "Why use volumes with Postgres?", "options": ["To speed CPU", "To persist database data", "To change Python version", "To hide ports"], "answerIndex": 1, "explain": "Volumes keep data persistent."},
            {"q": "What does `-p 5432:5432` do?", "options": ["Deletes DB", "Maps ports host:container", "Creates users", "Adds firewall"], "answerIndex": 1, "explain": "It maps host port 5432 to container port 5432."},
        ],
    ),
    add_course(
        "Cloud Deployment (Frontend + API)",
        "Deploy like a real product: Vercel/Netlify for frontend, Render/Railway for backend, Postgres managed.",
        [
            ("Deploy frontend", 2, ["# Frontend deploy", "", "Vercel/Netlify: build with Vite, set env `VITE_API_BASE`."]),
            ("Deploy backend", 3, ["# Backend deploy", "", "Render/Railway: start command `uvicorn app.main:app --host 0.0.0.0 --port $PORT`"]),
            ("Domains & subdomains", 3, ["# Domains", "", "Use `app.domain.com` for frontend and `api.domain.com` for backend."]),
            ("Env vars safely", 3, ["# Env vars", "", "Never commit secrets. Use platform env settings."]),
            ("CORS for prod", 3, ["# CORS", "", "Allow your frontend domain."]),
            ("Monitoring basics", 3, ["# Monitoring", "", "Logs, uptime checks, error tracking."]),
        ],
        [
            {"q": "Where should VITE_API_BASE point in production?", "options": ["localhost", "your api domain", "google.com", "a random IP"], "answerIndex": 1, "explain": "Frontend must call your real API domain."},
            {"q": "Why not commit secrets?", "options": ["It makes git slow", "Security risk", "It breaks CSS", "It changes UI"], "answerIndex": 1, "explain": "Secrets must stay private."},
        ],
    ),
    add_course(
        "Cybersecurity Fundamentals",
        "OWASP basics, passwords, input validation, auth, and safe deployment habits.",
        [
            ("Threat mindset", 2, ["# Threat mindset", "", "Assume inputs are hostile. Protect endpoints and data."]),
            ("Passwords & hashing", 3, ["# Hashing", "", "Never store raw passwords. Use bcrypt/argon2."]),
            ("Auth & permissions", 3, ["# Auth", "", "Auth = who are you. Authorization = what can you do."]),
            ("OWASP Top 10 (intro)", 3, ["# OWASP", "", "Injection, broken auth, sensitive data exposure, etc."]),
            ("API security checklist", 3, ["# Checklist", "", "Rate limiting, logging, validation, least privilege."]),
            ("Secure deployment", 3, ["# Secure deploy", "", "HTTPS, environment secrets, backups."]),
        ],
        [
            {"q": "Why hash passwords?", "options": ["To make login slower only", "To protect passwords if DB leaks", "To improve CSS", "To speed up SQL joins"], "answerIndex": 1, "explain": "Hashing protects passwords in case of data breach."},
            {"q": "Authorization means…", "options": ["Who you are", "What you are allowed to do", "How fast your internet is", "How many tables exist"], "answerIndex": 1, "explain": "Authorization controls permissions."},
        ],
    ),
    add_course(
        "Testing & QA (Python + Web)",
        "Write real tests with pytest, test APIs, and build confidence before deploying.",
        [
            ("Why tests matter", 2, ["# Why tests", "", "Tests prevent regressions and speed up change."]),
            ("pytest basics", 3, ["# pytest", "", "Arrange → Act → Assert. Test functions and edge cases."]),
            ("API testing", 3, ["# API tests", "", "Test status codes, payloads, auth required endpoints."]),
            ("Mocking basics", 3, ["# Mocking", "", "Mock external dependencies, focus on your logic."]),
            ("Frontend testing idea", 3, ["# Frontend tests", "", "Component tests + user flows."]),
            ("Quality checklist", 3, ["# Checklist", "", "Linting, formatting, tests passing, review."]),
        ],
        [
            {"q": "What is a regression?", "options": ["A new feature", "A bug returning after changes", "A CSS rule", "A database index"], "answerIndex": 1, "explain": "Regression is when an old bug comes back."},
            {"q": "AAA stands for…", "options": ["Add-Add-Add", "Arrange-Act-Assert", "All-At-Once", "Async-Await-API"], "answerIndex": 1, "explain": "Arrange, Act, Assert is a common test structure."},
        ],
    ),
    add_course(
        "UI/UX & Accessibility",
        "Design usable interfaces: hierarchy, spacing, UX writing, and accessibility basics.",
        [
            ("Visual hierarchy", 2, ["# Hierarchy", "", "Guide the eye: headings, spacing, contrast, alignment."]),
            ("Layout & spacing", 2, ["# Spacing", "", "Use consistent spacing scale and alignment grid."]),
            ("UX writing", 3, ["# UX writing", "", "Clear labels, helpful errors, friendly empty states."]),
            ("Accessibility basics", 3, ["# Accessibility", "", "Keyboard support, ARIA when necessary, contrast."]),
            ("Forms done right", 3, ["# Forms", "", "Labels, validation messages, success feedback."]),
            ("Polish checklist", 3, ["# Polish", "", "Loading states, error states, microcopy."]),
        ],
        [
            {"q": "Good UX error message should…", "options": ["Be vague", "Tell user what happened and how to fix", "Hide itself", "Blame the user"], "answerIndex": 1, "explain": "Clear errors reduce frustration."},
            {"q": "Accessibility helps…", "options": ["Only blind users", "Everyone in many situations", "Only designers", "Only backend devs"], "answerIndex": 1, "explain": "Accessibility improves usability for many users."},
        ],
    ),
    add_course(
        "Product & Agile Foundations",
        "Product thinking: MVP, feedback loops, agile planning, and measurable outcomes.",
        [
            ("Problem → solution fit", 2, ["# Problem first", "", "Start from user pain and define success metrics."]),
            ("MVP strategy", 3, ["# MVP", "", "Build the smallest thing that proves value."]),
            ("Agile basics", 3, ["# Agile", "", "Sprints, backlog, user stories, acceptance criteria."]),
            ("Prioritization", 3, ["# Priority", "", "Impact vs effort; focus on outcomes."]),
            ("Metrics & KPIs", 3, ["# Metrics", "", "Track retention, completion rate, engagement."]),
            ("Launch & iterate", 3, ["# Iterate", "", "Ship → measure → improve."]),
        ],
        [
            {"q": "MVP means…", "options": ["Maximum Value Project", "Minimum Viable Product", "Most Viral Product", "Minimum Verified Plan"], "answerIndex": 1, "explain": "Minimum Viable Product."},
            {"q": "Best way to improve product?", "options": ["Ignore users", "Ship and measure outcomes", "Add random features", "Stop tracking metrics"], "answerIndex": 1, "explain": "Measure outcomes and iterate."},
        ],
    ),
    add_course(
        "Data Analysis with pandas",
        "Load datasets, clean them, group, aggregate, and extract insight for decisions.",
        [
            ("Series & DataFrame", 2, ["# pandas basics", "", "DataFrame = table, Series = column.", "", "Load CSV and inspect."]),
            ("Cleaning data", 3, ["# Cleaning", "", "Handle missing values, types, duplicates."]),
            ("Groupby & aggregates", 3, ["# groupby", "", "Summarize data by categories and compute stats."]),
            ("Filtering & sorting", 3, ["# filter/sort", "", "Boolean masks and sorting by columns."]),
            ("Mini project workflow", 3, ["# mini project", "", "Question → data → clean → analysis → conclusion."]),
            ("Communicating results", 3, ["# communication", "", "Explain insights in plain English and charts."]),
        ],
        [
            {"q": "DataFrame is…", "options": ["A chart", "A table-like structure", "A Python keyword", "A database index"], "answerIndex": 1, "explain": "DataFrame is a table-like structure."},
            {"q": "What does groupby do?", "options": ["Deletes rows", "Groups rows by a key to aggregate", "Converts to JSON only", "Adds CSS styles"], "answerIndex": 1, "explain": "Groupby groups data to compute aggregates."},
        ],
    ),
    add_course(
        "Machine Learning Introduction",
        "Understand ML concepts: datasets, training/testing, evaluation, overfitting, basic models.",
        [
            ("What is ML?", 2, ["# What is ML?", "", "ML learns patterns from data to make predictions."]),
            ("Train/test split", 3, ["# Train/test", "", "You must evaluate on unseen data to avoid overfitting."]),
            ("Evaluation metrics", 3, ["# Metrics", "", "Accuracy, precision/recall, RMSE depending on problem."]),
            ("Overfitting vs generalization", 3, ["# Overfitting", "", "Model memorizes training data; fails on new data."]),
            ("Features & preprocessing", 3, ["# Features", "", "Good features matter more than fancy models."]),
            ("Simple models", 3, ["# Models", "", "Linear regression, logistic regression, decision trees."]),
        ],
        [
            {"q": "Overfitting means…", "options": ["Model learns general patterns", "Model memorizes training data", "Model is faster", "Model uses SQL"], "answerIndex": 1, "explain": "Overfitting is memorization leading to poor generalization."},
            {"q": "Why use a test set?", "options": ["To make training slower", "To evaluate on unseen data", "To delete labels", "To avoid CSS"], "answerIndex": 1, "explain": "Test set checks generalization."},
        ],
    ),
    add_course(
        "Business & Tech Foundations",
        "Connect business strategy with technology: data, security, product execution, transformation.",
        [
            ("Digital transformation", 2, ["# Transformation", "", "Tech changes processes, customer experience, and operations."]),
            ("Value chains & efficiency", 3, ["# Value", "", "Tech improves speed, quality, and cost."]),
            ("Data-driven decisions", 3, ["# Data", "", "Collect → analyze → act."]),
            ("Security & risk basics", 3, ["# Risk", "", "Understand threats and risk management."]),
            ("Product thinking", 3, ["# Product", "", "Solve real problems and measure outcomes."]),
            ("Case study approach", 3, ["# Case study", "", "Apply SWOT/PESTLE to a tech initiative."]),
        ],
        [
            {"q": "Digital transformation is mainly about…", "options": ["Buying random tools", "Changing how business works using tech", "Only hiring developers", "Only marketing"], "answerIndex": 1, "explain": "It changes operations and value creation using tech."},
            {"q": "Why use metrics?", "options": ["To look busy", "To measure outcomes and improve", "To replace users", "To stop iteration"], "answerIndex": 1, "explain": "Metrics guide improvement."},
        ],
    ),
]

# Ensure exactly 20 courses
assert len(COURSES) == 20, f"Expected 20 courses, got {len(COURSES)}"


# ----------------------------
# DB operations (safe reseed)
# ----------------------------
def delete_course_by_title(db, title: str):
    course = db.execute(select(models.Course).where(models.Course.title == title)).scalars().first()
    if not course:
        return

    modules = db.execute(select(models.Module).where(models.Module.course_id == course.id)).scalars().all()
    module_ids = [m.id for m in modules]

    lesson_ids = []
    if module_ids:
        lesson_ids = [lid for (lid,) in db.query(models.Lesson.id).filter(models.Lesson.module_id.in_(module_ids)).all()]

    # Delete progress first (avoids FK violations)
    if lesson_ids:
        db.query(models.Progress).filter(models.Progress.lesson_id.in_(lesson_ids)).delete(synchronize_session=False)

    # Then lessons/modules/course
    if module_ids:
        db.query(models.Lesson).filter(models.Lesson.module_id.in_(module_ids)).delete(synchronize_session=False)
        db.query(models.Module).filter(models.Module.course_id == course.id).delete(synchronize_session=False)

    db.query(models.Course).filter(models.Course.id == course.id).delete(synchronize_session=False)
    db.commit()


def seed_course(db, course_data: dict):
    c = models.Course(title=course_data["title"], description=course_data["description"])
    db.add(c)
    db.flush()
    db.refresh(c)

    for mod in course_data["modules"]:
        m = models.Module(course_id=c.id, title=mod["title"], sort_order=mod["sort_order"])
        db.add(m)
        db.flush()
        db.refresh(m)

        lesson_models = []
        for l in mod["lessons"]:
            lesson_models.append(
                models.Lesson(
                    module_id=m.id,
                    title=l["title"],
                    lesson_type=l["lesson_type"],
                    difficulty=l["difficulty"],
                    content=l.get("content"),
                    sort_order=l.get("sort_order", 0),
                )
            )
        db.add_all(lesson_models)

    db.commit()

def run_seed(db):
    """
    Called by FastAPI startup.
    Seeds (replaces) the 20 courses safely.
    """
    for course in COURSES:
        delete_course_by_title(db, course["title"])
        seed_course(db, course)

    print(f"Seeded {len(COURSES)} premium courses ✅")


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for course in COURSES:
            delete_course_by_title(db, course["title"])
            seed_course(db, course)
        print(f"Seeded {len(COURSES)} premium courses ✅")
    finally:
        db.close()


if __name__ == "__main__":
    run()
