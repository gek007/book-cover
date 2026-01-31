class Car:
    def __init__(self, make: str, model: str, year: int, color: str):
        self.make = make
        self.model = model
        self.year = year
        self.color = color

    # Instance method: operates on an instance (object) of the class. Can access and modify object attributes.
    def display_info(self):
        """Instance method. Use to display info about this specific car object."""
        print(f"{self.year} {self.color} {self.make} {self.model}")

    # Class method: operates on the class itself, not on a particular instance.
    @classmethod
    def from_string(cls, car_string: str):
        """
        Class method. Alternative constructor to create a Car from a string.
        Calls: Car.from_string("Toyota,Corolla,2018,Red")
        """
        make, model, year, color = car_string.split(",")
        return cls(make, model, int(year), color)

    # Static method: does not operate on class or instance, just utility tied to Car contextually.
    @staticmethod
    def is_valid_year(year: int) -> bool:
        """
        Static method. Does not access/change class or instance data.
        Usage: Car.is_valid_year(2020)
        """
        return 1886 <= year <= 2050  # 1886: first modern car

# === Explanation ===
# 1. Instance method: Called on an object. E.g.
#    mycar = Car("Honda", "Civic", 2020, "Blue")
#    mycar.display_info()  # prints info about mycar

# 2. Class method: Called on the class (not instance), usually used as alternative constructors, or when you need the class reference (cls).
#    car2 = Car.from_string("Ford,Mustang,1969,Yellow")
#    car2.display_info()

# 3. Static method: Utility function tied to the class, but no access to class/instance (no self/cls). Call as Car.is_valid_year(year) or mycar.is_valid_year(year).
#    print(Car.is_valid_year(1999))      # True
#    print(mycar.is_valid_year(1700))    # False