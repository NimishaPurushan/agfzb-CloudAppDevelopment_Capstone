from django.db import models
from django.utils.timezone import now

class CarMake(models.Model):
    make_id = models.AutoField(primary_key=True) 
    name = models.CharField(null=False, max_length=30,default="")
    description = models.CharField(max_length=1000)
    def __str__(self):
        return self.name
    
class CarModel(models.Model):
    CAR_TYPES = (
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        # Add other choices as needed
    )

    model_id = models.AutoField(primary_key=True)  # Explicitly defining the primary key as AutoField
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='car_models')
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=CAR_TYPES)
    year = models.DateField()
 
    def __str__(self):
        return f"{self.name} ({self.type}) - {self.year.year}"



# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


# <HINT> Create a plain Python class `CarDealer` to hold dealer data

class CarDealer(models.Model):
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    full_name = models.CharField(max_length=50)
    id = models.AutoField(primary_key=True)
    lat = models.CharField(max_length=50)
    long = models.CharField(max_length=50)
    short_name = models.CharField(max_length=50)
    st = models.CharField(max_length=50)
    zip = models.CharField(max_length=50)

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview(models.Model):
    dealership= models.CharField(max_length=50)
    name= models.CharField(max_length=50)
    purchase= models.CharField(max_length=50)
    review= models.CharField(max_length=200)
    purchase_date= models.DateField()
    car_make= models.CharField(max_length=50)
    car_model= models.CharField(max_length=50)
    car_year= models.CharField(max_length=50)
    sentiment= models.CharField(max_length=50)
    id= models.AutoField(primary_key=True)

    def __str__(self):
        return "Review: " + self.review +\
                " Sentiment: " + self.sentiment