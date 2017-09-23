from django.db import models

CONDITION = (
    (">", "mayor que (>)"),
    (">=", "mayor/igual que (>=)"),
    ("<", "menor que (<)"),
    ("<", "menor/igual que (<)"),
    ("==", "igual que (==)"),
)

STATUS_TASK = (
    ("SI", "Ejecutada"),
    ("NO", "No Ejecutada"),
)

class Device(models.Model):
    chip_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    @property
    def get_device_name(self):
        return "{}-{}".format(self.name, self.chip_id)

    def __str__(self):
        return self.get_device_name


class ActionInput(models.Model):
    name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    device = models.ForeignKey("devices.Device")

    @property
    def get_action_name(self):
        return "{} - {}".format(self.name, self.device.get_device_name)

    def __str__(self):
        return self.get_action_name


class ActionOutput(models.Model):
    name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    device = models.ForeignKey("devices.Device")

    @property
    def get_action_name(self):
        return "{} - {}".format(self.name, self.device.get_device_name)

    def __str__(self):
        return self.get_action_name


class ConfigTask(models.Model):
    action_input = models.ForeignKey("devices.ActionInput")
    action_output = models.ManyToManyField("devices.ActionOutput")
    condition = models.CharField(max_length=2, choices=CONDITION)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    notification = models.BooleanField(default=False)

    @property
    def get_name_task(self):
        return self.action_input.get_action_name

    def __str__(self):
        return self.get_name_task


class Task(models.Model):
    action = models.ForeignKey("devices.ActionOutput")
    device = models.ForeignKey("devices.Device")
    status = models.CharField(max_length=2, choices=STATUS_TASK)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def get_name_task(self):
        return self.action.get_action_name

    def __str__(self):
        return self.get_name_task


class Monitor(models.Model):
    value = models.DecimalField(max_digits=15, decimal_places=2)
    name = models.CharField(max_length=100)
    device = models.ForeignKey("devices.Device")
    date = models.DateTimeField(auto_now_add=True)

    @property
    def get_action_name(self):
        return "{} - {}".format(self.name, self.device.get_device_name)

    def __str__(self):
        return self.get_action_name
