#!/usr/bin/env python3
"""
TeachScript Educational Libraries

Provides specialized libraries for TeachScript:
- TSGraphics: Simple graphics and drawing
- TSGame: Game development
- TSMath: Advanced math functions
- TSAnimation: Animation and movement
- TSSound: Audio and sound effects (stub)
- TSNetwork: Basic networking (stub)
"""

import math
import random
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Tuple

# ============================================================================
# Color Definitions
# ============================================================================


class Color(Enum):
    """Predefined colors for graphics."""

    RED = "#FF0000"
    GREEN = "#00FF00"
    BLUE = "#0000FF"
    BLACK = "#000000"
    WHITE = "#FFFFFF"
    YELLOW = "#FFFF00"
    CYAN = "#00FFFF"
    MAGENTA = "#FF00FF"
    ORANGE = "#FFA500"
    PURPLE = "#800080"
    PINK = "#FFC0CB"
    GRAY = "#808080"
    BROWN = "#A52A2A"


# ============================================================================
# Graphics Library
# ============================================================================


@dataclass
class Point:
    """A point in 2D space."""

    x: float
    y: float

    def distance_to(self, other: "Point") -> float:
        """Calculate distance to another point."""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Point":
        return Point(self.x * scalar, self.y * scalar)


class Rectangle:
    """A rectangle shape."""

    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def contains_point(self, point: Point) -> bool:
        """Check if a point is inside the rectangle."""
        return (
            self.x <= point.x <= self.x + self.width
            and self.y <= point.y <= self.y + self.height
        )

    def intersects(self, other: "Rectangle") -> bool:
        """Check if this rectangle intersects another."""
        return (
            self.x < other.x + other.width
            and self.x + self.width > other.x
            and self.y < other.y + other.height
            and self.y + self.height > other.y
        )


class Circle:
    """A circle shape."""

    def __init__(self, center: Point, radius: float):
        self.center = center
        self.radius = radius

    def contains_point(self, point: Point) -> bool:
        """Check if a point is inside the circle."""
        return self.center.distance_to(point) <= self.radius

    def intersects(self, other: "Circle") -> bool:
        """Check if this circle intersects another."""
        distance = self.center.distance_to(other.center)
        return distance < self.radius + other.radius


class TeachScriptGraphics:
    """Graphics library for TeachScript."""

    @staticmethod
    def create_point(x: float, y: float) -> Point:
        """Create a point."""
        return Point(x, y)

    @staticmethod
    def create_rectangle(x: float, y: float, width: float, height: float) -> Rectangle:
        """Create a rectangle."""
        return Rectangle(x, y, width, height)

    @staticmethod
    def create_circle(x: float, y: float, radius: float) -> Circle:
        """Create a circle."""
        return Circle(Point(x, y), radius)

    @staticmethod
    def point_distance(p1: Point, p2: Point) -> float:
        """Calculate distance between two points."""
        return p1.distance_to(p2)

    @staticmethod
    def rectangle_area(rect: Rectangle) -> float:
        """Calculate rectangle area."""
        return rect.width * rect.height

    @staticmethod
    def circle_area(circle: Circle) -> float:
        """Calculate circle area."""
        return math.pi * circle.radius**2

    @staticmethod
    def circle_circumference(circle: Circle) -> float:
        """Calculate circle circumference."""
        return 2 * math.pi * circle.radius

    @staticmethod
    def color(name: str) -> str:
        """Get color by name."""
        try:
            return Color[name.upper()].value
        except KeyError:
            return "#000000"  # Default to black


# ============================================================================
# Game Library
# ============================================================================


@dataclass
class GameObject:
    """A game object."""

    name: str
    position: Point
    velocity: Optional[Point] = None
    width: float = 10
    height: float = 10
    active: bool = True

    def __post_init__(self):
        if self.velocity is None:
            self.velocity = Point(0, 0)

    def update(self, dt: float = 0.016):
        """Update object position."""
        if self.active:
            self.position = self.position + (self.velocity * dt)

    def get_bounds(self) -> Rectangle:
        """Get bounding rectangle."""
        return Rectangle(
            self.position.x - self.width / 2,
            self.position.y - self.height / 2,
            self.width,
            self.height,
        )

    def collides_with(self, other: "GameObject") -> bool:
        """Check collision with another object."""
        return self.get_bounds().intersects(other.get_bounds())


class TeachScriptGame:
    """Game library for TeachScript."""

    def __init__(self):
        """Initialize game library."""
        self.objects: List[GameObject] = []
        self.running = False
        self.score = 0
        self.level = 1
        self.input_state: Dict[str, bool] = {}

    def create_object(
        self, name: str, x: float, y: float, width: float = 10, height: float = 10
    ) -> GameObject:
        """Create a game object."""
        obj = GameObject(name, Point(x, y), width=width, height=height)
        self.objects.append(obj)
        return obj

    def remove_object(self, obj: GameObject):
        """Remove a game object."""
        if obj in self.objects:
            self.objects.remove(obj)

    def update_all(self, dt: float = 0.016):
        """Update all game objects."""
        for obj in self.objects:
            obj.update(dt)

    def check_collisions(self) -> List[Tuple[GameObject, GameObject]]:
        """Check for collisions between all objects."""
        collisions = []
        for i, obj1 in enumerate(self.objects):
            for obj2 in self.objects[i + 1 :]:
                if obj1.collides_with(obj2):
                    collisions.append((obj1, obj2))
        return collisions

    def add_score(self, amount: int):
        """Add to the score."""
        self.score += amount

    def set_level(self, level: int):
        """Set the current level."""
        self.level = level

    def get_active_objects(self) -> List[GameObject]:
        """Get all active objects."""
        return [obj for obj in self.objects if obj.active]


# ============================================================================
# Math Library
# ============================================================================


class TeachScriptMath:
    """Advanced math library for TeachScript."""

    # Constants
    PI = math.pi
    E = math.e
    TAU = 2 * math.pi
    GOLDEN_RATIO = (1 + math.sqrt(5)) / 2

    @staticmethod
    def sqrt(x: float) -> float:
        """Square root."""
        return math.sqrt(x)

    @staticmethod
    def power(base: float, exponent: float) -> float:
        """Raise to power."""
        return base**exponent

    @staticmethod
    def sin(x: float) -> float:
        """Sine (x in radians)."""
        return math.sin(x)

    @staticmethod
    def cos(x: float) -> float:
        """Cosine (x in radians)."""
        return math.cos(x)

    @staticmethod
    def tan(x: float) -> float:
        """Tangent (x in radians)."""
        return math.tan(x)

    @staticmethod
    def log(x: float, base: float = math.e) -> float:
        """Logarithm."""
        return math.log(x, base)

    @staticmethod
    def factorial(n: int) -> int:
        """Factorial."""
        return math.factorial(n)

    @staticmethod
    def gcd(a: int, b: int) -> int:
        """Greatest common divisor."""
        return math.gcd(a, b)

    @staticmethod
    def lcm(a: int, b: int) -> int:
        """Least common multiple."""
        return abs(a * b) // math.gcd(a, b)

    @staticmethod
    def is_prime(n: int) -> bool:
        """Check if number is prime."""
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def fibonacci(n: int) -> int:
        """Get nth Fibonacci number."""
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

    @staticmethod
    def degrees_to_radians(degrees: float) -> float:
        """Convert degrees to radians."""
        return math.radians(degrees)

    @staticmethod
    def radians_to_degrees(radians: float) -> float:
        """Convert radians to degrees."""
        return math.degrees(radians)


# ============================================================================
# Animation Library
# ============================================================================


class Animation:
    """Base class for animations."""

    def __init__(self, duration: float):
        """Initialize animation."""
        self.duration = duration
        self.elapsed: float = 0.0
        self.completed = False

    def update(self, dt: float):
        """Update animation."""
        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.completed = True

    def get_progress(self) -> float:
        """Get animation progress (0.0 to 1.0)."""
        return min(self.elapsed / self.duration, 1.0)


class LinearAnimation(Animation):
    """Linear interpolation animation."""

    def __init__(self, start: float, end: float, duration: float):
        super().__init__(duration)
        self.start = start
        self.end = end

    def get_value(self) -> float:
        """Get current interpolated value."""
        progress = self.get_progress()
        return self.start + (self.end - self.start) * progress


class EaseInOutAnimation(Animation):
    """Ease-in-out animation."""

    def __init__(self, start: float, end: float, duration: float):
        super().__init__(duration)
        self.start = start
        self.end = end

    def get_value(self) -> float:
        """Get current interpolated value with easing."""
        progress = self.get_progress()
        # Ease-in-out cubic
        if progress < 0.5:
            t = 2 * progress
            eased = 0.5 * t * t * t
        else:
            t = 2 * (progress - 1)
            eased = 0.5 * (t * t * t + 2)
        return self.start + (self.end - self.start) * eased


class TeachScriptAnimation:
    """Animation library for TeachScript."""

    @staticmethod
    def create_linear_animation(
        start: float, end: float, duration: float
    ) -> LinearAnimation:
        """Create a linear animation."""
        return LinearAnimation(start, end, duration)

    @staticmethod
    def create_ease_animation(
        start: float, end: float, duration: float
    ) -> EaseInOutAnimation:
        """Create an eased animation."""
        return EaseInOutAnimation(start, end, duration)

    @staticmethod
    def delay(seconds: float):
        """Delay execution."""
        time.sleep(seconds)


# ============================================================================
# Random Library (Enhanced)
# ============================================================================


class TeachScriptRandom:
    """Random number library for TeachScript."""

    @staticmethod
    def random() -> float:
        """Random float between 0 and 1."""
        return random.random()

    @staticmethod
    def randint(a: int, b: int) -> int:
        """Random integer between a and b (inclusive)."""
        return random.randint(a, b)

    @staticmethod
    def choice(seq: List) -> Any:
        """Choose random element from sequence."""
        return random.choice(seq)

    @staticmethod
    def shuffle(seq: List) -> List:
        """Shuffle a sequence."""
        shuffled = seq.copy()
        random.shuffle(shuffled)
        return shuffled

    @staticmethod
    def sample(seq: List, k: int) -> List:
        """Sample k elements from sequence."""
        return random.sample(seq, min(k, len(seq)))

    @staticmethod
    def seed(value: int):
        """Set random seed."""
        random.seed(value)


# ============================================================================
# Export all libraries
# ============================================================================

__all__ = [
    "Color",
    "Point",
    "Rectangle",
    "Circle",
    "GameObject",
    "LinearAnimation",
    "EaseInOutAnimation",
    "TeachScriptGraphics",
    "TeachScriptGame",
    "TeachScriptMath",
    "TeachScriptAnimation",
    "TeachScriptRandom",
]
