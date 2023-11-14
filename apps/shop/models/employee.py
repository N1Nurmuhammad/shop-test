from django.db import modelsclass EmployeeModel(models.Model):    full_name = models.CharField(max_length=255)    birthdate = models.DateField()    class Meta:        ordering = ['name']    @property    def clients_count(self):        return self.orders.all().values("client_id").count()    @property    def orders_count(self):        return self.orders.count()    @property    def unique_clients_count(self):        return self.orders.all().values("client_id").distinct("client_id").count()    @property    def orders_prices_sum(self):        return self.orders.all().aggregate(summa=models.Sum("price")).get("summa") or 0    def __str__(self):        return f"{self.full_name}"    class Meta:        verbose_name_plural = "Employees"        verbose_name = "Employee"        unique_together = ["full_name", "birthdate"]