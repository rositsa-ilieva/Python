class Material:
    DENSITIES = {"Concrete": 2500, "Brick": 2000, "Stone": 1600, "Wood": 600, "Steel": 7700}

    def __init__(self, mass):
        if not isinstance(mass, int):
            raise TypeError("Mass should be an integer.")
        self.mass = mass
        self.used = False
        self.components = [type(self).__name__]

    @property
    def volume(self):
        return float(self.mass / self.density)


class Concrete(Material):
    density = Material.DENSITIES["Concrete"]


class Brick(Material):
    density = Material.DENSITIES["Brick"]


class Stone(Material):
    density = Material.DENSITIES["Stone"]


class Wood(Material):
    density = Material.DENSITIES["Wood"]


class Steel(Material):
    density = Material.DENSITIES["Steel"]


class Factory:
    ACCESS_CLASS = {"Concrete": Concrete, "Brick": Brick,
                    "Stone": Stone, "Wood": Wood, "Steel": Steel}
    dynamic_classes = {}
    all_materials = []

    def __init__(self):
        self.materials = []

    def __call__(self, *args, **kwargs):
        if (args and kwargs) or (not args and not kwargs):
            raise ValueError("Input error for factory arguments.")
        if kwargs:
            return self.create_materials_from_kwargs(kwargs)
        elif args:
            return self.create_alloy_from_args(args)

    def create_materials_from_kwargs(self, kwargs):
        instance = []
        for class_name, mass in kwargs.items():
            if class_name not in self.ACCESS_CLASS:
                raise ValueError("Invalid material name.")
            cls = self.ACCESS_CLASS[class_name]
            material = cls(mass)
            instance.append(material)
            self.materials.append(material)
            self.all_materials.append(material)
        return tuple(instance)

    def create_alloy_from_args(self, args):
        if any(arg.used for arg in args) or any(not isinstance(arg, Material) for arg in args):
            raise AssertionError("Materials have already been used or are invalid.")

        used_materials = []
        for arg in args:
            if isinstance(arg, Material):
                for component in arg.components:
                    if "_" in component:
                        used_materials.extend(component.split("_"))
                    else:
                        used_materials.append(component)
            else:
                raise ValueError("Invalid argument type.")
            
        class_name = "_".join(sorted(set(used_materials)))
        mass = sum(arg.mass for arg in args)

        if class_name not in self.dynamic_classes:
            all_densities = [self.ACCESS_CLASS[comp].density if comp in self.ACCESS_CLASS else self.dynamic_classes[comp].density
                             for comp in set(used_materials)]
            average_density = sum(all_densities) / len(all_densities)
            dynamic_class = type(class_name, (Material,), {'density': average_density})
            self.dynamic_classes[class_name] = dynamic_class
        else:
            dynamic_class = self.dynamic_classes[class_name]

        new_material = dynamic_class(mass)
        self.materials.append(new_material)
        self.all_materials.append(new_material)

        for arg in args:
            arg.used = True

        return new_material

    def can_build(self, required_volume):
        return sum(material.volume for material in self.materials if not material.used) >= required_volume

    @classmethod
    def can_build_together(cls, required_volume):
        return sum(material.volume for material in cls.all_materials if not material.used) >= required_volume
