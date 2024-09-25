from panda3d.core import Point3, GeoMipTerrain, Filename
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import WindowProperties
import sys
import random

class WarSimulator(ShowBase):
    def __init__(self, map_file=None):
        super().__init__()

        # Disable the default camera controls
        self.disableMouse()

        # Set window title
        self.win.setTitle("3D War Simulator")

        # Load the map or create a simple flat terrain
        if map_file:
            # Load your real map here
            terrain = GeoMipTerrain("terrain")
            terrain.setHeightfield(Filename.fromOsSpecific(map_file))
            terrain.generate()
            self.terrain_node = terrain.getRoot()
            self.terrain_node.reparentTo(self.render)
        else:
            # Create a flat plane as ground
            self.ground = self.loader.loadModel("models/plane")
            self.ground.setScale(100, 100, 1)
            self.ground.setPos(0, 0, 0)
            self.ground.setColor(0.5, 0.8, 0.5, 1)
            self.ground.reparentTo(self.render)

        # Setup camera
        self.camera.setPos(0, -150, 100)
        self.camera.setHpr(0, -30, 0)

        # Initialize lists to hold units and missiles
        self.ground_units = []
        self.planes = []
        self.missiles = []

        # Spawn some ground units
        for _ in range(10):
            unit = self.loader.loadModel("models/sphere")  # Represented by a sphere (dot)
            unit.setScale(1)
            unit.setPos(random.uniform(-50, 50), random.uniform(-50, 50), 1)
            unit.setColor(0, 0, 1, 1)  # Blue units
            unit.reparentTo(self.render)
            self.ground_units.append(unit)

        # Spawn some planes
        for _ in range(5):
            plane = self.loader.loadModel("models/arrow")  # Represented by a simple arrow (triangle)
            plane.setScale(2)
            plane.setPos(random.uniform(-80, 80), random.uniform(-80, 80), 20)
            plane.setHpr(random.uniform(0, 360), 0, 0)
            plane.setColor(1, 0, 0, 1)  # Red planes
            plane.reparentTo(self.render)
            self.planes.append(plane)

        # Add task to update the simulation
        self.taskMgr.add(self.update_simulation, "UpdateSimulation")

    def update_simulation(self, task):
        # Example: Move planes forward
        for plane in self.planes:
            h, p, r = plane.getHpr()
            # Simple forward movement
            dx = 0
            dy = 1
            dz = 0
            plane.setPos(plane, dx, dy, dz)
            # Randomly fire missiles
            if random.random() < 0.01:
                missile = self.loader.loadModel("models/missile")
                missile.setScale(0.5)
                missile.setPos(plane.getPos())
                missile.setColor(1, 1, 0, 1)  # Yellow missiles
                missile.reparentTo(self.render)
                missile.velocity = Point3(0, 2, 0)
                self.missiles.append(missile)

        # Update missiles
        for missile in self.missiles:
            missile.setPos(missile.getPos() + missile.velocity)

            # Check for collision with ground units
            for unit in self.ground_units:
                if (missile.getPos() - unit.getPos()).length() < 2:
                    unit.removeNode()
                    self.ground_units.remove(unit)
                    missile.removeNode()
                    self.missiles.remove(missile)
                    break

        return Task.cont

if __name__ == "__main__":
    app = WarSimulator()
    app.run()